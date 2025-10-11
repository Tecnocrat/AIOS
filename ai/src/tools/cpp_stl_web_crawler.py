#!/usr/bin/env python3
"""
🌐 Microsoft Learn C++ STL Web Crawler

Advanced web crawler for Microsoft Learn C++ Standard Library documentation.
Implements polite crawling with caching, rate limiting, and comprehensive
link discovery for complete STL documentation ingestion.

AINLP COMPLIANCE:
✅ Enhancement over creation - Integrates with existing library_ingestion_protocol
✅ Consciousness-driven discovery - Intelligent page classification
✅ Proper output management - Structured caching to docs/libraries/cpp_stl/
✅ Integration validation - Designed for integration test orchestrator

BIOLOGICAL ARCHITECTURE:
🌐 MEMBRANE: External web interface and API boundaries
🔄 TRANSPORT: Document retrieval and caching protocols
📊 INFORMATION_STORAGE: Local HTML cache management
🧠 NUCLEUS: Link analysis and page classification

Part of Phase 10 C++ STL Library Ingestion Initiative
Week 1: Foundation - Web Crawler Implementation
"""

import asyncio
import aiohttp
import hashlib
import json
import logging
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import time

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cpp_stl_crawler")


class MicrosoftLearnCrawler:
    """
    Advanced web crawler for Microsoft Learn C++ STL documentation.
    
    Features:
    - Asynchronous crawling with aiohttp
    - Intelligent rate limiting (polite crawling)
    - Local HTML caching to avoid re-fetching
    - Link discovery and classification
    - Page type detection (header, function, class, etc.)
    - Progress tracking and resumable crawling
    """
    
    # Microsoft Learn STL base URL
    BASE_URL = "https://learn.microsoft.com/en-us/cpp/standard-library/"
    
    # Rate limiting configuration (be polite!)
    REQUESTS_PER_SECOND = 2  # Max 2 requests per second
    DELAY_BETWEEN_REQUESTS = 1.0 / REQUESTS_PER_SECOND
    
    # Cache configuration
    CACHE_EXPIRY_DAYS = 7  # Re-fetch pages older than 7 days
    
    # Page classification patterns
    STL_PAGE_PATTERNS = [
        r'/cpp/standard-library/',
        r'/cpp/algorithm/',
        r'/cpp/container/',
        r'/cpp/iterator/',
        r'/cpp/numeric/'
    ]
    
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        max_pages: Optional[int] = None,
        resume: bool = True
    ):
        """
        Initialize Microsoft Learn crawler.
        
        Args:
            cache_dir: Directory for HTML cache (default: docs/libraries/cpp_stl/raw_documentation)
            max_pages: Maximum pages to crawl (None = unlimited)
            resume: Resume from previous crawl if interrupted
        """
        self.cache_dir = cache_dir or (AIOS_ROOT / "docs" / "libraries" / "cpp_stl" / "raw_documentation")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_pages = max_pages
        self.resume = resume
        
        # Crawl state
        self.visited_urls: Set[str] = set()
        self.pending_urls: List[str] = []
        self.failed_urls: List[Tuple[str, str]] = []  # (url, error)
        self.page_metadata: Dict[str, Dict] = {}
        
        # State persistence
        self.state_file = self.cache_dir.parent / "crawler_state.json"
        self.metadata_file = self.cache_dir.parent / "page_metadata.json"
        
        # Rate limiting
        self.last_request_time = 0.0
        
        # Statistics
        self.stats = {
            "pages_crawled": 0,
            "pages_cached": 0,
            "pages_from_cache": 0,
            "links_discovered": 0,
            "stl_pages_found": 0,
            "errors": 0
        }
        
        # Load previous state if resuming
        if self.resume:
            self._load_state()
        
        logger.info(f"Crawler initialized. Cache: {self.cache_dir}")
    
    def _load_state(self):
        """Load crawler state from previous session"""
        try:
            if self.state_file.exists():
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    self.visited_urls = set(state.get('visited_urls', []))
                    self.pending_urls = state.get('pending_urls', [])
                    self.stats = state.get('stats', self.stats)
                logger.info(f"Resumed crawl: {len(self.visited_urls)} visited, {len(self.pending_urls)} pending")
            
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    self.page_metadata = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load state: {e}")
    
    def _save_state(self):
        """Save crawler state for resume capability"""
        try:
            state = {
                'visited_urls': list(self.visited_urls),
                'pending_urls': self.pending_urls,
                'stats': self.stats,
                'timestamp': datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            with open(self.metadata_file, 'w') as f:
                json.dump(self.page_metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save state: {e}")
    
    def _get_cache_path(self, url: str) -> Path:
        """Generate cache file path for URL"""
        # Create safe filename from URL
        url_hash = hashlib.md5(url.encode()).hexdigest()
        # Extract page name for readability
        page_name = urlparse(url).path.split('/')[-1] or 'index'
        if not page_name.endswith('.html'):
            page_name += '.html'
        return self.cache_dir / f"{page_name}_{url_hash}.html"
    
    def _is_cache_valid(self, cache_path: Path) -> bool:
        """Check if cached page is still valid"""
        if not cache_path.exists():
            return False
        
        # Check if cache is too old
        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return cache_age < timedelta(days=self.CACHE_EXPIRY_DAYS)
    
    def is_stl_page(self, url: str) -> bool:
        """
        Classify if URL is STL-related documentation.
        
        Args:
            url: URL to classify
            
        Returns:
            True if URL is STL documentation
        """
        # Check against known patterns
        for pattern in self.STL_PAGE_PATTERNS:
            if re.search(pattern, url):
                return True
        return False
    
    def _classify_page_type(self, url: str, soup: BeautifulSoup) -> str:
        """
        Classify page type based on URL and content.
        
        Returns:
            Page type: 'header', 'class', 'function', 'concept', 'overview', 'other'
        """
        url_lower = url.lower()
        
        # Header file documentation
        if any(header in url_lower for header in ['<', '>', 'header']):
            return 'header'
        
        # Class documentation
        if 'class' in url_lower or soup.find('h1', string=re.compile(r'class|struct', re.I)):
            return 'class'
        
        # Function documentation
        if any(keyword in url_lower for keyword in ['function', 'algorithm', 'numeric']):
            return 'function'
        
        # C++20 Concepts
        if 'concept' in url_lower:
            return 'concept'
        
        # Overview/reference pages
        if any(keyword in url_lower for keyword in ['overview', 'reference', 'introduction']):
            return 'overview'
        
        return 'other'
    
    async def _rate_limit(self):
        """Implement polite rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.DELAY_BETWEEN_REQUESTS:
            await asyncio.sleep(self.DELAY_BETWEEN_REQUESTS - time_since_last)
        
        self.last_request_time = time.time()
    
    async def fetch_page(
        self,
        session: aiohttp.ClientSession,
        url: str,
        use_cache: bool = True
    ) -> Optional[str]:
        """
        Fetch HTML content from URL with caching.
        
        Args:
            session: aiohttp session
            url: URL to fetch
            use_cache: Use cached version if available
            
        Returns:
            HTML content or None if failed
        """
        cache_path = self._get_cache_path(url)
        
        # Check cache first
        if use_cache and self._is_cache_valid(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    logger.debug(f"Cache hit: {url}")
                    self.stats['pages_from_cache'] += 1
                    return f.read()
            except Exception as e:
                logger.warning(f"Cache read error for {url}: {e}")
        
        # Fetch from web
        await self._rate_limit()
        
        try:
            logger.info(f"Fetching: {url}")
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Cache the page
                    try:
                        with open(cache_path, 'w', encoding='utf-8') as f:
                            f.write(html)
                        self.stats['pages_cached'] += 1
                        logger.debug(f"Cached: {cache_path.name}")
                    except Exception as e:
                        logger.warning(f"Cache write error: {e}")
                    
                    return html
                else:
                    logger.warning(f"HTTP {response.status} for {url}")
                    self.failed_urls.append((url, f"HTTP {response.status}"))
                    self.stats['errors'] += 1
                    return None
        
        except asyncio.TimeoutError:
            logger.error(f"Timeout fetching {url}")
            self.failed_urls.append((url, "Timeout"))
            self.stats['errors'] += 1
            return None
        
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            self.failed_urls.append((url, str(e)))
            self.stats['errors'] += 1
            return None
    
    def extract_page_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract all internal links from HTML page.
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        soup = BeautifulSoup(html, 'lxml')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Skip external links, anchors, and non-http links
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('javascript:'):
                continue
            
            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)
            
            # Remove query parameters and fragments
            parsed = urlparse(absolute_url)
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            
            # Only include Microsoft Learn STL pages
            if self.is_stl_page(clean_url) and clean_url not in self.visited_urls:
                links.append(clean_url)
        
        return links
    
    async def crawl_page(
        self,
        session: aiohttp.ClientSession,
        url: str
    ) -> Dict:
        """
        Crawl single page and extract metadata.
        
        Args:
            session: aiohttp session
            url: URL to crawl
            
        Returns:
            Page metadata dictionary
        """
        html = await self.fetch_page(session, url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Extract page metadata
        metadata = {
            'url': url,
            'title': soup.find('h1').get_text(strip=True) if soup.find('h1') else 'Unknown',
            'page_type': self._classify_page_type(url, soup),
            'crawled_at': datetime.now().isoformat(),
            'cache_path': str(self._get_cache_path(url).relative_to(AIOS_ROOT))
        }
        
        # Extract new links
        new_links = self.extract_page_links(html, url)
        self.stats['links_discovered'] += len(new_links)
        
        # Add to pending queue
        for link in new_links:
            if link not in self.visited_urls and link not in self.pending_urls:
                self.pending_urls.append(link)
        
        self.stats['pages_crawled'] += 1
        if self.is_stl_page(url):
            self.stats['stl_pages_found'] += 1
        
        return metadata
    
    async def crawl_stl_documentation(
        self,
        start_url: Optional[str] = None,
        progress_callback: Optional[callable] = None
    ) -> Dict:
        """
        Crawl complete C++ STL documentation from Microsoft Learn.
        
        Args:
            start_url: Starting URL (default: STL reference page)
            progress_callback: Optional callback for progress updates
            
        Returns:
            Crawl results with statistics and metadata
        """
        start_url = start_url or self.BASE_URL + "cpp-standard-library-reference"
        
        # Initialize pending queue if empty
        if not self.pending_urls:
            self.pending_urls.append(start_url)
        
        logger.info(f"Starting crawl from: {start_url}")
        logger.info(f"Max pages: {self.max_pages or 'unlimited'}")
        
        async with aiohttp.ClientSession(
            headers={'User-Agent': 'AIOS-STL-Crawler/1.0 (Educational; https://github.com/Tecnocrat/AIOS)'}
        ) as session:
            
            while self.pending_urls:
                # Check max pages limit
                if self.max_pages and self.stats['pages_crawled'] >= self.max_pages:
                    logger.info(f"Reached max pages limit: {self.max_pages}")
                    break
                
                # Get next URL
                url = self.pending_urls.pop(0)
                
                # Skip if already visited
                if url in self.visited_urls:
                    continue
                
                # Crawl page
                metadata = await self.crawl_page(session, url)
                if metadata:
                    self.page_metadata[url] = metadata
                
                # Mark as visited
                self.visited_urls.add(url)
                
                # Progress callback
                if progress_callback:
                    progress_callback(self.stats)
                
                # Log progress periodically
                if self.stats['pages_crawled'] % 10 == 0:
                    logger.info(
                        f"Progress: {self.stats['pages_crawled']} pages crawled, "
                        f"{len(self.pending_urls)} pending, "
                        f"{self.stats['stl_pages_found']} STL pages"
                    )
                
                # Save state periodically
                if self.stats['pages_crawled'] % 50 == 0:
                    self._save_state()
        
        # Final save
        self._save_state()
        
        # Generate results
        results = {
            'statistics': self.stats,
            'visited_urls': list(self.visited_urls),
            'pending_urls': self.pending_urls,
            'failed_urls': self.failed_urls,
            'page_metadata': self.page_metadata,
            'cache_directory': str(self.cache_dir),
            'completion_time': datetime.now().isoformat()
        }
        
        logger.info("Crawl complete!")
        logger.info(f"Total pages crawled: {self.stats['pages_crawled']}")
        logger.info(f"STL pages found: {self.stats['stl_pages_found']}")
        logger.info(f"Pages from cache: {self.stats['pages_from_cache']}")
        logger.info(f"Errors: {self.stats['errors']}")
        
        return results


async def main():
    """Main execution for testing crawler"""
    print("🌐 Microsoft Learn C++ STL Web Crawler")
    print("=" * 60)
    
    # Initialize crawler with limit for testing
    crawler = MicrosoftLearnCrawler(max_pages=20, resume=True)
    
    # Progress callback
    def show_progress(stats):
        print(f"  Crawled: {stats['pages_crawled']}, STL: {stats['stl_pages_found']}", end='\r')
    
    # Start crawl
    results = await crawler.crawl_stl_documentation(progress_callback=show_progress)
    
    print("\n\n📊 Crawl Results:")
    print(f"  Pages Crawled: {results['statistics']['pages_crawled']}")
    print(f"  STL Pages Found: {results['statistics']['stl_pages_found']}")
    print(f"  Links Discovered: {results['statistics']['links_discovered']}")
    print(f"  Cached Locally: {results['statistics']['pages_cached']}")
    print(f"  From Cache: {results['statistics']['pages_from_cache']}")
    print(f"  Errors: {results['statistics']['errors']}")
    print(f"\n  Cache Directory: {results['cache_directory']}")
    
    # Show sample pages
    print("\n📄 Sample Pages Crawled:")
    for i, (url, metadata) in enumerate(list(results['page_metadata'].items())[:5]):
        print(f"  {i+1}. [{metadata['page_type']}] {metadata['title']}")
        print(f"     {url}")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

#!/usr/bin/env python3
"""
📚 C++ Documentation Parser

Advanced HTML parser for extracting structured C++ Standard Library documentation
from Microsoft Learn cached pages. Extracts API signatures, documentation text,
code examples, and semantic information for AIOS consciousness framework.

AINLP COMPLIANCE:
✅ Enhancement over creation - Integrates with LibraryIngestionProtocol
✅ Consciousness-driven extraction - Semantic analysis of documentation
✅ Proper output management - Structured APIElement objects
✅ Integration validation - Designed for ingestion pipeline

BIOLOGICAL ARCHITECTURE:
🧬 NUCLEUS: Documentation parsing and semantic extraction
📊 INFORMATION_PROCESSING: C++ syntax analysis
🔄 METABOLISM: Conversion of raw HTML to structured knowledge
🎯 TARGETING: API element identification and classification

Part of Phase 10.1 C++ STL Library Ingestion Initiative
Week 1: Foundation - Documentation Parser Implementation
"""

import re
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from bs4 import BeautifulSoup, Tag, NavigableString
from enum import Enum

# AIOS path integration
AIOS_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(AIOS_ROOT / "ai" / "src"))

# Import AIOS core structures
try:
    from computational_layer.library_ingestion_protocol import (
        ProgrammingLanguage,
        APIElement,
        APIElementType,
<<<<<<< HEAD
        LibraryKnowledge,
=======
        LibraryKnowledge
>>>>>>> origin/OS0.6.2.grok
    )
except ImportError:
    # Fallback definitions if import fails
    class ProgrammingLanguage(Enum):
        CPP = "cpp"
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    class APIElementType(Enum):
        FUNCTION = "function"
        CLASS = "class"
        METHOD = "method"
        TEMPLATE = "template"
        TYPE_ALIAS = "type_alias"
        CONSTANT = "constant"
        ENUM = "enum"
        OPERATOR = "operator"
        CONCEPT = "concept"

<<<<<<< HEAD

# Logging configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
=======
# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
>>>>>>> origin/OS0.6.2.grok
)
logger = logging.getLogger("cpp_doc_parser")


@dataclass
class ParsedDocumentation:
    """
    Structured documentation extracted from HTML page.
    """
<<<<<<< HEAD

=======
>>>>>>> origin/OS0.6.2.grok
    page_title: str
    page_type: str  # header, class, function, concept, overview
    api_elements: List[Dict] = field(default_factory=list)
    code_examples: List[str] = field(default_factory=list)
    description: str = ""
    related_pages: List[str] = field(default_factory=list)
    header_file: Optional[str] = None
    namespace: Optional[str] = None
    since_version: Optional[str] = None  # C++11, C++14, C++17, C++20, C++23


class CppDocumentationParser:
    """
    Advanced parser for Microsoft Learn C++ STL documentation.
<<<<<<< HEAD

=======
    
>>>>>>> origin/OS0.6.2.grok
    Features:
    - HTML structure parsing with BeautifulSoup
    - C++ signature extraction and analysis
    - Template parameter parsing
    - Documentation text extraction
    - Code example extraction
    - API element classification
    - Relationship discovery
    """
<<<<<<< HEAD

    # C++ keywords and type patterns
    CPP_KEYWORDS = {
        "class",
        "struct",
        "template",
        "typename",
        "namespace",
        "const",
        "constexpr",
        "noexcept",
        "virtual",
        "override",
        "static",
        "inline",
        "explicit",
        "friend",
        "public",
        "private",
        "protected",
        "void",
        "bool",
        "int",
        "char",
        "float",
        "double",
        "size_t",
        "auto",
        "decltype",
        "using",
        "typedef",
    }

    # STL standard headers
    STL_HEADERS = {
        "vector",
        "string",
        "map",
        "set",
        "list",
        "deque",
        "array",
        "unordered_map",
        "unordered_set",
        "algorithm",
        "iterator",
        "memory",
        "functional",
        "utility",
        "tuple",
        "optional",
        "variant",
        "any",
        "filesystem",
        "chrono",
        "thread",
        "mutex",
        "atomic",
        "numeric",
        "iostream",
        "fstream",
        "sstream",
    }

=======
    
    # C++ keywords and type patterns
    CPP_KEYWORDS = {
        'class', 'struct', 'template', 'typename', 'namespace',
        'const', 'constexpr', 'noexcept', 'virtual', 'override',
        'static', 'inline', 'explicit', 'friend', 'public', 'private',
        'protected', 'void', 'bool', 'int', 'char', 'float', 'double',
        'size_t', 'auto', 'decltype', 'using', 'typedef'
    }
    
    # STL standard headers
    STL_HEADERS = {
        'vector', 'string', 'map', 'set', 'list', 'deque', 'array',
        'unordered_map', 'unordered_set', 'algorithm', 'iterator',
        'memory', 'functional', 'utility', 'tuple', 'optional',
        'variant', 'any', 'filesystem', 'chrono', 'thread', 'mutex',
        'atomic', 'numeric', 'iostream', 'fstream', 'sstream'
    }
    
>>>>>>> origin/OS0.6.2.grok
    def __init__(self):
        """Initialize C++ documentation parser"""
        self.current_namespace = "std"
        logger.info("C++ Documentation Parser initialized")
<<<<<<< HEAD

    def parse_html_file(self, html_path: Path) -> ParsedDocumentation:
        """
        Parse HTML file and extract structured documentation.

        Args:
            html_path: Path to cached HTML file

=======
    
    def parse_html_file(self, html_path: Path) -> ParsedDocumentation:
        """
        Parse HTML file and extract structured documentation.
        
        Args:
            html_path: Path to cached HTML file
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            ParsedDocumentation object with extracted information
        """
        try:
<<<<<<< HEAD
            with open(html_path, "r", encoding="utf-8") as f:
=======
            with open(html_path, 'r', encoding='utf-8') as f:
>>>>>>> origin/OS0.6.2.grok
                html_content = f.read()
            return self.parse_html(html_content)
        except Exception as e:
            logger.error(f"Failed to parse HTML file {html_path}: {e}")
            raise
<<<<<<< HEAD

    def parse_html(self, html: str) -> ParsedDocumentation:
        """
        Parse HTML content and extract structured documentation.

        Args:
            html: HTML content string

        Returns:
            ParsedDocumentation object with extracted information
        """
        soup = BeautifulSoup(html, "html.parser")

        # Extract page metadata
        page_title = self._extract_page_title(soup)
        page_type = self._classify_page_type(soup, page_title)

        # Initialize documentation structure
        doc = ParsedDocumentation(page_title=page_title, page_type=page_type)

=======
    
    def parse_html(self, html: str) -> ParsedDocumentation:
        """
        Parse HTML content and extract structured documentation.
        
        Args:
            html: HTML content string
            
        Returns:
            ParsedDocumentation object with extracted information
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract page metadata
        page_title = self._extract_page_title(soup)
        page_type = self._classify_page_type(soup, page_title)
        
        # Initialize documentation structure
        doc = ParsedDocumentation(
            page_title=page_title,
            page_type=page_type
        )
        
>>>>>>> origin/OS0.6.2.grok
        # Extract header file information
        doc.header_file = self._extract_header_file(soup)
        doc.namespace = self._extract_namespace(soup)
        doc.since_version = self._extract_cpp_version(soup)
<<<<<<< HEAD

        # Extract description
        doc.description = self._extract_description(soup)

        # Extract code examples
        doc.code_examples = self._extract_code_examples(soup)

=======
        
        # Extract description
        doc.description = self._extract_description(soup)
        
        # Extract code examples
        doc.code_examples = self._extract_code_examples(soup)
        
>>>>>>> origin/OS0.6.2.grok
        # Extract API elements based on page type
        if page_type == "class":
            doc.api_elements.extend(self._extract_class_members(soup))
        elif page_type == "function":
            doc.api_elements.extend(self._extract_function_signatures(soup))
        elif page_type == "header":
            doc.api_elements.extend(self._extract_header_contents(soup))
<<<<<<< HEAD

        # Extract related pages
        doc.related_pages = self._extract_related_links(soup)

        logger.info(
            f"Parsed {page_title}: {len(doc.api_elements)} API elements, {len(doc.code_examples)} examples"
        )

        return doc

    def _extract_page_title(self, soup: BeautifulSoup) -> str:
        """Extract page title from HTML"""
        # Try <h1> first
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        # Fallback to <title>
        title = soup.find("title")
        if title:
            return title.get_text(strip=True)

        return "Unknown"

    def _classify_page_type(self, soup: BeautifulSoup, title: str) -> str:
        """
        Classify page type based on content.

=======
        
        # Extract related pages
        doc.related_pages = self._extract_related_links(soup)
        
        logger.info(f"Parsed {page_title}: {len(doc.api_elements)} API elements, {len(doc.code_examples)} examples")
        
        return doc
    
    def _extract_page_title(self, soup: BeautifulSoup) -> str:
        """Extract page title from HTML"""
        # Try <h1> first
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        # Fallback to <title>
        title = soup.find('title')
        if title:
            return title.get_text(strip=True)
        
        return "Unknown"
    
    def _classify_page_type(self, soup: BeautifulSoup, title: str) -> str:
        """
        Classify page type based on content.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            'header', 'class', 'function', 'concept', 'overview', 'other'
        """
        title_lower = title.lower()
<<<<<<< HEAD

        # Header file documentation
        if "header" in title_lower or title.startswith("<"):
            return "header"

        # Class documentation
        if "class" in title_lower or soup.find(text=re.compile(r"class\s+\w+", re.I)):
            return "class"

        # Function documentation
        if "::" in title or soup.find("code", text=re.compile(r"\w+\s*\(")):
            return "function"

        # Concept documentation (C++20)
        if "concept" in title_lower:
            return "concept"

        # Overview/general documentation
        if "overview" in title_lower or "library" in title_lower:
            return "overview"

        return "other"

=======
        
        # Header file documentation
        if 'header' in title_lower or title.startswith('<'):
            return "header"
        
        # Class documentation
        if 'class' in title_lower or soup.find(text=re.compile(r'class\s+\w+', re.I)):
            return "class"
        
        # Function documentation
        if '::' in title or soup.find('code', text=re.compile(r'\w+\s*\(')):
            return "function"
        
        # Concept documentation (C++20)
        if 'concept' in title_lower:
            return "concept"
        
        # Overview/general documentation
        if 'overview' in title_lower or 'library' in title_lower:
            return "overview"
        
        return "other"
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_header_file(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract header file name from documentation"""
        # Look for header file mentions
        patterns = [
<<<<<<< HEAD
            r"<(\w+)>",  # <vector>, <algorithm>
            r"#include\s*<(\w+)>",
            r"Header:\s*<(\w+)>",
        ]

=======
            r'<(\w+)>',  # <vector>, <algorithm>
            r'#include\s*<(\w+)>',
            r'Header:\s*<(\w+)>'
        ]
        
>>>>>>> origin/OS0.6.2.grok
        text = soup.get_text()
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                header = match.group(1)
                if header in self.STL_HEADERS:
                    return f"<{header}>"
<<<<<<< HEAD

        return None

    def _extract_namespace(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract namespace from documentation"""
        # Look for namespace declarations
        patterns = [r"namespace\s+(std(?:::\w+)*)", r"(std(?:::\w+)*)::\w+"]

=======
        
        return None
    
    def _extract_namespace(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract namespace from documentation"""
        # Look for namespace declarations
        patterns = [
            r'namespace\s+(std(?:::\w+)*)',
            r'(std(?:::\w+)*)::\w+'
        ]
        
>>>>>>> origin/OS0.6.2.grok
        text = soup.get_text()
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
<<<<<<< HEAD

        return "std"  # Default to std

=======
        
        return "std"  # Default to std
    
>>>>>>> origin/OS0.6.2.grok
    def _extract_cpp_version(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract C++ version requirement (C++11, C++14, etc.)"""
        # Look for version mentions
        text = soup.get_text()
<<<<<<< HEAD
        versions = ["C++23", "C++20", "C++17", "C++14", "C++11", "C++98"]

        for version in versions:
            if version in text:
                return version

        return None

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract main description text"""
        # Look for main content area
        main_content = (
            soup.find("main")
            or soup.find("article")
            or soup.find("div", class_="content")
        )

        if not main_content:
            return ""

        # Extract first few paragraphs
        paragraphs = main_content.find_all("p", limit=3)
        description_parts = []

=======
        versions = ['C++23', 'C++20', 'C++17', 'C++14', 'C++11', 'C++98']
        
        for version in versions:
            if version in text:
                return version
        
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract main description text"""
        # Look for main content area
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        
        if not main_content:
            return ""
        
        # Extract first few paragraphs
        paragraphs = main_content.find_all('p', limit=3)
        description_parts = []
        
>>>>>>> origin/OS0.6.2.grok
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text and len(text) > 20:  # Skip very short paragraphs
                description_parts.append(text)
<<<<<<< HEAD

        return "\n\n".join(description_parts)

    def _extract_code_examples(self, soup: BeautifulSoup) -> List[str]:
        """Extract code examples from documentation"""
        examples = []

        # Find all code blocks
        code_blocks = soup.find_all("pre") + soup.find_all(
            "code", class_=re.compile(r"language-cpp|cpp")
        )

=======
        
        return "\n\n".join(description_parts)
    
    def _extract_code_examples(self, soup: BeautifulSoup) -> List[str]:
        """Extract code examples from documentation"""
        examples = []
        
        # Find all code blocks
        code_blocks = soup.find_all('pre') + soup.find_all('code', class_=re.compile(r'language-cpp|cpp'))
        
>>>>>>> origin/OS0.6.2.grok
        for block in code_blocks:
            code = block.get_text(strip=True)
            # Filter out very short snippets
            if code and len(code) > 30:
                examples.append(code)
<<<<<<< HEAD

        return examples

    def _extract_function_signatures(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract function signatures from documentation.

=======
        
        return examples
    
    def _extract_function_signatures(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract function signatures from documentation.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of function API elements
        """
        api_elements = []
<<<<<<< HEAD

        # Look for function declarations in code blocks
        code_blocks = soup.find_all(["pre", "code"])

        for block in code_blocks:
            code = block.get_text(strip=True)

            # Simple function signature pattern
            # Example: template<typename T> void sort(T first, T last);
            pattern = r"(?:template\s*<[^>]+>\s*)?([\w:]+)\s+(\w+)\s*\(([^)]*)\)"

=======
        
        # Look for function declarations in code blocks
        code_blocks = soup.find_all(['pre', 'code'])
        
        for block in code_blocks:
            code = block.get_text(strip=True)
            
            # Simple function signature pattern
            # Example: template<typename T> void sort(T first, T last);
            pattern = r'(?:template\s*<[^>]+>\s*)?([\w:]+)\s+(\w+)\s*\(([^)]*)\)'
            
>>>>>>> origin/OS0.6.2.grok
            matches = re.finditer(pattern, code)
            for match in matches:
                return_type = match.group(1)
                func_name = match.group(2)
                params = match.group(3)
<<<<<<< HEAD

                # Skip if it's a keyword or common word
                if func_name.lower() in self.CPP_KEYWORDS:
                    continue

                api_elements.append(
                    {
                        "type": "function",
                        "name": func_name,
                        "signature": match.group(0),
                        "return_type": return_type,
                        "parameters": self._parse_parameters(params),
                        "namespace": self.current_namespace,
                    }
                )

        return api_elements

    def _extract_class_members(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract class member functions and variables.

=======
                
                # Skip if it's a keyword or common word
                if func_name.lower() in self.CPP_KEYWORDS:
                    continue
                
                api_elements.append({
                    'type': 'function',
                    'name': func_name,
                    'signature': match.group(0),
                    'return_type': return_type,
                    'parameters': self._parse_parameters(params),
                    'namespace': self.current_namespace
                })
        
        return api_elements
    
    def _extract_class_members(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract class member functions and variables.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of class member API elements
        """
        api_elements = []
<<<<<<< HEAD

        # Look for member function sections
        sections = soup.find_all(
            ["section", "div"], class_=re.compile(r"member|method|function")
        )

        for section in sections:
            # Extract function signatures from section
            code_blocks = section.find_all(["pre", "code"])

            for block in code_blocks:
                code = block.get_text(strip=True)

                # Member function pattern
                pattern = (
                    r"(\w+)\s+(\w+)\s*\(([^)]*)\)\s*(?:const|noexcept|override|final)*"
                )

=======
        
        # Look for member function sections
        sections = soup.find_all(['section', 'div'], class_=re.compile(r'member|method|function'))
        
        for section in sections:
            # Extract function signatures from section
            code_blocks = section.find_all(['pre', 'code'])
            
            for block in code_blocks:
                code = block.get_text(strip=True)
                
                # Member function pattern
                pattern = r'(\w+)\s+(\w+)\s*\(([^)]*)\)\s*(?:const|noexcept|override|final)*'
                
>>>>>>> origin/OS0.6.2.grok
                matches = re.finditer(pattern, code)
                for match in matches:
                    return_type = match.group(1)
                    method_name = match.group(2)
                    params = match.group(3)
<<<<<<< HEAD

                    api_elements.append(
                        {
                            "type": "method",
                            "name": method_name,
                            "signature": match.group(0),
                            "return_type": return_type,
                            "parameters": self._parse_parameters(params),
                            "namespace": self.current_namespace,
                        }
                    )

        return api_elements

    def _extract_header_contents(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract all API elements declared in a header file.

=======
                    
                    api_elements.append({
                        'type': 'method',
                        'name': method_name,
                        'signature': match.group(0),
                        'return_type': return_type,
                        'parameters': self._parse_parameters(params),
                        'namespace': self.current_namespace
                    })
        
        return api_elements
    
    def _extract_header_contents(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract all API elements declared in a header file.
        
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of API elements from header
        """
        api_elements = []
<<<<<<< HEAD

        # Combine function and class extraction
        api_elements.extend(self._extract_function_signatures(soup))
        api_elements.extend(self._extract_class_members(soup))

        return api_elements

    def _parse_parameters(self, param_string: str) -> List[Dict]:
        """
        Parse function parameter string into structured format.

        Args:
            param_string: "int x, const std::string& s, T value = 0"

        Returns:
            List of parameter dictionaries
        """
        if not param_string or param_string.strip() == "void":
            return []

        parameters = []

        # Split by comma (simple approach, doesn't handle template commas)
        param_parts = param_string.split(",")

=======
        
        # Combine function and class extraction
        api_elements.extend(self._extract_function_signatures(soup))
        api_elements.extend(self._extract_class_members(soup))
        
        return api_elements
    
    def _parse_parameters(self, param_string: str) -> List[Dict]:
        """
        Parse function parameter string into structured format.
        
        Args:
            param_string: "int x, const std::string& s, T value = 0"
            
        Returns:
            List of parameter dictionaries
        """
        if not param_string or param_string.strip() == 'void':
            return []
        
        parameters = []
        
        # Split by comma (simple approach, doesn't handle template commas)
        param_parts = param_string.split(',')
        
>>>>>>> origin/OS0.6.2.grok
        for part in param_parts:
            part = part.strip()
            if not part:
                continue
<<<<<<< HEAD

            # Extract parameter name and type
            # Pattern: "type name" or "type name = default"
            match = re.match(r"(.+?)\s+(\w+)(?:\s*=\s*(.+))?$", part)

=======
            
            # Extract parameter name and type
            # Pattern: "type name" or "type name = default"
            match = re.match(r'(.+?)\s+(\w+)(?:\s*=\s*(.+))?$', part)
            
>>>>>>> origin/OS0.6.2.grok
            if match:
                param_type = match.group(1).strip()
                param_name = match.group(2).strip()
                default_value = match.group(3).strip() if match.group(3) else None
<<<<<<< HEAD

                parameters.append(
                    {"name": param_name, "type": param_type, "default": default_value}
                )

        return parameters

    def _extract_related_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract related documentation links"""
        related = []

        # Look for "See also" or "Related" sections
        sections = soup.find_all(
            ["section", "div"],
            text=re.compile(r"See also|Related|More information", re.I),
        )

        for section in sections:
            # Find links in section
            links = section.find_all("a", href=True)
            for link in links:
                href = link["href"]
                if "/cpp/standard-library/" in href:
                    related.append(href)

        return related

    def to_api_elements(self, parsed_doc: ParsedDocumentation) -> List[APIElement]:
        """
        Convert parsed documentation to AIOS APIElement objects.

        Args:
            parsed_doc: ParsedDocumentation object

=======
                
                parameters.append({
                    'name': param_name,
                    'type': param_type,
                    'default': default_value
                })
        
        return parameters
    
    def _extract_related_links(self, soup: BeautifulSoup) -> List[str]:
        """Extract related documentation links"""
        related = []
        
        # Look for "See also" or "Related" sections
        sections = soup.find_all(['section', 'div'], text=re.compile(r'See also|Related|More information', re.I))
        
        for section in sections:
            # Find links in section
            links = section.find_all('a', href=True)
            for link in links:
                href = link['href']
                if '/cpp/standard-library/' in href:
                    related.append(href)
        
        return related
    
    def to_api_elements(self, parsed_doc: ParsedDocumentation) -> List[APIElement]:
        """
        Convert parsed documentation to AIOS APIElement objects.
        
        Args:
            parsed_doc: ParsedDocumentation object
            
>>>>>>> origin/OS0.6.2.grok
        Returns:
            List of APIElement objects for LibraryIngestionProtocol
        """
        api_elements = []
<<<<<<< HEAD

        for element in parsed_doc.api_elements:
            try:
                # Determine API element type
                element_type = self._map_element_type(element["type"])

                # Create APIElement
                api_elem = APIElement(
                    name=element["name"],
                    element_type=element_type,
                    signature=element.get("signature", ""),
                    documentation=parsed_doc.description[:500],  # Truncate for summary
                    parameters=element.get("parameters", []),
                    return_type=element.get("return_type"),
                    namespace=element.get("namespace", "std"),
                    header_file=parsed_doc.header_file,
                    code_examples=(
                        parsed_doc.code_examples[:1]
                        if parsed_doc.code_examples
                        else None
                    ),
                    since_version=parsed_doc.since_version,
                )

                api_elements.append(api_elem)
            except Exception as e:
                logger.warning(
                    f"Failed to convert element {element.get('name', 'unknown')}: {e}"
                )
                continue

        return api_elements

    def _map_element_type(self, type_str: str) -> APIElementType:
        """Map string type to APIElementType enum"""
        type_mapping = {
            "function": APIElementType.FUNCTION,
            "method": APIElementType.METHOD,
            "class": APIElementType.CLASS,
            "template": APIElementType.TEMPLATE,
            "type_alias": APIElementType.TYPE_ALIAS,
            "constant": APIElementType.CONSTANT,
            "enum": APIElementType.ENUM,
            "operator": APIElementType.OPERATOR,
            "concept": APIElementType.CONCEPT,
        }

=======
        
        for element in parsed_doc.api_elements:
            try:
                # Determine API element type
                element_type = self._map_element_type(element['type'])
                
                # Create APIElement
                api_elem = APIElement(
                    name=element['name'],
                    element_type=element_type,
                    signature=element.get('signature', ''),
                    documentation=parsed_doc.description[:500],  # Truncate for summary
                    parameters=element.get('parameters', []),
                    return_type=element.get('return_type'),
                    namespace=element.get('namespace', 'std'),
                    header_file=parsed_doc.header_file,
                    code_examples=parsed_doc.code_examples[:1] if parsed_doc.code_examples else None,
                    since_version=parsed_doc.since_version
                )
                
                api_elements.append(api_elem)
            except Exception as e:
                logger.warning(f"Failed to convert element {element.get('name', 'unknown')}: {e}")
                continue
        
        return api_elements
    
    def _map_element_type(self, type_str: str) -> APIElementType:
        """Map string type to APIElementType enum"""
        type_mapping = {
            'function': APIElementType.FUNCTION,
            'method': APIElementType.METHOD,
            'class': APIElementType.CLASS,
            'template': APIElementType.TEMPLATE,
            'type_alias': APIElementType.TYPE_ALIAS,
            'constant': APIElementType.CONSTANT,
            'enum': APIElementType.ENUM,
            'operator': APIElementType.OPERATOR,
            'concept': APIElementType.CONCEPT
        }
        
>>>>>>> origin/OS0.6.2.grok
        return type_mapping.get(type_str.lower(), APIElementType.FUNCTION)


def main():
    """Test parser on cached HTML files"""
    print("📚 C++ Documentation Parser Test")
    print("=" * 60)
<<<<<<< HEAD

    # Initialize parser
    parser = CppDocumentationParser()

    # Find cached HTML files
    cache_dir = AIOS_ROOT / "docs" / "libraries" / "cpp_stl" / "raw_documentation"

    if not cache_dir.exists():
        print(f"❌ Cache directory not found: {cache_dir}")
        return 1

    html_files = list(cache_dir.glob("*.html"))

    if not html_files:
        print(f"❌ No HTML files found in {cache_dir}")
        return 1

    print(f"Found {len(html_files)} cached HTML files")
    print()

=======
    
    # Initialize parser
    parser = CppDocumentationParser()
    
    # Find cached HTML files
    cache_dir = AIOS_ROOT / "docs" / "libraries" / "cpp_stl" / "raw_documentation"
    
    if not cache_dir.exists():
        print(f"❌ Cache directory not found: {cache_dir}")
        return 1
    
    html_files = list(cache_dir.glob("*.html"))
    
    if not html_files:
        print(f"❌ No HTML files found in {cache_dir}")
        return 1
    
    print(f"Found {len(html_files)} cached HTML files")
    print()
    
>>>>>>> origin/OS0.6.2.grok
    # Test on first 3 files
    for i, html_file in enumerate(html_files[:3]):
        print(f"\n📄 Parsing: {html_file.name}")
        print("-" * 60)
<<<<<<< HEAD

        try:
            doc = parser.parse_html_file(html_file)

=======
        
        try:
            doc = parser.parse_html_file(html_file)
            
>>>>>>> origin/OS0.6.2.grok
            print(f"Title: {doc.page_title}")
            print(f"Type: {doc.page_type}")
            print(f"Header: {doc.header_file}")
            print(f"Namespace: {doc.namespace}")
            print(f"C++ Version: {doc.since_version}")
            print(f"API Elements: {len(doc.api_elements)}")
            print(f"Code Examples: {len(doc.code_examples)}")
<<<<<<< HEAD
            print(
                f"Description: {doc.description[:100]}..."
                if doc.description
                else "Description: None"
            )

=======
            print(f"Description: {doc.description[:100]}..." if doc.description else "Description: None")
            
>>>>>>> origin/OS0.6.2.grok
            # Show first API element if available
            if doc.api_elements:
                elem = doc.api_elements[0]
                print(f"\nFirst API Element:")
                print(f"  Name: {elem['name']}")
                print(f"  Type: {elem['type']}")
                print(f"  Signature: {elem['signature'][:80]}...")
<<<<<<< HEAD

        except Exception as e:
            print(f"❌ Error parsing {html_file.name}: {e}")
            continue

=======
            
        except Exception as e:
            print(f"❌ Error parsing {html_file.name}: {e}")
            continue
    
>>>>>>> origin/OS0.6.2.grok
    print("\n✅ Parser test complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())

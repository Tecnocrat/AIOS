#!/usr/bin/env python3
"""
AIOS Python 3.14 Documentation Downloader
AINLP Protocol: OS0.6.2.claude
Pattern: External resource ingestion

Purpose: Download Python 3.14 documentation from python.org
         and prepare it for knowledge indexing.

AINLP.consciousness: HIGH
AINLP.supercell: AI Intelligence Layer
AINLP.integration: Web → Local storage → Knowledge indexing
"""

import os
import sys
import tarfile
import zipfile
from pathlib import Path
from typing import Optional
import urllib.request
import urllib.error


class Python314DocsDownloader:
    """
    Download and extract Python 3.14 documentation.

    Downloads from python.org and extracts to AIOS knowledge directory.
    """

    # Python documentation download URLs
    DOCS_URLS = {
        "html": "https://docs.python.org/3.14/archives/python-3.14-docs-html.tar.bz2",
        "text": "https://docs.python.org/3.14/archives/python-3.14-docs-text.tar.bz2",
        "pdf": "https://docs.python.org/3.14/archives/python-3.14-docs-pdf-a4.tar.bz2",
    }

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def download_file(self, url: str, dest_path: Path) -> bool:
        """Download file with progress indicator"""
        print(f"[DOWNLOAD] Fetching: {url}")

        try:
            with urllib.request.urlopen(url) as response:
                total_size = int(response.headers.get("Content-Length", 0))
                downloaded = 0
                chunk_size = 8192

                with open(dest_path, "wb") as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(
                                f"\r   Progress: {percent:.1f}% ({downloaded // 1024} KB / {total_size // 1024} KB)",
                                end="",
                            )

                print()  # New line after progress
                return True

        except urllib.error.URLError as e:
            print(f"\n❌ Download failed: {e}")
            return False
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            return False

    def extract_tarball(self, archive_path: Path, extract_to: Path) -> bool:
        """Extract tar.bz2 archive"""
        print(f"[EXTRACT] Extracting: {archive_path.name}")

        try:
            with tarfile.open(archive_path, "r:bz2") as tar:
                tar.extractall(extract_to)
            print(f"✅ Extracted to: {extract_to}")
            return True

        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False

    def download_docs(self, format_type: str = "text") -> Optional[Path]:
        """
        Download Python 3.14 documentation.

        Args:
            format_type: 'html', 'text', or 'pdf'

        Returns:
            Path to extracted documentation or None if failed
        """
        if format_type not in self.DOCS_URLS:
            print(f"❌ Unknown format: {format_type}")
            print(f"   Available: {', '.join(self.DOCS_URLS.keys())}")
            return None

        url = self.DOCS_URLS[format_type]
        archive_name = url.split("/")[-1]
        archive_path = self.output_dir / archive_name

        # Download
        print(f"\n{'='*60}")
        print(f"Python 3.14 Documentation Downloader")
        print(f"{'='*60}")
        print(f"Format: {format_type.upper()}")
        print(f"Source: {url}")
        print(f"Destination: {self.output_dir}")
        print(f"{'='*60}\n")

        if archive_path.exists():
            print(f"⚠️  Archive already exists: {archive_path}")
            response = input("   Re-download? (y/N): ").strip().lower()
            if response != "y":
                print("   Using existing archive...")
            else:
                if not self.download_file(url, archive_path):
                    return None
        else:
            if not self.download_file(url, archive_path):
                return None

        # Extract
        extract_dir = self.output_dir / f"python-3.14-docs-{format_type}"
        if extract_dir.exists():
            print(f"⚠️  Extraction directory exists: {extract_dir}")
            response = input("   Re-extract? (y/N): ").strip().lower()
            if response != "y":
                print("   Using existing documentation...")
                return extract_dir

        if not self.extract_tarball(archive_path, self.output_dir):
            return None

        # Cleanup archive (optional)
        cleanup = input("\n🗑️  Delete archive to save space? (y/N): ").strip().lower()
        if cleanup == "y":
            archive_path.unlink()
            print(f"   Deleted: {archive_path}")

        return extract_dir

    def verify_download(self, docs_path: Path) -> bool:
        """Verify downloaded documentation is complete"""
        if not docs_path.exists():
            print(f"❌ Documentation directory not found: {docs_path}")
            return False

        # Count files
        txt_files = list(docs_path.rglob("*.txt"))
        html_files = list(docs_path.rglob("*.html"))

        print(f"\n📊 Verification:")
        print(f"   Text files: {len(txt_files)}")
        print(f"   HTML files: {len(html_files)}")

        # Check for key directories
        expected_dirs = ["library", "reference", "tutorial", "c-api"]
        found_dirs = [d for d in expected_dirs if (docs_path / d).exists()]

        print(f"   Key directories: {len(found_dirs)}/{len(expected_dirs)}")

        if len(found_dirs) < len(expected_dirs):
            missing = set(expected_dirs) - set(found_dirs)
            print(f"   ⚠️  Missing: {', '.join(missing)}")
            return False

        print("   ✅ Documentation appears complete")
        return True


def main():
    """Main execution for documentation download"""
    # Determine AIOS root
    script_path = Path(__file__).resolve()
    aios_root = script_path.parent.parent.parent

    # Output directory for documentation
    docs_base = aios_root / "ai" / "docs" / "architecture"

    # Create downloader
    downloader = Python314DocsDownloader(docs_base)

    # Download text format (best for indexing)
    print("📚 Downloading Python 3.14 documentation (text format)...")
    print("   This is the best format for semantic indexing.\n")

    docs_path = downloader.download_docs(format_type="text")

    if docs_path:
        print(f"\n{'='*60}")
        print("✅ Download Complete!")
        print(f"{'='*60}")
        print(f"Documentation location: {docs_path}")

        # Verify
        if downloader.verify_download(docs_path):
            print("\n🎯 Next Steps:")
            print("   1. Run the knowledge indexer:")
            print("      python ai/tools/python314_knowledge_indexer.py")
            print("\n   2. Documentation will be indexed and ready for AIOS agents")
        else:
            print("\n⚠️  Verification failed. Manual inspection recommended.")

        return 0
    else:
        print("\n❌ Download failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

"""
Cache utility for storing and retrieving parsed documents.
"""
import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from pathlib import Path
from llama_index.core.schema import Document


class ParserCache:
    """Cache utility for parser responses."""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize parser cache.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different cache types
        self.documents_cache_dir = self.cache_dir / "documents"
        self.documents_cache_dir.mkdir(exist_ok=True)
        
        self.metadata_cache_dir = self.cache_dir / "metadata"
        self.metadata_cache_dir.mkdir(exist_ok=True)
    
    def _get_file_hash(self, file_path: str) -> str:
        """
        Generate a hash for the file based on path and modification time.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Hash string for the file
        """
        file_path = Path(file_path).resolve()
        stat = file_path.stat()
        
        # Create hash from file path and modification time
        hash_input = f"{file_path}_{stat.st_mtime}_{stat.st_size}"
        return hashlib.md5(hash_input.encode()).hexdigest()
    
    def _get_cache_path(self, file_path: str, parser_name: str) -> tuple[Path, Path]:
        """
        Get cache file paths for a given file and parser.
        
        Args:
            file_path: Path to the original file
            parser_name: Name of the parser
            
        Returns:
            Tuple of (markdown_cache_path, metadata_cache_path)
        """
        file_hash = self._get_file_hash(file_path)
        cache_filename = f"{parser_name}_{file_hash}"
        
        markdown_path = self.documents_cache_dir / f"{cache_filename}.md"
        metadata_path = self.metadata_cache_dir / f"{cache_filename}.json"
        
        return markdown_path, metadata_path
    
    def is_cached(self, file_path: str, parser_name: str) -> bool:
        """
        Check if a file is already cached.
        
        Args:
            file_path: Path to the file
            parser_name: Name of the parser
            
        Returns:
            True if cached, False otherwise
        """
        if not os.path.exists(file_path):
            return False
            
        documents_path, metadata_path = self._get_cache_path(file_path, parser_name)
        
        # Check if both cache files exist
        return documents_path.exists() and metadata_path.exists()
    
    def get_cached_markdown(self, file_path: str, parser_name: str) -> Optional[str]:
        """
        Retrieve cached markdown content.
        
        Args:
            file_path: Path to the file
            parser_name: Name of the parser
            
        Returns:
            Cached markdown content or None if not cached
        """
        if not self.is_cached(file_path, parser_name):
            return None
        
        try:
            markdown_path, _ = self._get_cache_path(file_path, parser_name)
            
            with open(markdown_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            return markdown_content
        except Exception as e:
            print(f"Error loading cached markdown: {e}")
            return None
    
    def cache_markdown(self, file_path: str, parser_name: str, markdown_content: str, 
                       metadata: Dict[str, Any] = None) -> bool:
        """
        Cache markdown content.
        
        Args:
            file_path: Path to the file
            parser_name: Name of the parser
            markdown_content: Markdown content to cache
            metadata: Additional metadata to cache
            
        Returns:
            True if successfully cached, False otherwise
        """
        try:
            markdown_path, metadata_path = self._get_cache_path(file_path, parser_name)
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            cache_metadata = {
                "file_path": file_path,
                "parser_name": parser_name,
                "cached_at": str(Path(file_path).stat().st_mtime),
                "content_length": len(markdown_content),
                "additional_metadata": metadata or {}
            }
            
            with open(metadata_path, 'w') as f:
                json.dump(cache_metadata, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error caching markdown: {e}")
            return False
    
    def clear_cache(self, file_path: str = None, parser_name: str = None) -> bool:
        """
        Clear cache for specific file/parser or entire cache.
        
        Args:
            file_path: Specific file to clear cache for (optional)
            parser_name: Specific parser to clear cache for (optional)
            
        Returns:
            True if successfully cleared, False otherwise
        """
        try:
            if file_path and parser_name:
                # Clear specific file/parser cache
                documents_path, metadata_path = self._get_cache_path(file_path, parser_name)
                
                if documents_path.exists():
                    documents_path.unlink()
                if metadata_path.exists():
                    metadata_path.unlink()
            else:
                # Clear entire cache
                import shutil
                if self.cache_dir.exists():
                    shutil.rmtree(self.cache_dir)
                    self.cache_dir.mkdir(exist_ok=True)
                    self.documents_cache_dir.mkdir(exist_ok=True)
                    self.metadata_cache_dir.mkdir(exist_ok=True)
            
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about cached files.
        
        Returns:
            Dictionary with cache information
        """
        cache_info = {
            "cache_dir": str(self.cache_dir),
            "cached_files": [],
            "total_size": 0
        }
        
        try:
            for markdown_file in self.documents_cache_dir.glob("*.md"):
                metadata_file = self.metadata_cache_dir / f"{markdown_file.stem}.json"
                
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    file_size = markdown_file.stat().st_size
                    cache_info["cached_files"].append({
                        "file_path": metadata.get("file_path"),
                        "parser_name": metadata.get("parser_name"),
                        "cached_at": metadata.get("cached_at"),
                        "content_length": metadata.get("content_length"),
                        "cache_size": file_size
                    })
                    cache_info["total_size"] += file_size
        except Exception as e:
            print(f"Error getting cache info: {e}")
        
        return cache_info

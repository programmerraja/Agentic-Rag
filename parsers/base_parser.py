"""
Base parser implementation.
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.interfaces.parser_interface import ParserInterface
from llama_index.core.schema import Document
from util.cache_util import ParserCache


class BaseParser(ParserInterface):
    """Base parser implementation with common functionality."""
    
    def __init__(self, enable_cache: bool = True, cache_dir: str = "cache", **kwargs):
        """
        Initialize base parser.
        
        Args:
            enable_cache: Enable caching functionality
            cache_dir: Directory to store cache files
            **kwargs: Additional configuration
        """
        self.config = kwargs
        self.enable_cache = enable_cache
        self.cache = ParserCache(cache_dir) if enable_cache else None
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate if the file can be parsed by this parser.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file can be parsed, False otherwise
        """
        if not os.path.exists(file_path):
            return False
        
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.get_supported_formats()
    
    def _create_document(self, content: str, metadata: Dict[str, Any] = None) -> Document:
        """
        Create a Document object with content and metadata.
        
        Args:
            content: Document content
            metadata: Document metadata
            
        Returns:
            Document object
        """
        if metadata is None:
            metadata = {}
        
        return Document(
            text=content,
            metadata=metadata
        )
    
    def _get_cached_markdown(self, file_path: str) -> Optional[str]:
        """
        Get cached markdown content if available.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Cached markdown content or None if not cached
        """
        if not self.enable_cache or not self.cache:
            return None
        
        return self.cache.get_cached_markdown(file_path, self.get_parser_name())
    
    def _cache_markdown(self, file_path: str, markdown_content: str, 
                       metadata: Dict[str, Any] = None) -> bool:
        """
        Cache markdown content.
        
        Args:
            file_path: Path to the file
            markdown_content: Markdown content to cache
            metadata: Additional metadata to cache
            
        Returns:
            True if successfully cached, False otherwise
        """
        if not self.enable_cache or not self.cache:
            return False
        
        return self.cache.cache_markdown(file_path, self.get_parser_name(), markdown_content, metadata)
    
    def _is_cached(self, file_path: str) -> bool:
        """
        Check if file is already cached.
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if cached, False otherwise
        """
        if not self.enable_cache or not self.cache:
            return False
        
        return self.cache.is_cached(file_path, self.get_parser_name())
    
    def clear_cache(self, file_path: str = None) -> bool:
        """
        Clear cache for this parser.
        
        Args:
            file_path: Specific file to clear cache for (optional)
            
        Returns:
            True if successfully cleared, False otherwise
        """
        if not self.enable_cache or not self.cache:
            return False
        
        return self.cache.clear_cache(file_path, self.get_parser_name())
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get cache information for this parser.
        
        Returns:
            Dictionary with cache information
        """
        if not self.enable_cache or not self.cache:
            return {"enabled": False}
        
        cache_info = self.cache.get_cache_info()
        cache_info["parser_name"] = self.get_parser_name()
        cache_info["enabled"] = True
        
        # Filter to only show files parsed by this parser
        if "cached_files" in cache_info:
            cache_info["cached_files"] = [
                file_info for file_info in cache_info["cached_files"]
                if file_info.get("parser_name") == self.get_parser_name()
            ]
        
        return cache_info

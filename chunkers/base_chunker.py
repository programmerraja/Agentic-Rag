"""
Base chunker implementation.
"""
from typing import List, Dict, Any
from core.interfaces.chunker_interface import ChunkerInterface
from llama_index.core.schema import Document, BaseNode


class BaseChunker(ChunkerInterface):
    """Base chunker implementation with common functionality."""
    
    def __init__(self, **kwargs):
        """Initialize base chunker."""
        self.config = kwargs
    
    def get_chunking_config(self) -> Dict[str, Any]:
        """Get current chunking configuration."""
        return self.config.copy()
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update chunking configuration."""
        self.config.update(config)

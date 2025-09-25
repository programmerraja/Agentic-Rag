"""
Chunker interface for document chunking strategies.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from llama_index.core.schema import Document, BaseNode


class ChunkerInterface(ABC):
    """Abstract base class for document chunkers."""
    
    @abstractmethod
    def chunk(self, documents: List[Document], **kwargs) -> List[BaseNode]:
        """
        Chunk documents into nodes.
        
        Args:
            documents: List of documents to chunk
            **kwargs: Additional chunking options
            
        Returns:
            List of chunked nodes
        """
        pass
    
    @abstractmethod
    def get_chunking_strategy(self) -> str:
        """
        Get the name of the chunking strategy.
        
        Returns:
            Chunking strategy name
        """
        pass
    
    @abstractmethod
    def get_chunking_config(self) -> Dict[str, Any]:
        """
        Get the current chunking configuration.
        
        Returns:
            Dictionary of chunking configuration parameters
        """
        pass
    
    @abstractmethod
    def update_config(self, config: Dict[str, Any]) -> None:
        """
        Update chunking configuration.
        
        Args:
            config: New configuration parameters
        """
        pass

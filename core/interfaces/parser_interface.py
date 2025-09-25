"""
Parser interface for document processing.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from llama_index.core.schema import Document


class ParserInterface(ABC):
    """Abstract base class for document parsers."""
    
    @abstractmethod
    def parse(self, file_path: {str, str}, **kwargs) -> List[Document]:
        """
        Parse a document and return a list of Document objects.
        
        Args:
            file_path: Path to the document to parse
            **kwargs: Additional parsing options
            
        Returns:
            List of Document objects
        """
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported file formats.
        
        Returns:
            List of supported file extensions
        """
        pass
    
    @abstractmethod
    def get_parser_name(self) -> str:
        """
        Get the name of this parser.
        
        Returns:
            Parser name
        """
        pass
    
    @abstractmethod
    def validate_file(self, file_path: str) -> bool:
        """
        Validate if the file can be parsed by this parser.
        
        Args:
            file_path: Path to the file to validate
            
        Returns:
            True if file can be parsed, False otherwise
        """
        pass

"""
Hierarchical chunker implementation.
"""
from typing import List, Dict, Any
from llama_index.core.schema import Document, BaseNode
from llama_index.core.node_parser import HierarchicalNodeParser
from chunkers.base_chunker import BaseChunker


class HierarchicalChunker(BaseChunker):
    """Hierarchical chunker creating multi-level document hierarchy."""
    
    def __init__(self, chunk_sizes: List[int] = [1536, 512, 128], **kwargs):
        """
        Initialize hierarchical chunker.
        
        Args:
            chunk_sizes: List of chunk sizes for each level
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.chunk_sizes = chunk_sizes
        self._parser = None
    
    def _get_parser(self) -> HierarchicalNodeParser:
        """Get or create hierarchical node parser."""
        if self._parser is None:
            self._parser = HierarchicalNodeParser.from_defaults(
                chunk_sizes=self.chunk_sizes
            )
        return self._parser
    
    def chunk(self, documents: List[Document], **kwargs) -> List[BaseNode]:
        """
        Chunk documents using hierarchical splitting.
        
        Args:
            documents: List of documents to chunk
            **kwargs: Additional chunking options
            
        Returns:
            List of chunked nodes
        """
        parser = self._get_parser()
        
        try:
            nodes = parser.get_nodes_from_documents(documents)
            
            # Add chunking metadata to each node
            for node in nodes:
                if not hasattr(node, 'metadata'):
                    node.metadata = {}
                node.metadata.update({
                    "chunker": "hierarchical",
                })
            
            return nodes
            
        except Exception as e:
            raise RuntimeError(f"Failed to chunk documents with hierarchical chunker: {str(e)}")
    
    def _get_node_level(self, node: BaseNode) -> int:
        """Determine the level of a hierarchical node."""
        # This is a simplified approach - in practice, you might need
        # to track the level more precisely during chunking
        if hasattr(node, 'metadata') and 'level' in node.metadata:
            return node.metadata['level']
        
        # Estimate level based on text length
        text_length = len(node.text)
        for i, chunk_size in enumerate(self.chunk_sizes):
            if text_length <= chunk_size:
                return i
        return len(self.chunk_sizes) - 1
    
    def get_chunking_strategy(self) -> str:
        """Get chunking strategy name."""
        return "hierarchical"
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update chunking configuration."""
        super().update_config(config)
        
        if "chunk_sizes" in config:
            self.chunk_sizes = config["chunk_sizes"]
            # Reset parser to use new chunk sizes
            self._parser = None

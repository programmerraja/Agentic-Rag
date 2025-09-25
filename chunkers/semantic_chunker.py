"""
Semantic chunker implementation.
"""
from typing import List, Dict, Any
from llama_index.core.schema import Document, BaseNode
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings
from chunkers.base_chunker import BaseChunker


class SemanticChunker(BaseChunker):
    """Semantic chunker using semantic similarity for intelligent splitting."""
    
    def __init__(self, buffer_size: int = 1, threshold: float = 0.75, 
                 embed_model_name: str = "BAAI/bge-small-en-v1.5", **kwargs):
        """
        Initialize semantic chunker.
        
        Args:
            buffer_size: Buffer size for semantic splitting
            threshold: Threshold for semantic similarity
            embed_model_name: Name of the embedding model
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.buffer_size = buffer_size
        self.threshold = threshold
        self.embed_model_name = embed_model_name
        self._embed_model = None
        self._splitter = None
    
    def _get_embed_model(self) -> FastEmbedEmbedding:
        """Get or create embedding model."""
        if self._embed_model is None:
            self._embed_model = FastEmbedEmbedding(model_name=self.embed_model_name)
            Settings.embed_model = self._embed_model
        return self._embed_model
    
    def _get_splitter(self) -> SemanticSplitterNodeParser:
        """Get or create semantic splitter."""
        if self._splitter is None:
            embed_model = self._get_embed_model()
            self._splitter = SemanticSplitterNodeParser(
                buffer_size=self.buffer_size,
                breakpoint_percentile_threshold=self.threshold,
                embed_model=embed_model,
            )
        return self._splitter
    
    def chunk(self, documents: List[Document], **kwargs) -> List[BaseNode]:
        """
        Chunk documents using semantic splitting.
        
        Args:
            documents: List of documents to chunk
            **kwargs: Additional chunking options
            
        Returns:
            List of chunked nodes
        """
        splitter = self._get_splitter()
        
        try:
            nodes = splitter.get_nodes_from_documents(documents)
            
            # Add chunking metadata to each node
            for node in nodes:
                if not hasattr(node, 'metadata'):
                    node.metadata = {}
                node.metadata.update({
                    "chunker": "semantic",
                    "buffer_size": self.buffer_size,
                    "threshold": self.threshold,
                    "embed_model": self.embed_model_name
                })
            
            return nodes
            
        except Exception as e:
            raise RuntimeError(f"Failed to chunk documents with semantic chunker: {str(e)}")
    
    def get_chunking_strategy(self) -> str:
        """Get chunking strategy name."""
        return "semantic"
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update chunking configuration."""
        super().update_config(config)
        
        if "buffer_size" in config:
            self.buffer_size = config["buffer_size"]
        if "threshold" in config:
            self.threshold = config["threshold"]
        if "embed_model_name" in config:
            self.embed_model_name = config["embed_model_name"]
            # Reset embed model to use new name
            self._embed_model = None
            self._splitter = None

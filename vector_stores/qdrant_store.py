"""
Qdrant vector store implementation.
"""

from typing import List, Dict, Any, Optional
import qdrant_client
from qdrant_client.http import models as rest
from llama_index.core.schema import BaseNode, NodeWithScore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from vector_stores.base_vector_store import BaseVectorStore
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
import logging

logger = logging.getLogger(__name__)


class QdrantStore(BaseVectorStore):
    """Qdrant vector store implementation."""

    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection_name: str = "documents",
        api_key: str = "",
        enable_hybrid: bool = True,
        batch_size: int = 64,
        parallel: int = 1,
        embed_model_name: str = "BAAI/bge-small-en-v1.5",
        **kwargs,
    ):
        """
        Initialize Qdrant vector store.

        Args:
            url: Qdrant server URL
            collection_name: Collection name
            api_key: API key for authentication
            enable_hybrid: Enable hybrid search
            batch_size: Batch size for operations
            parallel: Number of parallel operations
            embed_model_name: Embedding model name for FastEmbed
            **kwargs: Additional configuration
        """
        super().__init__(**kwargs)
        self.url = url
        self.collection_name = collection_name
        self.api_key = api_key
        self.enable_hybrid = enable_hybrid
        self.batch_size = batch_size
        self.parallel = parallel
        self.embed_model_name = embed_model_name
        self._client = None
        self._vector_store = None
        self._embed_model = None
        self._index = None

    def _initialize(self) -> None:
        """Initialize Qdrant client and vector store."""
        try:
            # Create embedding model
            self._embed_model = FastEmbedEmbedding(model_name=self.embed_model_name)

            # Create Qdrant client
            self._client = qdrant_client.QdrantClient(
                url=self.url, api_key=self.api_key if self.api_key else None
            )

            # Create vector store
            self._vector_store = QdrantVectorStore(
                client=self._client,
                collection_name=self.collection_name,
                enable_hybrid=self.enable_hybrid,
                batch_size=self.batch_size,
                parallel=self.parallel,
            )

            # Set up storage context and index
            storage_context = StorageContext.from_defaults(
                vector_store=self._vector_store
            )
            Settings.embed_model = self._embed_model
            self._index = VectorStoreIndex.from_vector_store(
                vector_store=self._vector_store, storage_context=storage_context
            )

        except Exception as e:
            raise RuntimeError(f"Failed to initialize Qdrant vector store: {str(e)}")

    def add(self, nodes: List[BaseNode], **kwargs) -> List[str]:
        """
        Add nodes to the vector store.

        Args:
            nodes: List of nodes to add
            **kwargs: Additional storage options

        Returns:
            List of node IDs that were added
        """
        self._ensure_initialized()

        try:
            for node in nodes:
                if not hasattr(node, "embedding") or node.embedding is None:
                    node.embedding = self._embed_model.get_text_embedding(
                        node.get_content()
                    )

            # Add to vector store
            node_ids = self._vector_store.add(nodes, **kwargs)

            # Update the index with new nodes
            if self._index is not None:
                self._index.insert_nodes(nodes)

            return node_ids
        except Exception as e:
            raise RuntimeError(f"Failed to add nodes to Qdrant: {str(e)}")

    def search(
        self, query: str, top_k: int = 5, plan_name: str = None, **kwargs
    ) -> List[NodeWithScore]:
        """
        Search for similar nodes using retriever pattern.

        Args:
            query: Search query
            top_k: Number of results to return
            **kwargs: Additional search options

        Returns:
            List of nodes with similarity scores
        """
        self._ensure_initialized()

        try:
            filters = MetadataFilters(
                filters=[
                    MetadataFilter(
                        key="plan_name", value=plan_name, operator=FilterOperator.EQ
                    ),
                ]
            )

            retriever = self._index.as_retriever(
                similarity_top_k=top_k, filters=filters
            )
            nodes_with_scores = retriever.retrieve(query)
            return nodes_with_scores
        except Exception as e:
            logger.error(f"Failed to search in Qdrant: {str(e)}")
            raise RuntimeError(f"Failed to search in Qdrant: {str(e)}")

    def get_retriever(self, similarity_top_k: int = 5, **kwargs):
        """
        Get a retriever for the vector store.

        Args:
            similarity_top_k: Number of results to return
            **kwargs: Additional retriever options

        Returns:
            Retriever object
        """
        self._ensure_initialized()
        return self._index.as_retriever(similarity_top_k=similarity_top_k, **kwargs)

    def delete(self, node_ids: List[str]) -> bool:
        """
        Delete nodes by their IDs.

        Args:
            node_ids: List of node IDs to delete

        Returns:
            True if deletion was successful
        """
        self._ensure_initialized()

        try:
            self._client.delete(
                collection_name=self.collection_name,
                points_selector=rest.PointIdsList(points=node_ids),
            )
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to delete nodes from Qdrant: {str(e)}")

    def get_store_name(self) -> str:
        """Get vector store name."""
        return "QdrantStore"

    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information."""
        info = super().get_collection_info()
        info.update(
            {
                "url": self.url,
                "collection_name": self.collection_name,
                "enable_hybrid": self.enable_hybrid,
                "batch_size": self.batch_size,
                "parallel": self.parallel,
            }
        )
        return info

    def clear_collection(self) -> bool:
        """
        Clear all data from the collection.

        Returns:
            True if clearing was successful
        """
        self._ensure_initialized()

        try:
            self._client.delete_collection(collection_name=self.collection_name)
            # Recreate the collection
            self._initialize()
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to clear Qdrant collection: {str(e)}")

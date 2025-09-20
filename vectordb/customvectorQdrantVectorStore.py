
from typing import List, Any
from llama_index.core.schema import TextNode
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client.http import models as rest


class CustomQdrantVectorStore(QdrantVectorStore):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _build_points(
        self, nodes: List[TextNode], sparse_vector_name: str
    ) -> tuple[List[Any], List[str]]:
        points = []
        ids = []

        for node in nodes:
            node_id = node.node_id

            minimal_metadata = {
                "id": "",
                "mimetype": node.mimetype,
            }

            payload = {
                self.text_key: node.get_content(metadata_mode="none"),
                **minimal_metadata,
            }

            vector_data = {self.dense_vector_name: node.get_embedding()}

            point = rest.PointStruct(id=node_id, payload=payload, vector=vector_data)

            points.append(point)
            ids.append(node_id)

        return points, ids

    def add(self, nodes: List[TextNode], **add_kwargs: Any) -> List[str]:
        if len(nodes) > 0 and not self._collection_initialized:
            self._create_collection(
                collection_name=self.collection_name,
                vector_size=len(nodes[0].get_embedding()),
            )

        if self._collection_initialized and self._legacy_vector_format is None:
            self._detect_vector_format(self.collection_name)

        points, ids = self._build_points(nodes, self.sparse_vector_name)

        self._client.upload_points(
            collection_name=self.collection_name,
            points=points,
            batch_size=self.batch_size,
            parallel=self.parallel,
            max_retries=self.max_retries,
            wait=True,
        )

        return ids


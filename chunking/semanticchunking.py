"""
Semantic chunking using SemanticSplitterNodeParser in LlamaIndex works by splitting documents based on semantic similarity rather than fixed chunk sizes. It uses embeddings to identify natural breakpoints in the content where the semantic meaning changes significantly.

The semantic splitter:
- Analyzes the semantic similarity between consecutive sentences/paragraphs
- Creates chunks at natural semantic boundaries
- Preserves context and meaning within each chunk
- Uses a threshold to determine when to split content

This approach is more intelligent than fixed-size chunking as it respects the natural flow of information.
"""

from llama_index.core import Document, VectorStoreIndex, StorageContext, Settings
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.readers.file import PDFReader

import qdrant_client


# Create semantic splitter with custom parameters
semantic_splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=0.75,
    embed_model=None,  # Will be set after embedding model is initialized
)

# Load documents
documents = PDFReader().load_data(file="../documents/Imperial Dynamic Plan (HMO) 012-8-18.pdf")

# Setup vector store
vector_store = QdrantVectorStore(
    client=qdrant_client.QdrantClient(url="http://localhost:6333", api_key=""),
    collection_name="semantic_chunks",
    enable_hybrid=True,
    batch_size=64,
    parallel=1,
)   

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create semantic chunks
nodes = semantic_splitter.get_nodes_from_documents(documents)

# Setup embedding model
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.embed_model = embed_model

semantic_splitter = SemanticSplitterNodeParser(
    buffer_size=1,
    breakpoint_percentile_threshold=0.75,
    embed_model=embed_model,
)

nodes = semantic_splitter.get_nodes_from_documents(documents)

index = VectorStoreIndex(
    nodes=nodes,
    storage_context=storage_context,
    show_progress=True,
    insert_batch_size=64,
)

# Example query
# retriever = index.as_retriever(similarity_top_k=5)
# nodes_with_scores = retriever.retrieve("What is the insurance plan for family health?")

# for node in nodes_with_scores:
#     print(node.text)
#     print(node.metadata)

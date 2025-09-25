

"""
The HierarchicalNodeParser in LlamaIndex works by splitting a document into a recursive hierarchy of nodes (chunks) using one or more NodeParsers with specified chunk sizes at different levels. It constructs a multi-layer hierarchy where:

Top-level nodes represent large chunks with a big chunk size (e.g., 2048 tokens)

Second-level nodes break down those top nodes into smaller child nodes (e.g., 512 tokens)

Third-level nodes further decompose the second-level nodes into even smaller chunks (e.g., 128 tokens)

This hierarchical relationship preserves document structure and content context across layers.


Document
 ├─ Level 1 (512 chars) → big section
 │    ├─ Level 2 (256 chars) → paragraph
 │    │    ├─ Level 3 (128 chars) → sentence
 │    │    └─ Level 3 (128 chars) → sentence
 │    └─ Level 2 (256 chars) → paragraph
 │         └─ Level 3 (128 chars) → sentence
 └─ Level 1 (512 chars) → another section


So basically we have 3 levels of chunks:
 `Assume this is the text we are parsing:`
    level1 -> Assume this is the text we are parsing:
    level 2 -> assume this , is the text , we are parsing 
    level 3 -> assume, this, is the, text, we are parsing

SO we split same text in 3  differnt levels
"""

# from llama_index.core import Document
from llama_index.core.node_parser import HierarchicalNodeParser
# from llama_index.node_parser.docling import DoclingNodeParser
# from customvectorQdrantVectorStore import CustomQdrantVectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore

from llama_index.readers.file import PDFReader
import qdrant_client
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.embeddings.fastembed import FastEmbedEmbedding
from llama_index.core import Settings

node_parser = HierarchicalNodeParser.from_defaults(chunk_sizes=[1536, 512, 128])

# docling_node_parser = DoclingNodeParser()

# documents = PDFReader().load_data(file="../documents/Family Health Optima Insurance Plan.pdf")

vector_store = QdrantVectorStore(
    client=qdrant_client.QdrantClient(url="http://localhost:6333", api_key=""),
    collection_name="documents",
    enable_hybrid=True,
    batch_size=64,
    parallel=1,
)   

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# nodes = node_parser.get_nodes_from_documents(documents)

# docling_nodes = docling_node_parser.get_nodes_from_documents(documents)


embed_model = FastEmbedEmbedding(model_name="BAAI/bge-small-en-v1.5")

Settings.embed_model = embed_model

index = VectorStoreIndex(
    nodes=[],
    storage_context=storage_context,
    show_progress=True,
    insert_batch_size=64,
)

retriever = index.as_retriever(similarity_top_k=5)

nodes_with_scores = retriever.retrieve("What is the best health insurance policy for me?")

for node in nodes_with_scores:
    print(node.text)
    print(node.metadata)
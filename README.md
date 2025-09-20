# Agentic-Rag
A MultiAgent setup for Agentic RAG



Need to be generic tell about your bussiness we will genereate a systemPrompt and extract the data and RAG.

- A multiagent to anayslis the problem for agentic RAG.




TO run qdrant:

docker run \
  -p 6333:6333 \
  -p 6334:6334 \
  --memory=2048mb \
  -v qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest


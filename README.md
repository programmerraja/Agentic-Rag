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





A agent will indetify the user intent ask clarify question if the question not clear mean else split the question in two sub if it is complex
else it will do simple RAG and find the solution 

A orchsiter agent must need to have the domain knoweldege about problem we are solving.

if it is complex
    - split and assign the task to multiple agent who has tool attached
    - collect response from them and answer the question 
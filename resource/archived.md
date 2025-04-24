sentence-transformers → embedding model (text → vector)
faiss → vector database (stores/searches those vectors)

Provider	Description
✅ Sentence Transformers	Open-source, local embedding via sentence-transformers (e.g., all-MiniLM-L6-v2)
🆕 OpenAI Embeddings	Uses text-embedding-ada-002 or similar via OpenAI API
🆕 Cohere Embeddings	Paid embeddings with domain-tuned support
🆕 Hugging Face Hub	Any hosted model with embedding support
🆕 Gemini Embeddings	If Google provides API access (future-proofing)



Provider	Description
✅ FAISS	Local, in-memory and on-disk vector DB. Great for development & small data
🆕 Chroma DB	Local/remote open-source vector store with metadata, filtering, persistence
🆕 Weaviate	Open-source, GraphQL interface, scale-friendly
🆕 Pinecone	Managed vector DB, scalable, filterable, metadata support
🆕 Qdrant	Similar to Pinecone, open-source option
🆕 Milvus	Highly scalable open-source vector DB

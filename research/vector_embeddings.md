# Vector Embeddings — Day 17

## What are Vector Embeddings?
- Text converted to numbers (arrays of floats)
- Similar meaning = similar numbers
- Used for semantic search (search by meaning, not exact words)

## Example:
- "I love Python programming" → [0.2, 0.8, 0.5, 0.9, 0.1, ...]
- "coding in Python is fun"  → [0.3, 0.7, 0.6, 0.8, 0.2, ...]
- "I ate pizza for lunch"    → [0.9, 0.1, 0.2, 0.1, 0.8, ...]

First two sentences have SIMILAR numbers (both about Python/coding)
Third sentence has DIFFERENT numbers (about food)

## How ChromaDB Works:
1. You give it text → it converts to vectors (embeddings)
2. Vectors are stored in a database
3. When you search → your query is also converted to vector
4. ChromaDB finds vectors closest to your query
5. Returns the most similar texts

## Why ChromaDB for Spidey?
- Find past conversations by MEANING
- "What did we talk about coding?" → finds Python chats
- "Any health tips?" → finds fitness/health conversations
- Much smarter than LIKE '%word%' SQL search

## ChromaDB Key Concepts:
- **Collection**: Like a table (group of documents)
- **Document**: The text you store
- **Embedding**: The vector representation
- **Metadata**: Extra info (timestamp, category, etc.)
- **Query**: Search by similarity
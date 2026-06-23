"""
Practice Script: ChromaDB Basics
"""
import chromadb
import shutil
import os

print("=== ChromaDB Basics ===\n")

test_dir = "data/chroma_practice"
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)

client = chromadb.PersistentClient(path=test_dir)

print("1. Creating collection...")
collection = client.get_or_create_collection(name="my_documents")
print("   ✅ Collection created!\n")

print("2. Adding documents...")
collection.add(
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"],
    documents=[
        "Python is a great programming language for beginners",
        "Machine learning uses data to train AI models",
        "I love eating pizza and pasta for dinner",
        "JavaScript is used for building websites",
        "The gym is a great place for exercise and fitness"
    ],
    metadatas=[
        {"category": "coding"},
        {"category": "AI"},
        {"category": "food"},
        {"category": "coding"},
        {"category": "health"}
    ]
)
print("   ✅ 5 documents added!\n")

print("3. Semantic Search Examples:\n")

print("   🔍 Search: 'coding tutorials'")
results = collection.query(query_texts=["coding tutorials"], n_results=3)
for i, doc in enumerate(results["documents"][0]):
    distance = round(results["distances"][0][i], 3)
    print(f"      {i+1}. {doc[:50]}... (distance: {distance})")

print()

print("   🔍 Search: 'healthy lifestyle'")
results = collection.query(query_texts=["healthy lifestyle"], n_results=3)
for i, doc in enumerate(results["documents"][0]):
    distance = round(results["distances"][0][i], 3)
    print(f"      {i+1}. {doc[:50]}... (distance: {distance})")

print()

print("   🔍 Search: 'Italian food'")
results = collection.query(query_texts=["Italian food"], n_results=3)
for i, doc in enumerate(results["documents"][0]):
    distance = round(results["distances"][0][i], 3)
    print(f"      {i+1}. {doc[:50]}... (distance: {distance})")

print()

print("   🔍 Search: 'artificial intelligence'")
results = collection.query(query_texts=["artificial intelligence"], n_results=3)
for i, doc in enumerate(results["documents"][0]):
    distance = round(results["distances"][0][i], 3)
    print(f"      {i+1}. {doc[:50]}... (distance: {distance})")

print()
print(f"4. Total documents: {collection.count()}")

shutil.rmtree(test_dir)
print("\n✅ ChromaDB basics learned!")
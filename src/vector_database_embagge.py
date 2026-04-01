from chromadb import PersistentClient
import os
import uuid

def get_collection():
    return collection

# Create the vect database
client = PersistentClient(path="./vectorial_database")
collection = client.get_or_create_collection(name="python-lib-collection")

if __name__ == "__main__":
    print("creating or geting the vectorial database")

# Populate the Vect Database
for archive in os.listdir("docs/langgraph"):
    with open(f"docs/langgraph/{archive}", "r", encoding="utf-8") as f:
        content: list[str] = f.read().splitlines() # pega cada linha 
    
    collection.add(
        ids=[str(uuid.uuid4()) for _ in content],
        documents=content,
        metadatas=[{
            "line": line,
            "archive_content": archive
        } for line in range(len(content))]
    )

if __name__ == "__main__":
    print("database vector was build or alredy exists")
    print(collection.peek())

    print("test if the database is correpondenting:")

    results = collection.query(
        query_texts=[
            "How can i install the langgraph lib?",
            "where is the local server?"
        ],
        n_results=5,
    )

    for i, r in enumerate(results["documents"]):
        print(f"\nquery {i}:")
        print("\n".join(r))



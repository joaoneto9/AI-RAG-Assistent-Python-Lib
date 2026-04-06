import sys

from chromadb import Collection, PersistentClient
import os
import uuid

def get_collection() -> Collection:
    return collection

def split_themes_readme_files(text: str) -> list[str]:
    """
    Divide o texto do README em blocos baseados em títulos (hashtags),
    ignorando blocos de código (CodeGroup).
    """
    lines = text.splitlines()
    blocks = []
    current_block = []
    
    is_in_code_group = False
    
    for line in lines:
        if "<CodeGroup>" in line:
            is_in_code_group = True
        
        if line.strip().startswith("#") and not is_in_code_group:
            if current_block:
                blocks.append("\n".join(current_block))
            current_block = [line]
        else:
            current_block.append(line)
            
        if "</CodeGroup>" in line:
            is_in_code_group = False
            
    if current_block:
        blocks.append("\n".join(current_block))
    
    return blocks

# Create the vect database
client = PersistentClient(path="./vectorial_database")

if len(sys.argv) < 2: # se nao tiver parametro -> pega o ja existente
    collection = client.get_or_create_collection(name="python-lib-collection")
else:
    try:
        client.delete_collection(name="python-lib-collection")
    except ValueError:
        pass

    collection = client.create_collection(name="python-lib-collection")

    # Populate the Vect Database
    for archive in os.listdir("docs/langgraph"):
        with open(f"docs/langgraph/{archive}", "r", encoding="utf-8") as f:
            content: list[str] = split_themes_readme_files(f.read())
        
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
            "how can i install langgraph?"
        ],
        n_results=5,
    )

    for i, r in enumerate(results["documents"]):
        print(f"\nquery {i}:")
        print("\n".join(r))



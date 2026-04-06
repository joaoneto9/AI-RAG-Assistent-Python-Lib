import sys

from chromadb import PersistentClient
import os
import uuid

def get_collection():
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
        # Detecta limites do CodeGroup
        if "<CodeGroup>" in line:
            is_in_code_group = True
        
        # Se for um título (e não estamos dentro de um CodeGroup), 
        # significa que um novo bloco começou.
        if line.strip().startswith("#") and not is_in_code_group:
            if current_block:
                blocks.append("\n".join(current_block))
            current_block = [line]
        else:
            current_block.append(line)
            
        # Detecta o fechamento após processar a linha para incluir a tag no bloco
        if "</CodeGroup>" in line:
            is_in_code_group = False
            
    # Adiciona o último bloco acumulado
    if current_block:
        blocks.append("\n".join(current_block))
    
    return blocks

# Create the vect database
client = PersistentClient(path="./vectorial_database")

if len(sys.argv) < 2: # se nao tiver parametro -> pega o ja existente
    print("poegando o collection que ja existe")
    collection = client.get_or_create_collection(name="python-lib-collection")
else:
    print("Recriando a collection")
    # Deleta a collection se ela existir para garantir uma criação limpa
    try:
        client.delete_collection(name="python-lib-collection")
    except ValueError:
        # Caso a collection não exista, o Chroma pode lançar um erro; 
        # o try-except evita que o script pare.
        pass

# if __name__ == "__main__":
#     print("creating or geting the vectorial database")

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
            "How can i install the langgraph lib?",
            "where is the local server?"
        ],
        n_results=5,
    )

    for i, r in enumerate(results["documents"]):
        print(f"\nquery {i}:")
        print("\n".join(r))



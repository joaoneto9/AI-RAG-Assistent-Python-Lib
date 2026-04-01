from chromadb import PersistentClient

# Create the vect database

client = PersistentClient(path="./vectorial_database")

collection = client.get_or_create_collection(name="python-lib-collection")

print("creating or geting the vectorial database")

# Populate the Vect Database

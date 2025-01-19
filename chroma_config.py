import chromadb

def connect_chroma():
    return chromadb.PersistentClient('vector_db')
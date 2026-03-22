from langchain_community.vectorstores import Chroma

PERSIST_DIR = "./chroma_db"

def create_vectorstore(chunks, embeddings):
    return Chroma.from_texts(
        chunks,
        embeddings,
        persist_directory=PERSIST_DIR
    )

def load_vectorstore(embeddings):
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k": 3})
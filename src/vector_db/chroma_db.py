from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class ChromaDB:
    def __init__(self, persist_directory: str, embedding_model: str = "nomic-embed-text"):
        self.persist_directory = persist_directory
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.vectorstore = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def chunk_and_store_logs(self, orn: str, log_text: str, log_type: str, status: str = None, timestamp: str = None, chunk_size: int = 512, chunk_overlap: int = 50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunks = splitter.split_text(log_text)
        metadatas = [{
            "orn": orn,
            "log_type": log_type,
            "chunk_index": i,
            "status": status,
            "timestamp": timestamp
        } for i in range(len(chunks))]
        ids = [f"{orn}_{log_type}_{i}" for i in range(len(chunks))]
        self.vectorstore.add_texts(texts=chunks, metadatas=metadatas, ids=ids)
        self.vectorstore.persist()

    def similarity_search(self, query: str, k: int = 5):
        return self.vectorstore.similarity_search(query, k=k)

    def delete_orn(self, orn: str):
        # Remove all chunks for a given ORN
        all_ids = [doc.metadata["id"] for doc in self.vectorstore.get()['documents'] if doc.metadata.get("orn") == orn]
        self.vectorstore.delete(ids=all_ids)
        self.vectorstore.persist()

    def metadata_search(self, orn: str, log_type: str = None, k: int = 5):
        return self.get_all_by_metadata(orn=orn, log_type=log_type, k=k)

    def get_all_by_metadata(self, orn: str = None, log_type: str = None, k: int = 1000):
        # Build filter dict for metadata search using Chroma's expected format
        filter_dict = {}
        print(f"Building filter dict for metadata search: {orn}, {log_type}")
        if orn and log_type:
            filter_dict = {"$and": [{"orn": {"$eq": orn}}, {"log_type": {"$eq": log_type}}]}
        elif orn:
            filter_dict = {"orn": {"$eq": orn}}
        elif log_type:
            filter_dict = {"log_type": {"$eq": log_type}}
        else:
            filter_dict = None
        return self.vectorstore.search(
            query="*",  # Dummy query string
            search_type="similarity",
            filter=filter_dict,
            k=k
        )
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import ollama
from config import EMBEDDING_MODEL


class VectorStore:
    def __init__(self, persist_path="data/embeddings", collection_name="nepistory"):
        ollama.pull(EMBEDDING_MODEL)
        self.persist_path = persist_path
        self.collection_name = collection_name
        self.embedding_function = OllamaEmbeddings(model=EMBEDDING_MODEL)
        self.db = Chroma(persist_directory=persist_path,
                        embedding_function=self.embedding_function,
                        collection_name=collection_name)
    
    def get_db(self):
        return self.db
            
    def document_exists(self, source):
        result = self.db._collection.get(
            where={"source": source}
        )
        return len(result['ids']) > 0
    
    def add_document(self, source, documents):
        for doc in documents:
            if 'metadata' in doc:
                doc.metadata['source'] = source
            else:
                doc.metadata = {'source': source}
        
        ids = self.db.add_documents(documents=documents)
        print(ids)
        return ids
    
    def clear_store(self):
        self.db.delete_collection()
        self.db = Chroma(persist_directory=self.persist_path,
                        embedding_function=OllamaEmbeddings(model=EMBEDDING_MODEL),
                        collection_name=self.collection_name)
        print("Store cleared")
    
    def remove_document(self, source):
        self.db._collection.delete(
            where={"source": source}
        )
        print(f"Document {source} removed")

    def get_similar_documents(self, query, top_k=5):
        result = self.db.search(query, search_type="similarity", k=top_k)
        return result

vector_store = VectorStore()


if __name__ == "__main__":
    vector_store.clear_store()
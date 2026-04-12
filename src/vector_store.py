from sentence_transformers import SentenceTransformer
import pandas as pd
from google.cloud import aiplatform
from config import settings
class VectorStore:
    def __init__(self, source='data/embeddings/nepali-history.json'):
        self.df = pd.read_json(source, lines=True, orient='records')
        
        aiplatform.init(
            project=settings.PROJECT_ID,
            location=settings.LOCATION
        )
        self.index = aiplatform.MatchingEngineIndex(
            settings.INDEX_ID
        )
        self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(
            settings.INDEX_ENDPOINT_ID
        )
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def __len__(self):
        return len(self.df)

    def get_document_by_id(self, idx):
        return self.df[self.df['ids'] == idx].iloc[0]['documents']

    def get_document_by_ids(self, ids):
        return self.df[self.df['ids'].isin(ids)]['documents'].to_list()
    
    def get_embeddings(self, text):
        return self.model.encode(str(text)).tolist()
    
    def get_similar_documents(self, query, k=50):
        query_embedding = self.get_embeddings(query)
        response = self.index_endpoint.find_neighbors(
            deployed_index_id=settings.DEPLOYED_INDEX_ID,
            queries=[query_embedding],
            num_neighbors=k
        )
        ids = [resp.id for resp in response[0] if resp.distance > 0.6]
        return self.get_document_by_ids(ids)
    
    def add_new_source(self, source):
        pass

    def remove_source(self, source):
        pass

    def get_random_document(self):
        randomly_selected = self.df.sample(1)
        return randomly_selected.iloc[0]

store = VectorStore()

if __name__ == "__main__":
    a = VectorStore()
    doc = a.get_random_document()
    docs = a.get_similar_documents(doc['documents'])
    print(docs)
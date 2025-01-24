from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class KnowledgeBase:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = QdrantClient(":memory:")  # Use persistent storage in production
        self._initialize_collections()

    def _initialize_collections(self):
        # Create collections for different knowledge types
        self.client.recreate_collection(
            collection_name="solutions",
            vectors_config={
                "size": 384,
                "distance": "Cosine"
            }
        )

    def store_solution(self, problem_type: str, code: str):
        embedding = self.encoder.encode(code)
        self.client.upsert(
            collection_name="solutions",
            points=[
                {
                    "id": hash(code),
                    "vector": embedding.tolist(),
                    "payload": {
                        "type": problem_type,
                        "code": code
                    }
                }
            ]
        )

    def retrieve_solutions(self, error_context: str, top_k: int = 3) -> List[Dict]:
        query_embedding = self.encoder.encode(error_context).tolist()
        return self.client.search(
            collection_name="solutions",
            query_vector=query_embedding,
            limit=top_k
        )
    
    def recommend_tech(self, requirements: str) -> List:
      """Use vector similarity to find successful tech choices"""
      results = self.client.search(
          collection_name="tech_patterns",
          query_text=requirements,
          top_k=5
      )
      return [hit.payload for hit in results]
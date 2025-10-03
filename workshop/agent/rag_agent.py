import string
import chromadb
from .base_agent import BaseAgent
from sentence_transformers import SentenceTransformer

class ContextAgent(BaseAgent):
    prompt_template: string.Template
    collection: chromadb.Collection

    def __init__(self, 
                 name: str, 
                 system_prompt: str, 
                 prompt_template: str, 
                 collection: chromadb.Collection,
                 embedding_model: SentenceTransformer,
                 ):

        super().__init__(name, system_prompt)
        self.collection = collection
        self.embedding_model = embedding_model

        prompt_template = string.Template(prompt_template)
        identifiers = prompt_template.get_identifiers()
        extra_identifiers = set(identifiers) - {'context', 'prompt'}
        
        if len(extra_identifiers) > 0:
            raise ValueError(f"Parameter 'prompt_template' must have only 'context' and 'prompt' identifiers. Instead, got: {extra_identifiers}")
        
        self.prompt_template = prompt_template
        
    def completion(self, prompt: str) -> str:
        query_embedding = self.embedding_model.encode([prompt])
        
        texts = self.collection.query(
            query_embeddings=query_embedding,
            n_results=10,
            include=['documents'],
        )['documents'][0]

        context: str = '\n'.join(texts)

        query = self.prompt_template.substitute(prompt=prompt, context=context)

        return BaseAgent.completion(self, query)
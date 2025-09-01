from typing import List, Dict, Tuple
import re
import math
from collections import Counter

class DocumentIndex:
    def __init__(self):
        self.documents = []  # List of (document_id, filename, chunk_text)
        self.vocabulary = set()
        self.doc_freq = {}  # Document frequency for each term
    
    def _preprocess_text(self, text: str) -> List[str]:
        # Simple text preprocessing: lowercase and split by words
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _compute_tf(self, words: List[str]) -> Dict[str, float]:
        # Compute term frequency
        word_count = len(words)
        if word_count == 0:
            return {}
        
        tf = {}
        counter = Counter(words)
        for word, count in counter.items():
            tf[word] = count / word_count
        
        return tf
    
    def add_document(self, document_id: str, filename: str, chunks: List[str]):
        for chunk in chunks:
            # Preprocess the chunk
            words = self._preprocess_text(chunk)
            
            # Add to documents
            self.documents.append((document_id, filename, chunk))
            
            # Update vocabulary and document frequency
            unique_words = set(words)
            self.vocabulary.update(unique_words)
            
            for word in unique_words:
                self.doc_freq[word] = self.doc_freq.get(word, 0) + 1
    
    def _compute_tfidf_vector(self, tf: Dict[str, float]) -> Dict[str, float]:
        # Compute TF-IDF vector for a document without NumPy
        total_docs = len(self.documents)
        vector = {}
        
        for word, tf_value in tf.items():
            if word in self.doc_freq:
                idf = math.log(total_docs / (1 + self.doc_freq[word]))
                vector[word] = tf_value * idf
        
        return vector
    
    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        # Compute cosine similarity between two vectors without NumPy
        dot_product = 0
        norm1_squared = 0
        norm2_squared = 0
        
        # Calculate dot product and norms
        all_keys = set(vec1.keys()).union(set(vec2.keys()))
        for key in all_keys:
            val1 = vec1.get(key, 0)
            val2 = vec2.get(key, 0)
            dot_product += val1 * val2
            norm1_squared += val1 * val1
            norm2_squared += val2 * val2
        
        norm1 = math.sqrt(norm1_squared)
        norm2 = math.sqrt(norm2_squared)
        
        if norm1 == 0 or norm2 == 0:
            return 0
        
        return dot_product / (norm1 * norm2)
    
    def search(self, query: str, k: int = 5) -> List[Tuple[str, str, str, float]]:
        if not self.documents:
            return []
        
        # Preprocess query
        query_words = self._preprocess_text(query)
        query_tf = self._compute_tf(query_words)
        query_vector = self._compute_tfidf_vector(query_tf)
        
        # Compute similarities with all documents
        similarities = []
        for i, (document_id, filename, chunk) in enumerate(self.documents):
            # Compute TF-IDF for this document
            doc_words = self._preprocess_text(chunk)
            doc_tf = self._compute_tf(doc_words)
            doc_vector = self._compute_tfidf_vector(doc_tf)
            
            # Calculate similarity
            similarity = self._cosine_similarity(query_vector, doc_vector)
            similarities.append((i, similarity))
        
        # Sort by similarity and get top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, sim in similarities[:k] if sim > 0]
        
        # Prepare results
        results = []
        for idx in top_indices:
            document_id, filename, chunk = self.documents[idx]
            similarity = similarities[idx][1]
            results.append((document_id, filename, chunk, float(similarity)))
        
        return results
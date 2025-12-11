# src/retrieval.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class TfidfRetriever:
    def __init__(self, chunk_csv_path):
        """
        Load chunks and initialize vectorizer.
        """
        self.df = pd.read_csv(chunk_csv_path)
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            stop_words="english"
        )
        self.X = self.vectorizer.fit_transform(self.df["chunk_text"])

    def retrieve(self, query, k=5):
        """
        Return top-k most relevant chunks for the query.
        """
        q_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(q_vec, self.X).flatten()

        top_indices = scores.argsort()[-k:][::-1]

        results = self.df.iloc[top_indices].copy()
        results["score"] = scores[top_indices]
        return results[["chunk_id", "source_file", "page_start", "page_end", "score", "chunk_text"]]
        
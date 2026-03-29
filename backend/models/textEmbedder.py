import requests
from typing import List

class TextEmbedder:
    @staticmethod
    def encode(texts) -> List[List[float]]:
        if not texts:
            return []

        url = "http://localhost:11434/api/embed"

        data = {
            "model": "embeddinggemma",
            "input": texts
        }

        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status() 
            
            result = response.json()

            if "embeddings" not in result:
                raise ValueError("Invalid response format")

            return result["embeddings"]

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []

        except Exception as e:
            print(f"Unexpected error: {e}")
            return []


if __name__ == "__main__":
    embeddings = TextEmbedder.encode(["hello how are you?","nice to meet you"])

    print(len(embeddings))        # number of vectors
    print(len(embeddings[0]))     # dimension
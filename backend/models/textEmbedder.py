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

            return result["embeddings"][0]

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return []

        except Exception as e:
            print(f"Unexpected error: {e}")
            return []


if __name__ == "__main__":
    embeddings = TextEmbedder.encode(["3.2 Architecture Development Process Based on the IoT ARM Following the overview of the different cases of usage in which the IoT ARM plays a beneﬁcial role, we will now focus on how the IoT ARM can be used during the process of generating concrete IoT architectures suitable for speciﬁc applications and use cases.We will ﬁrst discuss the idea behind reference models and reference architectures and the underlying methodology.The process of developing an architecture is about ﬁnding a solution to a pre-deﬁned goal.In turn, the development and description of architectures is a modelling exercise.Modelling is important to point out that the modelling itself does not take place in a vacuum but is based on a thorough understanding of the domain to be modelled.In other words, any architecture development is contingent on the understanding of the domain in question.The same is true for a generalisation of this process, i.e. the derivation of reference architectures."])

    print(embeddings)
    print(len(embeddings))        # number of vectors
    # print(len(embeddings[0]))     # dimension
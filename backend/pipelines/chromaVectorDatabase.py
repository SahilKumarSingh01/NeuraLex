import chromadb
from typing import List
from  schema.chunk import Chunk

class VectorDatabase:
    
    def __init__(self, dimension: int = 768):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.dimension = dimension
    
    def add_chunks(self, chunks: List[Chunk], collectionName: str="default"):
        if not chunks:
            return
        
        collection = self.client.get_or_create_collection(name=collectionName)
        
        vectors = [chunk.vector for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        ids = [str(chunk.id) for chunk in chunks]
        
        collection.add(
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, quesEmbedding, collectionName: str, sourceFileName: List[str], top_k: int = 5) -> List[Chunk]:
        results = []

        try:
            collection = self.client.get_collection(name=collectionName)
        except Exception:
            return results

        querySourceList = [{"source": fileName} for fileName in sourceFileName]
        
        if len(querySourceList)>1:
            query={
                "$or": querySourceList
            }
        else:
            query=querySourceList[0]
            

        query_result = collection.query(
            query_embeddings=[quesEmbedding],
            n_results=top_k,
            where=query
        )

        if not query_result or not query_result.get("ids") or len(query_result["ids"]) == 0:
            return results

        ids = query_result["ids"][0]
        documents = query_result["documents"][0]
        metadatas = query_result["metadatas"][0]

        for id_, doc, meta in zip(ids, documents, metadatas):
            results.append(Chunk(
                id=id_,
                text=doc,
                vector=None,
                metadata=meta
            ))
            
        # print(results)

        return results
    
    def delete(self, collectionName: str, sourceFileName: List[str]):
        try:
            collection = self.client.get_collection(name=collectionName)
        except Exception as e:
            print(f"Error getting collection: {e}")
            return

        if not sourceFileName:
            print("No source file names provided")
            return

        
        if len(sourceFileName) == 1:
            query = {"source": sourceFileName[0]}
        else:
            query = {
                "$or": [{"source": name} for name in sourceFileName]
            }

        
        collection.delete(where=query)
        #deleting in case collection is empty
        if collection.count() == 0:
            self.client.delete_collection(name=collectionName)
    
    
    def getChunk(self, collectionName: str, sourceFileName: List[str])->List[Chunk]:
        results = []

        try:
            collection = self.client.get_collection(name=collectionName)
        except Exception:
            return results

        querySourceList = [{"source": fileName} for fileName in sourceFileName]
        
        if len(querySourceList)>1:
            query={
                "$or": querySourceList
            }
        else:
            query=querySourceList[0]
            
        query_result = collection.get(
            
            where=query
        )

        # print(query_result)
        if not query_result or not query_result.get("ids") or len(query_result["ids"]) == 0:
            return results

        ids = query_result.get("ids")
        documents = query_result.get("documents")
        metadatas = query_result.get("metadatas")
        
        for id_, doc, meta in zip(ids, documents, metadatas):
            results.append(Chunk(
                id=id_,
                text=doc,
                vector=None,
                metadata=meta
            ))
            
        # print(results)

        return results
        
        
        
        
            
        
        
            
             

        
        
        
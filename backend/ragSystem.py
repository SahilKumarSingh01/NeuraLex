from  models.documentLoader import DocumentLoader
from  models.generalPurposeModel import GeneralPurposeModel
from  models.textEmbedder import TextEmbedder
from  pipelines.chromaVectorDatabase import VectorDatabase
from  pipelines.documentChunker import DocumentChunker

from typing import List
from schema.chunk import Chunk
class RAGSystem:
    
    def __init__(self):
        self.document_loader=DocumentLoader()
        self.llm =GeneralPurposeModel()
        self.vector_db = VectorDatabase()
        self.text_embedder=TextEmbedder()
        self.document_chunker=DocumentChunker()
        self.sources=[]
    
    def file_to_pageChunk(self,fileNameList:List[str],collectionName:str)->List[Chunk]:
        chunks=self.document_loader.processFileToChunks(fileNameList,collectionName)
        return chunks
    
    def chunk_document(self,chunks:List[Chunk])->List[Chunk]:
        chunks=self.document_chunker.chunk_embedder(chunks)
        return chunks
    
    def store_chunk(self,chunks:List[Chunk],collectionName:str):
        self.vector_db.add_chunks(chunks,collectionName)
    
    
    def ingest_document(self,fileNameList:List[str],collectionName:str):
        chunks=self.file_to_pageChunk(fileNameList,collectionName)
        chunks=self.chunk_document(chunks)
        self.store_chunk(chunks,collectionName)
    
    
    def generateSourceList(self,chunks:List[Chunk]):
         self.sources=[c.to_dict() for c in chunks]
         
    
    def getSourceList(self)->List[dict]:
        return self.sources
    
    def query(self,ques:str,sourceFileNameList:List[str],collectionName:str):
        quesEmbedding=self.text_embedder.encode([ques])
        
        relatedChunks=self.vector_db.search(quesEmbedding,collectionName,sourceFileNameList,5)
        
        self.generateSourceList(relatedChunks)
        
        
        llmGenratedResponse=self.llm.generate(relatedChunks,ques)
        # print(llmGenratedResponse)
        return [self.getSourceList(),llmGenratedResponse]
    
    def deleteChunkEmbedding(self, collectionName: str, sourceFileName: List[str]):
        self.vector_db.delete(collectionName,sourceFileName)
    
    def getChunks(self, collectionName: str, sourceFileName: List[str])->List[Chunk]:
        return self.vector_db.getChunk(collectionName,sourceFileName)
from  models.documentLoader import DocumentLoader
from  models.generalPurposeModel import GeneralPurposeModel
from  models.thinkingModel import ThinkingModel
from  models.textEmbedder import TextEmbedder
from  pipelines.chromaVectorDatabase import VectorDatabase
from  pipelines.documentChunker import DocumentChunker
from  pipelines.CoreferenceResolver import CoreferenceResolver
from typing import List
from schema.chunk import Chunk
class RAGSystem:
    
    def __init__(self):
        self.document_loader=DocumentLoader()
        self.llm =GeneralPurposeModel()
        self.vector_db = VectorDatabase()
        self.text_embedder=TextEmbedder()
        self.document_chunker=DocumentChunker()
        self.coreference_resolver=CoreferenceResolver()
        self.thinkingLLM=ThinkingModel()
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
        chunks=self.coreference_resolver.resolve_chunk_pairs(chunks)
        chunks=self.chunk_document(chunks)
        self.store_chunk(chunks,collectionName)
    
    
    def generateSourceList(self,chunks:List[Chunk]):
         self.sources=[c.to_dict() for c in chunks]
         
    
    def getSourceList(self)->List[dict]:
        return self.sources
    
    def query(self, messages: List[dict], sourceFileNameList: List[str], collectionName: str,mode: str):
        resolved_query = self.coreference_resolver.resolve_history(messages)
        
        ques_embedding = self.text_embedder.encode([resolved_query])[0]
        
        related_chunks = self.vector_db.search(ques_embedding, collectionName, sourceFileNameList, 10,0.6)

        self.generateSourceList(related_chunks)
        
        # Format the chunks into a single string
        context_content = ""
        for i, chunk in enumerate(related_chunks):
            context_content += f"--- Chunk {i+1} ---\n{chunk.text}\n"

        # Injecting the chunks as a 'user' or 'system' role so Ollama accepts it
        # We place it before the final user question
        chunk_message = {
            "role": "system", 
            "content": f"You are a helpful assistant. You may use these chunks to answer:\nRetrieved Context Chunks:\n {context_content}"
        }
        if(context_content):
            messages.insert(-1, chunk_message)
        
        # Now messages contains only valid roles (system, user, assistant)
        llm_generated_response = self.thinkingLLM.generate(messages) if mode == "Thinking" else self.llm.generate(messages)        
        return [self.getSourceList(), llm_generated_response]
    
    def deleteChunkEmbedding(self, collectionName: str, sourceFileName: List[str]):
        self.vector_db.delete(collectionName,sourceFileName)
    
    def getChunks(self, collectionName: str, sourceFileName: List[str])->List[Chunk]:
        return self.vector_db.getChunk(collectionName,sourceFileName)
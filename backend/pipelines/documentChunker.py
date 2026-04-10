import spacy
from typing import List
from  schema.chunk import Chunk
import math
from models.textEmbedder import TextEmbedder

class DocumentChunker:
    
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        
    
    def split_into_sentence_chunk(self, pageText: str):
        doc = self.nlp(pageText)
        return [sent.text for sent in doc.sents]
    
    def chunk_embedder(self, chunks: List[Chunk]) -> List[Chunk]:
        result: List[Chunk] = []
        
        for chunk in chunks:
            sentences = self.split_into_sentence_chunk(chunk.text)
            
            newChunkText = ""
            sentence_id = 0
            leftStart = 0
            
            for i, sentence in enumerate(sentences):
                
                if len(newChunkText + sentence) <= 1000:
                    newChunkText += sentence
                else:
                    
                    result.append(Chunk(
                        id=f"{chunk.id}_{sentence_id}",
                        text=newChunkText,
                        vector=TextEmbedder.encode(newChunkText),
                        metadata=dict(chunk.metadata)
                    ))
                    
                    result[-1].metadata["sentence_range"] = f"{leftStart}-{i}"
                    
                    
                    overlap_len = int(0.2 * len(newChunkText))
                    overlapText = newChunkText[-overlap_len:]
                    
                    newChunkText = overlapText + sentence
                    leftStart = i
                    sentence_id += 1
            
         
            if newChunkText:
                result.append(Chunk(
                    id=f"{chunk.id}_{sentence_id}",
                    text=newChunkText,
                    vector=TextEmbedder.encode([newChunkText]),
                    metadata=dict(chunk.metadata)
                ))
                result[-1].metadata["sentence_range"] = f"{leftStart}-{len(sentences)}"
        # print(result[0])
        # print(type(result[0].vector))
        return result
import spacy
from typing import List
from schema.chunk import Chunk
from models.textEmbedder import TextEmbedder

class DocumentChunker:
    
    def __init__(self):
        # Disable unused components to speed up Spacy
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer", "tagger", "attribute_ruler"])
        self.nlp.add_pipe("sentencizer") 
        
    def split_into_sentence_chunk(self, pageText: str):
        doc = self.nlp(pageText)
        return [sent.text for sent in doc.sents]
    
    def chunk_embedder(self, chunks: List[Chunk]) -> List[Chunk]:
        intermediate_chunks: List[Chunk] = []
        
        # --- Step 1: Text Splitting (CPU Logic) ---
        for chunk in chunks:
            sentences = self.split_into_sentence_chunk(chunk.text)
            newChunkText = ""
            sentence_id = 0
            leftStart = 0
            
            for i, sentence in enumerate(sentences):
                if len(newChunkText + sentence) <= 1000:
                    newChunkText += sentence
                else:
                    c = Chunk(
                        id=f"{chunk.id}_{sentence_id}",
                        text=newChunkText,
                        vector=None, # Temporarily empty
                        metadata=dict(chunk.metadata)
                    )
                    c.metadata["sentence_range"] = f"{leftStart}-{i}"
                    intermediate_chunks.append(c)
                    
                    overlap_len = int(0.2 * len(newChunkText))
                    newChunkText = newChunkText[-overlap_len:] + sentence
                    leftStart = i
                    sentence_id += 1
            
            if newChunkText:
                c = Chunk(
                    id=f"{chunk.id}_{sentence_id}",
                    text=newChunkText,
                    vector=None,
                    metadata=dict(chunk.metadata)
                )
                c.metadata["sentence_range"] = f"{leftStart}-{len(sentences)}"
                intermediate_chunks.append(c)

        # --- Step 2: Batch Embedding (The real speedup) ---
        if intermediate_chunks:
            all_texts = [c.text for c in intermediate_chunks]
            # Send all texts at once to the model
            all_vectors = TextEmbedder.encode(all_texts) 
            
            for i, vector in enumerate(all_vectors):
                intermediate_chunks[i].vector = vector
                
        return intermediate_chunks
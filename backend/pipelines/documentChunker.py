import spacy
from typing import List
from schema.chunk import Chunk
from models.textEmbedder import TextEmbedder

class DocumentChunker:
    
    def __init__(self):
        # We need tok2vec for the statistical senter to work accurately with abbreviations
        # 1. Load the blank model for speed (or the small model if you prefer)
        # We use spacy.blank to avoid any hidden dependency issues with 'sm'
        self.nlp = spacy.blank("en")
        
        # 2. Add the sentencizer specifically
        # This component is designed to set sentence boundaries
        self.nlp.add_pipe("sentencizer")
        
    def chunk_embedder(self, chunks: List[Chunk]) -> List[Chunk]:
        intermediate_chunks: List[Chunk] = []
        
        # --- Step 1: Batch NLP Processing (The Speedup) ---
        # Collect all texts and process them in one go using nlp.pipe
        raw_texts = [chunk.text for chunk in chunks]
        # batch_size=20 is balanced for university-level hardware
        docs = list(self.nlp.pipe(raw_texts, batch_size=20))
        
        # --- Step 2: Text Splitting Logic ---
        # Zip the original chunk objects with the processed spaCy docs
        new_chunk_text = ""
        page=1
        sentence_id = 0
        left_start = 0
        for original_chunk, doc in zip(chunks, docs):
            sentences = [sent.text for sent in doc.sents]

            sentence_id = 0
            left_start = 0
            
            for i, sentence in enumerate(sentences):
                # print("chunker",sentence)
                # Using 1000 character limit
                if len(new_chunk_text) + len(sentence) <= 1000:
                    # Avoid leading space on the first sentence
                    new_chunk_text += (" " if new_chunk_text else "") + sentence
                else:
                    c = Chunk(
                        id=f"{original_chunk.id}_{sentence_id}",
                        text=new_chunk_text,
                        vector=None,
                        metadata=dict(original_chunk.metadata)
                    )
                    c.metadata["sentence"] = f"{left_start+1}"
                    a,b=page,original_chunk.metadata["page"]
                    c.metadata["page"] = f"{a}-{b}" if a!=b else f"{a}"

                    intermediate_chunks.append(c)
                    
                    new_chunk_text = sentence
                    left_start = i
                    sentence_id += 1
                    page=original_chunk.metadata["page"]
            
        # Catch trailing text for this specific doc
        if new_chunk_text:
            c = Chunk(
                id=f"{original_chunk.id}_{sentence_id}",
                text=new_chunk_text,
                vector=None,
                metadata=dict(original_chunk.metadata)
            )
            c.metadata["sentence"] = f"{left_start+1}"
            a,b=page,original_chunk.metadata["page"]
            c.metadata["page"] = f"{a}-{b}" if a!=b else f"{a}"

            intermediate_chunks.append(c)

        # # --- Step 3: Batch Embedding (GPU Efficiency) ---
        # if intermediate_chunks:
        #     all_texts = [c.text for c in intermediate_chunks]
        #     # Send all processed sentences to the embedder in one batch
        #     all_vectors = TextEmbedder.encode(all_texts) 
            
        #     for i, vector in enumerate(all_vectors):
        #         intermediate_chunks[i].vector = vector
        # Not doing here not responsibilty of chunker
                
        return intermediate_chunks
import spacy
from typing import List, Dict
from  schema.chunk import Chunk

class CoreferenceResolver:
    def __init__(self):
        print("Loading spaCy model...")
        self.nlp = spacy.load("en_core_web_sm")
        self.singular_pronouns = {"he", "she", "it", "his", "her", "its"}
        self.plural_pronouns = {"they", "them", "their"}
        self.sep_token = "<<<SEP>>>"

    def resolve(self, text: str) -> str:
        doc = self.nlp(text)
        resolved_tokens = []
        active_singular = None
        active_plural = None

        for sent in doc.sents:
            current_subj = None
            current_obj = None
            is_subj_plural = False

            for token in sent:
                if token.dep_ in ["nsubj", "nsubjpass"] and token.pos_ in ["NOUN", "PROPN"]:                    
                    current_subj = token.text

                    if token.tag_ in ["NNS", "NNPS"]:
                        is_subj_plural = True

                    conjuncts = [
                        c.text for c in token.conjuncts
                        if c.pos_ in ["NOUN", "PROPN"]
                    ]
                    if conjuncts:
                        current_subj = f"{current_subj} and {' and '.join(conjuncts)}"
                        is_subj_plural = True

                if token.dep_ in ["dobj", "pobj"] and token.pos_ in ["NOUN", "PROPN"]:
                    current_obj = token.text

            if current_subj:
                if is_subj_plural:
                    active_plural = current_subj
                else:
                    active_singular = current_subj
                    if current_obj:
                        active_plural = f"{current_subj} and {current_obj}"

            for token in sent:
                replacement = None
                clean_pronoun = token.lower_

                if token.pos_ == "PRON":
                    if clean_pronoun in self.plural_pronouns and active_plural:
                        replacement = active_plural
                    elif clean_pronoun in self.singular_pronouns and active_singular:
                        replacement = active_singular

                if replacement:
                    if token.is_title:
                        replacement = replacement.capitalize()
                    resolved_tokens.append(replacement + token.whitespace_)
                else:
                    resolved_tokens.append(token.text_with_ws)
        return "".join(resolved_tokens)

    def resolve_chunk_pairs(self, chunks: List[Chunk]) -> List[Chunk]:
        if not chunks:
            return chunks

        resolved_chunks:List[Chunk]=[]
        for chunk in chunks:
            resolved_chunks.append(chunk)

        for i in range(len(resolved_chunks) - 1):
            chunk1 = resolved_chunks[i].text
            chunk2 = resolved_chunks[i + 1].text

            combined = f"{chunk1} {self.sep_token} {chunk2}"
            resolved_text = self.resolve(combined)

            if self.sep_token in resolved_text:
                part1, part2 = resolved_text.split(self.sep_token, 1)
            else:
                part1, part2 = resolved_text, chunk2

            resolved_chunks[i].text = part1.strip()
            resolved_chunks[i + 1].text= part2.strip()

        return resolved_chunks

    def resolve_history(self, messages: List[Dict[str, str]]) -> str:
        # 1. Combine user and assistant content into a single narrative for resolution
        # We only care about the text flow to identify what "it/he/she" refers to
        context_parts = []
        for msg in messages:
            if msg["role"] in ["user", "assistant"]:
                context_parts.append(msg["content"])
        
        full_conversation_text = f" {self.sep_token} ".join(context_parts)
        
        # 2. Resolve coreferences across the whole dialogue
        resolved_full_text = self.resolve(full_conversation_text)
        
        # 3. Extract only the last message (the latest query) after it has been resolved
        if self.sep_token in resolved_full_text:
            resolved_parts = resolved_full_text.split(self.sep_token)
            return resolved_parts[-1].strip()
        
        return resolved_full_text.strip()

# --- TEST RUNNER ---
if __name__ == "__main__":
    resolver = CoreferenceResolver()

    # Test Case 1: The Abbreviation & Boundary Test
    print("--- Test 1: Boundary & Pronoun Test ---")
    chunk_a = Chunk("something","3-listen-This function is used in network programming to mark a socket as a passive socket, which means it will be used to accept incoming connection requests. int listenint sockfd, int backlog; sockfd: The file descriptor of the socket. backlog: The maximum number of pending connections. 4-accept-The accept function is used in network programming to accept an incoming connection request on a listening socket. int new_socket acceptint sockfd, struct sockaddr addr, socklen_t addrlen; sockfd: The file descriptor of the listening socket that is ready to accept a new connection. addr: A pointer to a struct sockaddr that will be filled with the address of the connecting client optional, can be NULL. addrlen: A pointer to a socklen_t variable that contains the size of the addr structure. Pointer is modified to store the actual size of the address optional, can be NULL. 5-Connect- This function is called by a client program to initiate communication with a server.",None,None)
    chunk_b = Chunk("something","This project involves U.S.A. standards and i.e. networking protocols. It is very complex.",None,None)
    
    test_chunks = [chunk_a, chunk_b]
    results = resolver.resolve_chunk_pairs(test_chunks)

    for i, res in enumerate(results):
        print(f"Chunk {i+1}: {res.text}")

    # Validation check for U.S.A.
    full_text = " ".join([c.text for c in results])
    if "U.S.A. standards" in full_text:
        print("\nSUCCESS: Sentence boundary preserved for U.S.A.")
    else:
        print("\nFAIL: Sentence broke inside abbreviation.")
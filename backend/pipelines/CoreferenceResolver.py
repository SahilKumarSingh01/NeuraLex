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
                if token.dep_ == "nsubj" and token.pos_ in ["NOUN", "PROPN"]:
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
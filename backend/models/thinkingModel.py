import requests
import json
from typing import List, Dict

class ThinkingModel:
    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model_name = "hf.co/mradermacher/Nanbeige-4.1-Python-DeepThink-3B-i1-GGUF:Q4_K_M"

    def generate(self, messages: List[Dict[str, str]]):
        data = {
            "model": self.model_name,
            "messages": messages,
            "stream": True
        }

        try:
            response = requests.post(
                self.url,
                json=data,
                stream=True,
                timeout=120
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if not line:
                    continue

                chunk = json.loads(line.decode("utf-8"))
                
                if "message" in chunk:
                    msg = chunk["message"]
                    
                    # 1. Check for Thinking Process
                    if "thinking" in msg and msg["thinking"]:
                        payload = {"type": "thinking", "content": msg["thinking"]}
                        yield json.dumps(payload) + '\n'
                    
                    # 2. Check for Final Answer
                    if "content" in msg and msg["content"]:
                        payload = {"type": "answer", "content": msg["content"]}
                        yield json.dumps(payload) + '\n'

                if chunk.get("done", False):
                    break

        except Exception as e:
            error_payload = {"type": "error", "content": str(e)}
            yield json.dumps(error_payload) + '\n'

if __name__ == "__main__":
    # Internal testing logic
    reasoning_model = ThinkingModel()
    conversation = [{"role": "user", "content": "What is 2+2?"}]

    print("--- STREAMING NDJSON ---")
    for raw_json_line in reasoning_model.generate(conversation):
        # On the backend, raw_json_line is what gets yielded to StreamingResponse
        # For this local print test, we parse it back to see the structure
        update = json.loads(raw_json_line)
        
        if update["type"] == "thinking":
            print(f"[THOUGHT]: {update['content']}", end="", flush=True)
        
        elif update["type"] == "answer":
            print(f"\n[ANSWER]: {update['content']}", end="", flush=True)
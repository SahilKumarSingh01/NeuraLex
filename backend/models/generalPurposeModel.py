import requests
import json
from typing import List, Dict

class GeneralPurposeModel:
    def __init__(self):
        pass
      
    def generate(self, messages: List[Dict[str, str]]):
        url = "http://localhost:11434/api/chat"
        
        data = {
            "model": "hf.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF:latest",
            "messages": messages,
            "stream": True
        }

        try:
            response = requests.post(
                url,
                json=data,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if not line:
                    continue

                chunk = json.loads(line.decode("utf-8"))
                
                if "message" in chunk:
                    content = chunk["message"].get("content", "")
                    
                    # Wrap the content in your unified JSON schema
                    # Use 'answer' as the type for standard generation
                    payload = {
                        "type": "answer",
                        "content": content
                    }
                    yield json.dumps(payload) + '\n'

                if chunk.get("done", False):
                    break

        except Exception as e:
            # Even errors should follow the schema so the frontend doesn't crash
            error_payload = {
                "type": "error",
                "content": f"Error in generation: {str(e)}"
            }
            yield json.dumps(error_payload) + '\n'
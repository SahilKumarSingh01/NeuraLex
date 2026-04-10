import requests 
import json
class ToolCalling:
    toolDescription=[]
    functionMap={}
    @staticmethod
    def addFunctionToCalling(function,description) :
        ToolCalling.toolDescription.append(description)
        ToolCalling.functionMap[function.__name__]=function
        
    @staticmethod
    def run():
        messages = [{'role': 'user', 'content': "What is the temperature in New York?"}]

        while True:
            url = "http://localhost:11434/api/chat"
            data = {
                "model": "qwen3:0.6b",
                "messages": messages,
                "stream": True,
                "think": True,
                "tools":ToolCalling.toolDescription
            }

            stream = requests.post(url, json=data)
            thinking = ''
            content = ''
            tool_calls = []

            done_thinking = False
           
            # print(stream)
            for chunk in stream.iter_lines():
                if not chunk:
                    continue

                chunk = chunk.decode("utf-8")
                data = json.loads(chunk)

                message = data.get("message", {})

                if "thinking" in message:
                    thinking += message["thinking"]
                    # print(message["thinking"], end='', flush=True)

                if "content" in message:
                    if not done_thinking:
                        done_thinking = True
                        # print('\n')
                    content += message["content"]
                    # print(message["content"], end='', flush=True)

                if "tool_calls" in message:
                    tool_calls.extend(message["tool_calls"])
                    # print(message["tool_calls"])
                    
                if thinking or content or tool_calls:
                            messages.append({
                                'role': 'assistant',
                                'thinking': thinking,
                                'content': content,
                                'tool_calls': tool_calls
                            })
     
            if not tool_calls:
                            break

            for call in tool_calls:
                if call["function"]["name"] :
                #    result = ToolCalling.get_temperature(**call["function"]["arguments"])  
                    result=ToolCalling.functionMap[call["function"]["name"]](**call["function"]["arguments"])
                else:
                    result = 'Unknown tool'

                messages.append({
                    'role': 'tool',
                    'tool_name': call["function"]["name"],
                    'content': result
                })
      
        data = {
                "model": "qwen3:0.6b",
                "messages": messages,
                "stream": False,
                "think": False,
            }
        
        print("\nFinal response")
        print(messages[-1].get("content"))



def get_temperature(city: str) -> str:
        """Get the current temperature for a city
        
        Args:
            city: The name of the city

        Returns:
            The current temperature for the city
        """
        temperatures = {
            'New York': '22°C',
            'London': '15°C',
        }
        return temperatures.get(city, 'Unknown')
    
if __name__=="__main__":
    desc={
                            "type": "function",
                            "function": {
                                "name": "get_temperature",
                                "description": "Get the current temperature for a city",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "city": {"type": "string"}
                                    },
                                    "required": ["city"]
                                }
                            }
            }
    
    
    ToolCalling.addFunctionToCalling(function=get_temperature,description=desc)
    ToolCalling.run()
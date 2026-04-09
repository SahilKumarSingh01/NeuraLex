from typing import List
import requests
from  schema.chunk import Chunk
import json

# CORRECT IT 
class ThinkingModel:
    @staticmethod
    def generate(context_chunks:List[Chunk],query:str):
        context_part=[]
        
        for i in range(len(context_chunks)):
            context_part.append(
                  f"[Source {i+1}: {context_chunks[i].metadata.get('source','N/A')}, "
                  f"Page {context_chunks[i].metadata.get('page', 'N/A')} ,senetence-range {context_chunks[i].metadata.get('sentence_range','N/A')}]\n{context_chunks[i].text}\n"
            )
        
        context="\n".join(context_part)
        # print(context)
        prompt = f"""You are a helpful AI assistant. Answer the question based ONLY on the provided context.

        CONTEXT:
        {context}

        QUESTION: {query}

        INSTRUCTIONS:
     1. Answer based only on the context above 
     2. If context is insufficient, state that clearly
     3. Be concise but thorough
    

        ANSWER:"""  
        
        # print(prompt)
        
        url = "http://localhost:11434/api/generate"
        data={
            "model":"hf.co/mradermacher/Nanbeige-4.1-Python-DeepThink-3B-i1-GGUF:Q4_K_M",
            "prompt":prompt,
            "stream":True
        }
        response=requests.post(url,
                  json=data,
                  stream=True
                  )
        
        # return response.json()["response"];
        
        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line.decode("utf-8"))

            
            if "response" in data:
                yield data.get('response',"")

            
            if data.get("done", False):
                break
    

if __name__=="__main__":
    context_chunks=[{
      "text": "3.2 Architecture Development Process Based on the IoT ARM Following the overview of the different cases of usage in which the IoT ARM plays a beneﬁcial role, we will now focus on how the IoT ARM can be used during the process of generating concrete IoT architectures suitable for speciﬁc applications and use cases. We will ﬁrst discuss the idea behind reference models and reference architectures and the underlying methodology. The process of developing an architecture is about ﬁnding a solution to a pre-deﬁned goal. In turn, the development and description of architectures is a modelling exercise. It is important to point out that the modelling itself does not take place in a vacuum but is based on a thorough understanding of the domain to be modelled. In other words, any architecture development is contingent on the understanding of the domain in question. The same is true for a generalisation of this process, i.e. the derivation of reference architectures. Thus, reference architectures, such as the one presented in this book, also have to be based on a detailed understanding of the domain in question. This understanding is commonly provided in the form of a reference model. 3.2.1 Reference Model and Reference Architecture Reference models and reference architectures provide a description that is more abstract than what is inherent to actual systems and applications. They are more abstract than concrete architectures that have been designed for a particular appli- cation with particular constraints and choices. From literature, we can extrapolate the dependencies between a reference architecture, architectures and actual systems see Fig. 3.1 Muller 2008. Architectures do help in designing, engineering, building and testing actual systems. At the same time, a better understanding of system constraints can provide input for the architecture design, and this allows future opportunities to be identiﬁed. The structure of the architecture can be made explicit through an architecture description, or it is implicit through the system itself. Extracting essential components of existing architectures, such as mechanisms or the use of standards, allows the deﬁnition of a reference architecture. Guidelines can be linked to a reference architecture in order to derive concrete architectures from the reference architecture Fig. 3.2, left. These general archi- tecture dependencies apply to the modelling of the IoT domain as well. The transformation step from an application-independent model to a platform- independent model is informed by guidelines. The step from platform-independent model to platform-speciﬁc model is discussed later in this chapter. While the model presented in Fig. 3.1 stops at the reference architecture, the IoT-A Architectural Reference Model goes one step beyond this and also deﬁnes a 3 The IoT Architectural Reference Model as Enabler 21",
      "metadata": {
        "source": "test.pdf",
        "page": 1,
        "type": "text"
      }
    },
    {
      "text": "reference model. As already discussed, a reference model provides the ground for a common understanding of the IoT domain by modelling its concepts and their relationships. A detailed description of the IoT Reference Model can be found in Chap. 7. 3.2.2 Generating Architectures Now that we have a general understanding about reference models, reference architectures and their relationships, the important question is how to derive the appropriate concrete architecture from the reference architecture. We dedicate an entire chapter to this issue, namely the Process Chap. 6, where we describe all aspects in great detail. However, the reader needs at least some appreciation of the Fig. 3.1 Relationship between a reference architecture, architectures and actual systems Adapted from Muller 2008 Fig. 3.2 Derivation of implementations platform-speciﬁc models from an architectural refer- ence model application-independent model via the intermediate step of a concrete architecture platform-independent model 22 M. Bauer and J.W. Walewski",
      "metadata": {
        "source": "test.pdf",
        "page": 2,
        "type": "text"
      }
    }]
    
    response=ThinkingModel.generate(context_chunks,"what is Architecture Development Process in Iot")
    print(response)

        

from typing import  Dict, Optional,List
from dataclasses import dataclass
import numpy as np
from dataclasses import asdict
import json
@dataclass
class Chunk:
    """Text chunk with metadata and embedding."""
    id: str
    text: str
    vector:  List[float]
    metadata: Dict
    
    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "vector":self.vector if self.vector else None,
            "metadata": self.metadata
        }
    
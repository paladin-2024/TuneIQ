from pydantic import BaseModel
from dataclasses import dataclass

class RecommendationScheme(BaseModel):
    name: str
    count: int

@dataclass
class Music :
    name:str
    link:str
    artist:str
    image_link:str

from pydantic import BaseModel
from dataclasses import dataclass

class RecommendationScheme(BaseModel):
    artist_name: str
    genres: list[str]
    attrs:dict

@dataclass
class Music :
    name:str
    link:str
    artist:str
    image_link:str

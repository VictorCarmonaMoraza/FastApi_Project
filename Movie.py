from typing import Optional

from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(default='Titulo de la pelicula', min_length=5, max_length=60)
    overview: str = Field(default='Descripcion de la pelicula', min_length=15, max_length=60)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10)
    category: str = Field(default='Aqui va la categoria', min_length=3, max_length=15)


## Serialize to dictionary
def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "overview": self.overview,
            "year": self.year,
            "rating": self.rating,
            "category": self.category
        }

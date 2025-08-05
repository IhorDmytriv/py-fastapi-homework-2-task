import datetime
from typing import List, Optional

from pydantic import BaseModel

from database.models import MovieStatusEnum


class MovieBaseSchema(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: float
    revenue: float
    country_id: Optional[int] = None


class MovieCreateSchema(MovieBaseSchema):
    pass


# class MovieUpdate(MovieCreate):
#     id: int


class MovieDetailSchema(MovieBaseSchema):
    id: int
    # country: CountryModel
    # genres: List[GenreModel]
    # actors: List[ActorModel]
    # languages: List[LanguageModel]

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float
    overview: str

    class Config:
        from_attributes = True


class MoviePaginatedResponseSchema(BaseModel):
    movies: List[MovieListResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int

    model_config = {
        "from_attributes": True,
    }


class MovieListItemSchema(MovieBaseSchema):
    id: int

    class Config:
        from_attributes = True

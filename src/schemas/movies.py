# Write your code here
import datetime
from typing import List, Optional

from pydantic import BaseModel

from database.models import MovieStatusEnum, CountryModel, GenreModel, ActorModel, LanguageModel


class MovieBase(BaseModel):
    name: str
    date: datetime.date
    score: float
    overview: str


class MovieCreate(MovieBase):
    name: str
    date: datetime.date
    score: float
    overview: str
    budget: float
    revenue: float


class MovieUpdate(MovieCreate):
    id: int


class MovieDetailSchema(MovieBase):
    id: int
    name: str
    date: datetime.date
    score: float
    overview: str
    status: MovieStatusEnum
    budget: float
    revenue: float

    class Config:
        from_attributes = True


class MovieListResponseSchema(MovieBase):
    id: int

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


class MovieListItemSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True

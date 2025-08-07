from fastapi import APIRouter, HTTPException, Request

from crud import get_movies, create_movie
from routes.dependencies import PaginationDep, SessionDep
from schemas.movies import MovieListResponseSchema, MovieCreateSchema, MovieDetailSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_films(
        request: Request,
        params: PaginationDep,
        db: SessionDep
):
    films = await get_movies(
        request=request,
        page=params["page"],
        per_page=params["per_page"],
        db=db
    )
    if not films:
        raise HTTPException(status_code=404, detail="No movies found.")
    return films


@router.post("/movies/", status_code=201, response_model=MovieDetailSchema)
async def add_movie(movie: MovieCreateSchema, db: SessionDep):
    db_movie = await create_movie(movie=movie, db=db)
    return db_movie

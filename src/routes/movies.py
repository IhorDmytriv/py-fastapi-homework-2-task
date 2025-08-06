from fastapi import APIRouter, HTTPException, Request

from crud import get_movies
from routes.dependencies import PaginationDep, SessionDep
from schemas.movies import MovieListResponseSchema

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

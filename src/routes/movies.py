from fastapi import APIRouter, Depends, HTTPException, Query, Request

from sqlalchemy.ext.asyncio import AsyncSession

from crud import get_movies
from database import get_db
from schemas.movies import MoviePaginatedResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MoviePaginatedResponseSchema)
async def list_films(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
):
    films = await get_movies(
        request=request,
        page=page,
        per_page=per_page,
        db=db
    )
    if not films:
        raise HTTPException(status_code=404, detail="No movies found.")
    return films

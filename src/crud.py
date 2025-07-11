from fastapi import Query, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db, MovieModel
from schemas import MovieListResponseSchema
from schemas.movies import MoviePaginatedResponseSchema


# async def create_film(db: AsyncSession, film: FilmCreate):
#     new_film = Film(**film.dict())
#     db.add(new_film)
#     await db.commit()
#     await db.refresh(new_film)
#     return new_film

# async def get_film(db: AsyncSession, film_id: int):
#     result = await db.execute(select(Film).where(Film.id == film_id))
#     film = result.scalar_one_or_none()
#     return film

async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
):

    offset = (page - 1) * per_page

    total_items_query = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_items_query.scalar()

    total_pages = (total_items + per_page - 1) // per_page

    if not total_items or page > total_pages:
        return None

    result = await db.execute(select(MovieModel).offset(offset).limit(per_page).order_by(MovieModel.id.desc()))
    movies = result.scalars().all()
    movie_schemas = [MovieListResponseSchema.model_validate(movie) for movie in movies]

    full_path = request.url.path

    if full_path.startswith("/api/v1"):
        base_url = full_path[len("/api/v1"):]
    else:
        base_url = full_path

    query_template = f"?page={{}}&per_page={per_page}"
    prev_page = f"{base_url}{query_template.format(page - 1)}" if page > 1 else None
    next_page = f"{base_url}{query_template.format(page + 1)}" if page < total_pages else None

    return MoviePaginatedResponseSchema(
        movies=movie_schemas,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )

# async def update_film(db: AsyncSession, film_id: int, film: FilmUpdate):
#     result = await db.execute(select(Film).where(Film.id == film_id))
#     db_film = result.scalar_one_or_none()
#     if not db_film:
#         return None
#
#     db_film.title = film.title
#     db_film.genre = film.genre
#     db_film.price = film.price
#     await db.commit()
#     await db.refresh(db_film)
#     return db_film
#
# async def delete_film(db: AsyncSession, film_id: int):
#     result = await db.execute(select(Film).where(Film.id == film_id))
#     db_film = result.scalar_one_or_none()
#     if not db_film:
#         return None
#     await db.delete(db_film)
#     await db.commit()
#     return db_film

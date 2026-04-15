from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category

async def get_categories_curd(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_sql = select(Category).offset(skip).limit(limit)
    result = await db.execute(db_sql)
    return result.scalars().all()
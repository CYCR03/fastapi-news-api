from fastapi import APIRouter, Depends
from curd.news import get_categories_curd
from config.db_config import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/api/news', tags=['news'])

# 获取新闻分类列表
@router.get('/categories')
async def get_categories(db:AsyncSession = Depends(get_db), skip:int = 0, limit:int = 100):
    categories = await get_categories_curd(db=db, skip=skip, limit=limit)
    return {
        "code" : 200,
        "message" : "获取新闻分类成功",
        "data" : categories
    }
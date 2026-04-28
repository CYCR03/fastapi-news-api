from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from curd.news import (
    get_categories_curd,
    get_news_list_curd,
    count_news_curd,
    get_news_detail_curd,
    increase_views_curd,
    get_related_news_curd
)
from config.db_config import get_db
from cache.news_cache import (
    get_cache_categories,
    set_cache_categories,
    get_cache_news_list,
    set_cache_news_list
)
from schemas.news import NewsResponseBase 

router = APIRouter(prefix='/api/news', tags=['news'])

# 获取新闻分类列表路由
@router.get('/categories')
async def get_categories(
    db:AsyncSession = Depends(get_db), 
    skip:int = 0, 
    limit:int = 100
):
    # 先查询缓存
    categories = await get_cache_categories()
    # 如果缓存不存在，则查询数据库
    if categories is None:
        categories = await get_categories_curd(db=db, skip=skip, limit=limit)
        # 如果查询的数据结果不为空，要写入缓存
        if categories is not None:
            cache_categories = jsonable_encoder(categories)
            await set_cache_categories(cache_categories)
    
    return {
        "code" : 200,
        "message" : "获取新闻分类成功",
        "data" : categories
    }

# 获取新闻列表路由
@router.get('/list')
async def get_news_list(
    db:AsyncSession = Depends(get_db), 
    page:int = 1, 
    page_size:int = Query(10, le=100, alias='pageSize'),
    category_id:int = Query(..., alias='categoryId')
):
    # 计算跳过的新闻数量
    offset = (page-1)*page_size
    # 获取新闻总数
    total = await count_news_curd(db=db, category_id=category_id)

    # 先查询缓存
    news_list = await get_cache_news_list(category_id=category_id, page=page, page_size=page_size)
    # 如果缓存不存在，则查询数据库
    if news_list is None:
        news_list = await get_news_list_curd(db=db, category_id=category_id, skip=offset, limit=page_size)
        # 如果查询的数据结果不为空，要写入缓存
        if news_list is not None:
            # 先将orm对象转成pydantic对象，再转成json兼容格式
            # by_alias=False表示不转换字段别名
            cache_news_list = [NewsResponseBase.model_validate(news).model_dump(mode="json", by_alias=False) for news in news_list]
            await set_cache_news_list(category_id=category_id, page=page, page_size=page_size, data=cache_news_list)
    
    # 判断是否有更多
    has_more = offset + len(news_list) < total

    return {
        "code" : 200,
        "message" : "获取新闻列表成功",
        "data" : {
            "list" : news_list,
            "total" : total,
            "hasMore" : has_more
        }
    }

# 获取新闻详情路由 
@router.get('/detail')
async def get_news_detail(
    news_id: int = Query(..., alias='id'), 
    db:AsyncSession = Depends(get_db)
):
    # 获取新闻详情 + 浏览量+1 + 获取相关新闻

    news = await get_news_detail_curd(db=db, news_id=news_id)
    # 新闻不存在则抛出异常
    if news is None:
        raise HTTPException(status_code=404, detail="新闻不存在")

    # 新闻浏览量加1
    views_res = await increase_views_curd(db=db, news_id=news_id)
    if views_res is None:
        raise HTTPException(status_code=500, detail="新闻浏览量更新失败")
    
    # 获取相关新闻
    related_news = await get_related_news_curd(db=db, news_id=news_id, category_id=news.category_id)

    return {
        "code" : 200,
        "message" : "获取新闻详情成功",
        "data" :{
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'image': news.image,
            'author': news.author,
            'publishTime': news.publish_time,
            'categoryId': news.category_id,
            'views': news.views,
            'relatedNews': related_news
        }
    }
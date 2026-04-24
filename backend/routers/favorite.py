from fastapi import APIRouter, Query, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from curd.favorite import (
    is_news_favorite, 
    add_news_favorite, 
    remove_news_favorite, 
    get_user_favorite_count,
    get_favorite_list,
    clear_favorite_list
    )
from schemas.favorite import (
    FavoriteCheckResponse, 
    FavoriteAddRequest, 
    FavoriteResponse, 
    FavoriteNewsResponse,
    FavoriteListResponse
    )

router = APIRouter(prefix='/api/favorite', tags=['favorite'])

# 检查新闻收藏状态
@router.get('/check')
async def check_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    查询新闻是否被收藏
    """
    is_favorite = await is_news_favorite(db, user.id, news_id)
    return success_response(message="检查收藏状态成功", data=FavoriteCheckResponse(isFavorite=is_favorite))

# 添加新闻收藏
@router.post('/add')
async def add_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    添加新闻收藏
    """
    favorite = await add_news_favorite(db, user.id, data.news_id)
    return success_response(message="添加收藏成功", data=FavoriteResponse.model_validate(favorite)) 

# 取消新闻收藏
@router.delete('/remove')
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    取消新闻收藏
    """
    is_remove = await remove_news_favorite(db, user.id, news_id)
    # 判断是否成功取消收藏
    if not is_remove:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏记录不存在")
    
    return success_response(message="取消收藏成功")

# 新闻收藏列表
@router.get("/list")
async def favorite_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize", description="每页数量"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    total = await get_user_favorite_count(db, user.id)
    rows = await get_favorite_list(db, user.id, page, page_size)
    has_more = total > page*page_size

    favorite_list = [
        FavoriteNewsResponse.model_validate({**news.__dict__, "favorite_time": favorite_time})
        for news, favorite_time in rows
    ]
    
    data = FavoriteListResponse(
        list=favorite_list,
        total=total,
        has_more=has_more
    )
    return success_response(message="获取收藏列表成功", data=data)

# 清空收藏列表
@router.delete("/clear")
async def clear_favorite(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    count = await clear_favorite_list(db, user.id)
    return success_response(message=f"清空收藏列表成功，共删除了{count}条数据")
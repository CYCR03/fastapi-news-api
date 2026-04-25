from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from schemas.history import (
    HistoryAddRequest, 
    HistoryResponse,
    NewsHistoryResponse,
    HistoryListResponse
    )
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response
from curd.history import (
    add_view_history,
    get_user_history_count,
    get_view_history_list,
    delete_one_view_history,
    clear_view_history
)

router = APIRouter(prefix="/api/history", tags=["history"])

# 添加浏览记录
@router.post("/add")
async def add_history(
    data: HistoryAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    history_data = await add_view_history(db, user.id, data.news_id)
    return success_response(message="添加浏览历史成功", data=HistoryResponse.model_validate(history_data))

# 获取浏览记录列表
@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize", description="每页数量"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    total = await get_user_history_count(db, user.id)
    rows = await get_view_history_list(db, user.id, page, page_size)
    has_more = total > page * page_size

    # 构造浏览记录列表
    history_list = [
        NewsHistoryResponse.model_validate({**News.__dict__, "view_time":view_time})
        for News, view_time in rows
    ]

    # 构造响应数据
    data = HistoryListResponse(
        list=history_list,
        total=total,
        has_more=has_more
    )
    return success_response(message="获取浏览历史列表成功", data=data)

# 删除单条浏览记录
@router.delete("/delete/{news_id}")
async def delete_history(
    news_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    根据用户ID和新闻ID删除某个用户的单条浏览记录
    """
    result = await delete_one_view_history(db, user.id, news_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="浏览历史不存在")
    return success_response(message="删除浏览历史成功")

# 清空用户浏览记录
@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    根据用户ID清空该用户的所有浏览记录
    """
    count = await clear_view_history(db, user.id)
    return success_response(message= f"清空浏览历史成功, 删除了{count}条浏览记录")
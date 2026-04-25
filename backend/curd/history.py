from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select, delete

from models.news import News
from models.history import History

# 获取某个用户某条新闻的浏览记录
async def get_history(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    获取某个用户某条新闻的浏览记录
    """
    db_sql = select(History).where(History.user_id == user_id, History.news_id == news_id) 
    result = await db.execute(db_sql)
    return result.scalar_one_or_none() 

# 添加浏览记录
async def add_view_history(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    添加浏览记录， 浏览历史存在则更新时间，不存在则添加
    """
    view_history = await get_history(db, user_id, news_id)

    # 浏览历史存在则更新时间，不存在则添加
    if view_history is not None:
        view_history.view_time = datetime.now()
    else:  
        view_history = History(user_id=user_id, news_id=news_id)

    db.add(view_history)
    await db.commit()
    await db.refresh(view_history) 
    return view_history

# 根据用户ID统计所有浏览记录
async def get_user_history_count(
        db: AsyncSession,
        user_id: int
):
    """
    根据用户ID统计所有浏览记录
    """
    db_sql = select(func.count(History.news_id)).where(History.user_id == user_id)
    result = await db.execute(db_sql)
    return result.scalar_one()

# 获取某个用户的浏览历史记录列表
async def get_view_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    """
    根据用户ID获取用户的浏览历史记录列表
    """
    offset = (page - 1) * page_size
    db_sql = (
        select(News, History.view_time)
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset).limit(page_size)
        )
    result = await db.execute(db_sql)
    rows = result.all()
    return rows

# 删除某个用户的单条浏览记录
async def delete_one_view_history(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    """
    根据用户ID和新闻ID删除某个用户的单条浏览记录
    """
    db_sql = delete(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(db_sql)
    await db.commit()
    return result.rowcount > 0

# 删除某个用户的所有浏览记录
async def clear_view_history(
        db: AsyncSession,
        user_id: int
):
    """
    根据用户ID删除某个用户的所有浏览记录
    """
    db_sql = delete(History).where(History.user_id == user_id)
    result = await db.execute(db_sql)
    await db.commit()
    return result.rowcount
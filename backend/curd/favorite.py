from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, func, select

from models.favorite import Favorite
from models.news import News

# 检测新闻是否被收藏
async def is_news_favorite(
        db: AsyncSession, 
        user_id: int, 
        news_id: int
) -> bool:
    """
    根据用户ID和新闻ID查询收藏记录，如果存在则返回True，否则返回False
    """
    db_sql = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(db_sql)
    is_favorite = result.scalar_one_or_none() is not None
    return is_favorite

# 给新闻添加收藏
async def add_news_favorite(
        db: AsyncSession, 
        user_id: int, 
        news_id: int
):
    """
    给新闻添加收藏
    """
    favorite_news = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite_news)

    await db.commit()
    await db.refresh(favorite_news)

    return favorite_news

# 取消新闻收藏
async def remove_news_favorite(
        db: AsyncSession, 
        user_id: int, 
        news_id: int
):
    """
    取消新闻收藏，成功返回True，失败返回False
    """
    db_sql = delete(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(db_sql)
    await db.commit()

    return result.rowcount > 0

# 获取用户的收藏新闻总数
async def get_user_favorite_count(
        db: AsyncSession, 
        user_id: int
):
    """
    根据用户ID获取用户收藏新闻总数
    """
    db_sql = select(func.count(Favorite.news_id)).where(Favorite.user_id == user_id)
    result = await db.execute(db_sql)
    return result.scalar_one()

# 获取新闻收藏列表: 
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    """
    获取新闻收藏列表
    """   
    # 跳过的新闻数量     
    offset = (page-1)*page_size

    # 联表查询
    db_sql = (
        select(News, Favorite.created_at.label('favorite_time'))
        .join(Favorite, Favorite.news_id == News.id )
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset).limit(page_size)
        )
    
    result = await db.execute(db_sql)
    row = result.all()
    return row

# 清空新闻收藏列表
async def clear_favorite_list(
        db: AsyncSession,
        user_id: int 
):
    """
    清空收藏列表，并返回删除的行数
    """
    db_sql = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(db_sql)
    await db.commit()
    return result.rowcount

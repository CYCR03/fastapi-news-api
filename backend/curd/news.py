from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category, News

#查询新闻分类列表
async def get_categories_curd(db: AsyncSession, skip: int = 0, limit: int = 100):
    db_sql = select(Category).offset(skip).limit(limit)
    result = await db.execute(db_sql)
    return result.scalars().all()

# 查询新闻列表
async def get_news_list_curd(db: AsyncSession, category_id: int, skip: int = 0, limit: int = 10):
    db_sql = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(db_sql)
    return result.scalars().all()

# 按新闻分类id统计新闻总量
async def count_news_curd(db: AsyncSession, category_id: int):
    db_sql = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(db_sql)
    return result.scalar_one()

# 按新闻id获取新闻详情
async def get_news_detail_curd(db: AsyncSession, news_id: int):
    db_sql = select(News).where(News.id == news_id)
    result = await db.execute(db_sql)
    # 返回结果唯一或为空
    return result.scalar_one_or_none()

# 浏览量加1
async def increase_views_curd(db: AsyncSession, news_id: int):
    db_sql = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(db_sql)
    await db.commit()

    # 检查更新是否命中
    return result.rowcount > 0

# 推荐与新闻id相同分类id的相关新闻
async def get_related_news_curd(db: AsyncSession, news_id: int, category_id: int, limit: int = 5):
    db_sql = select(News).where(
        News.id != news_id,
        News.category_id == category_id
    ).order_by(
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)

    result = await db.execute(db_sql)
    related_list = result.scalars().all()
    return [
    {
        'id': news.id,
        'title': news.title,
        'description': news.description,
        'image': news.image,
        'author': news.author,
        'views': news.views,
    } for news in related_list]

from typing import Any, Dict, List, Optional

from config.redis_config import get_cache_json, set_cache


CATEGORIES_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"

# 获取新闻分类缓存
async def get_cache_categories():
    return await get_cache_json(CATEGORIES_KEY)

# 写入新闻分类缓存（数越稳定，则缓存时间越长） 
# 分类、配置: 7200，列表: 600，详情: 1800，验证码：120
async def set_cache_categories(
    data: List[Dict[str, Any]], 
    expire: int = 7200
):
    return await set_cache(CATEGORIES_KEY, data, expire)


# 写入新闻列表缓存
# news:list:{category_id}:{page}:{page_size} + 列表数据 + 过期时间
async def set_cache_news_list(
    category_id: Optional[int],
    page: int, 
    page_size: int, 
    data: List[Dict[str, Any]], 
    expire: int = 600
):
    # 判断分类ID是否为空
    if category_id is None:
        category_id = 'all'
    else:
        category_id = str(category_id)
    
    key = NEWS_LIST_PREFIX + category_id + f":{page}:{page_size}"
    return await set_cache(key, data, expire)

# 获取新闻列表缓存
async def get_cache_news_list(
    category_id: Optional[int],
    page: int, 
    page_size: int
):
    if category_id is None:
        category_id = 'all'
    else:
        category_id = str(category_id)
    key = NEWS_LIST_PREFIX + category_id + f":{page}:{page_size}"
    return await get_cache_json(key)
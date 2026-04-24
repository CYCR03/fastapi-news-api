from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.news import NewsResponseBase

# 收藏状态响应类
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

# 添加新闻收藏请求类
class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")

# 收藏记录响应类
class FavoriteResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias="userId")
    news_id: int = Field(..., alias="newsId")
    created_at: datetime = Field(..., alias="createdTime")

    model_config = ConfigDict(
        populate_by_name=True,     # 允许使用原本的属性名以及字段别名
        from_attributes=True,      # 允许从ORM对象中获取属性值（原本默认为False，既通过接收字典获取属性值）
    )

# 收藏新闻响应类
class FavoriteNewsResponse(NewsResponseBase):
    favorite_time: datetime = Field(..., alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True, # 允许使用原本的属性名以及字段别名
        from_attributes=True,  # 允许从ORM对象中获取属性值
    )

# 收藏新闻列表响应类
class FavoriteListResponse(BaseModel):
    list: list[FavoriteNewsResponse]
    total: int
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,  # 允许使用原本的属性名以及字段别名
        from_attributes=True,  # 允许从ORM对象中获取属性值
    )
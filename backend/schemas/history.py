from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from schemas.news import NewsResponseBase

# 添加浏览历史记录请求类
class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias='newsId')

    model_config = ConfigDict(
        populate_by_name=True,      # 允许使用原本的属性名以及字段别名
    )

# 浏览历史记录响应类
class HistoryResponse(BaseModel):
    id: int
    user_id: int = Field(..., alias='userId')
    news_id: int = Field(..., alias='newsId')
    view_time: datetime = Field(..., alias='viewTime')

    model_config = ConfigDict(
        populate_by_name=True,      # 允许使用原本的属性名以及字段别名
        from_attributes=True        # 允许从ORM对象中获取属性值
    )

# 新闻浏览记录响应类
class NewsHistoryResponse(NewsResponseBase):
    view_time: datetime = Field(..., alias='viewTime')

    model_config = ConfigDict(
        populate_by_name=True,      # 允许使用原本的属性名以及字段别名
        from_attributes=True        # 允许从ORM对象中获取属性值
    )

class HistoryListResponse(BaseModel):
    list: list[NewsHistoryResponse]
    total: int
    has_more: bool = Field(..., alias='hasMore')

    model_config = ConfigDict(
        populate_by_name=True,      # 允许使用原本的属性名以及字段别名
        from_attributes=True        # 允许从ORM对象中获取属性值
    )
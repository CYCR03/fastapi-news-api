from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# 新闻响应基类
class NewsResponseBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: Optional[datetime] = Field(..., alias="publishTime")

    model_config = ConfigDict(
        populate_by_name=True, # 允许使用原本的属性名以及字段别名
        from_attributes=True,  # 允许从ORM对象中获取属性值（原本默认为False，既通过接收字典获取属性值）        
    )

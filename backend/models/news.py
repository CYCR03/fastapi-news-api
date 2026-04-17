from datetime import datetime
from typing import Optional
from unicodedata import category

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 创建新闻基类
class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

# 创建新闻分类表类
class Category(Base):
    __tablename__ = 'news_category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, default=0, comment="排序顺序")

    # 定义字符串表示方法，方便调试和日志记录
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', sort_order={self.sort_order})>"

# 创建新闻表类
class News(Base):
    __tablename__ = 'news'

    # 设置通用表参数，如索引、表约束和表注释
    __table_args__ = (
        Index('fk_news_category_idx', 'category_id'),
        Index('idx_publish_time_views', 'publish_time', 'views')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="新闻ID")
    title: Mapped[str] =mapped_column(String(255), nullable=False, comment="新闻标题")
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="新闻简介")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="新闻内容")
    image: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="封面图片URL")
    author: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="作者")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('news_category.id'), nullable=False, comment="分类ID")
    views: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}', views={self.views})>"
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    '''
    用户信息表ORM模型
    '''

    __tablename__ = "user"

    # 创建索引
    __table_args__ = (
        Index('idx_username', 'username'),
        Index('idx_phone', 'phone'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="用户名")
    password: Mapped[str] = mapped_column(String(255), nullable=False, comment="密码（加密存储）")
    nickname: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="昵称")
    avatar: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment="头像URL")
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'), default='unknown', comment="性别")
    bio: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="简介")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment="手机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, nickname={self.nickname})>"

class UserToken(Base):
    '''
    用户令牌表ORM模型
    '''

    __tablename__ = "user_token"

    # 创建索引
    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_token', 'token'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="令牌ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id), nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="令牌过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")

    def __repr__(self):
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token={self.token})>"
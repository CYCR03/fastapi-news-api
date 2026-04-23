from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

class UserRequest(BaseModel):
    username: str = Field(..., description="注册用户名")
    password: str = Field(..., description="注册密码", min_length=6)

# 用户详情模型基类
class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

# 用户详情响应模型类
class UserInfoResponse(UserInfoBase):
    id: int
    username: str

    model_config = ConfigDict(
        from_attributes=True,   # 允许从对象中获取属性值
    )

# 用户认证响应模型类
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name = True,    # 允许使用原本的属性名以及字段别名
        from_attributes = True,     # 允许从ORM对象中获取属性值（原本默认为True，既通过接收字典获取属性值）
    )

# 用户更新请求类
class UserUpdateRequest(UserInfoBase):
    phone : Optional[str] = Field(None, description="手机号")

# 用户密码更新请求类
class UserUpdatePwdRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")
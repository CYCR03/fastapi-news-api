from pydantic import BaseModel, Field

class UserRequest(BaseModel):
    username: str = Field(..., description="注册用户名")
    password: str = Field(..., description="注册密码", min_length=6)
    # nickname: str | None = Field(None, description="昵称")
    # gender: str | None = Field(None, description="性别")
    # bio: str | None = Field(None, description="简介")
    # phone: str | None = Field(None, description="手机号")
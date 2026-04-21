from passlib.context import CryptContext

# 创建加密上下文
pwd_context = CryptContext(
    schemes=["argon2", "bcrypt"],   # 密码加密算法
    default= "argon2",              # 默认加密算法
    deprecated="auto"               # 自动兼容旧密码
    )

# 密码加密
def hash_password(password: str):
    return pwd_context.hash(password)
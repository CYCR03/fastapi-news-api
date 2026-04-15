from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os

# 加载根目录的环境变量
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

ASYNC_ENGINE_URL = f'mysql+asyncmy://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# 创建异步引擎
async_engine = create_async_engine(
    url = ASYNC_ENGINE_URL,
    pool_size = 10,     # 连接池
    max_overflow = 20,  # 最大额外连接数
    echo = True         # 输出sql日志 
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,       # 绑定异步引擎
    class_ = AsyncSession,      # 指定异步会话类
    expire_on_commit = False    # 会话对象commit后不会过期 
)

# 创建获取异步会话的依赖项
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

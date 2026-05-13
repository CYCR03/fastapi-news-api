# FastAPI News API

基于 FastAPI 的新闻聚合后端服务，为移动端提供高性能的新闻资讯 API。

## 技术栈

| 类别 | 技术 |
|------|------|
| Web 框架 | FastAPI (异步) |
| ORM | SQLAlchemy 2.0 (异步) |
| 数据库 | MySQL |
| 缓存 | Redis 7 |
| 密码加密 | Argon2 / Bcrypt |
| 数据校验 | Pydantic v2 |
| 容器化 | Docker Compose |
| 包管理 | uv |

## 功能特性

- **新闻模块** — 新闻分类、列表分页、详情查看，支持 Redis 缓存
- **用户模块** — 注册、登录、个人信息管理、密码修改
- **收藏模块** — 收藏/取消收藏新闻、收藏列表、清空收藏
- **浏览历史** — 记录浏览历史、分页查看、单条删除、清空历史
- **认证机制** — Token 认证，保护敏感接口
- **缓存策略** — 分类 7200s / 列表 600s / 详情 1800s，LRU 淘汰
- **CORS 支持** — 允许前端跨域访问

## 项目结构

```
backend/
├── main.py                  # 应用入口
├── pyproject.toml           # 依赖声明
├── config/
│   ├── db_config.py         # MySQL 异步引擎 & 会话
│   └── redis_config.py      # Redis 异步客户端
├── models/
│   ├── news.py              # 新闻 & 分类 ORM
│   ├── users.py             # 用户 & Token ORM
│   ├── favorite.py          # 收藏 ORM
│   └── history.py           # 浏览历史 ORM
├── schemas/
│   ├── news.py              # 新闻请求/响应模型
│   ├── users.py             # 用户请求/响应模型
│   ├── favorite.py          # 收藏请求/响应模型
│   └── history.py           # 历史请求/响应模型
├── routers/
│   ├── news.py              # /api/news/*
│   ├── users.py             # /api/user/*
│   ├── favorite.py          # /api/favorite/*
│   └── history.py           # /api/history/*
├── curd/
│   ├── news.py              # 新闻 CRUD
│   ├── news_cache.py        # 新闻缓存 CRUD
│   ├── users.py             # 用户 CRUD
│   ├── favorite.py          # 收藏 CRUD
│   └── history.py           # 历史 CRUD
├── cache/
│   └── news_cache.py        # 缓存键封装
└── utils/
    ├── auth.py              # Token 认证依赖
    ├── security.py          # 密码加密
    ├── response.py          # 统一响应格式
    ├── exception.py         # 异常定义
    └── exception_hendlers.py # 异常处理器注册
```

### 端点总览

#### 新闻（无需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/news/categories` | 获取新闻分类 |
| GET | `/api/news/list` | 获取新闻列表（分页） |
| GET | `/api/news/detail` | 获取新闻详情 |

#### 用户

| 方法 | 路径 | 说明 | 需认证 |
|------|------|------|--------|
| POST | `/api/user/register` | 用户注册 | 否 |
| POST | `/api/user/login` | 用户登录 | 否 |
| GET | `/api/user/info` | 获取用户信息 | 是 |
| PUT | `/api/user/update` | 更新用户信息 | 是 |
| PUT | `/api/user/password` | 修改密码 | 是 |

#### 收藏（需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/favorite/check` | 检查收藏状态 |
| POST | `/api/favorite/add` | 添加收藏 |
| DELETE | `/api/favorite/remove` | 取消收藏 |
| GET | `/api/favorite/list` | 收藏列表（分页） |
| DELETE | `/api/favorite/clear` | 清空收藏 |

#### 浏览历史（需认证）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/history/add` | 添加浏览记录 |
| GET | `/api/history/list` | 浏览历史（分页） |
| DELETE | `/api/history/delete/{news_id}` | 删除单条记录 |
| DELETE | `/api/history/clear` | 清空浏览历史 |

## 数据库模型

| 表名 | 说明 |
|------|------|
| user | 用户表（用户名、密码、昵称、头像等） |
| user_token | 用户令牌表 |
| news_category | 新闻分类表 |
| news | 新闻表（标题、内容、作者、浏览量等） |
| favorite | 收藏表（用户-新闻多对多） |
| history | 浏览历史表（用户-新闻多对多） |

建表脚本见 `database/database.sql`。

## 许可证

MIT License

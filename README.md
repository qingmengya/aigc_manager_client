# AIGC Manager Client

## 项目概述

AIGC Manager Client 是一个用于管理Docker容器的FastAPI应用程序，专为AI生成内容(AIGC)服务设计。该客户端提供了一套完整的API接口，用于创建、重启、停止容器，以及监控容器的运行状态和空闲时间。

## 功能特性

- 容器管理：创建、重启、停止Docker容器
- 状态监控：查询容器运行状态和空闲时间
- 实例监控：监控服务器实例的空闲时间
- RESTful API：提供标准化的API接口

## 技术栈

- **FastAPI**: 高性能的Python Web框架
- **Uvicorn**: ASGI服务器
- **Docker SDK for Python**: 用于与Docker引擎交互

## 安装指南

### 前提条件

- Python 3.10+
- Docker

### 安装步骤

1. 克隆仓库

```bash
git clone <repository-url>
cd aigc_manager_client
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 启动服务

```bash
python main.py
```

或者使用提供的脚本：

```bash
./run.sh
```

服务将在 `http://0.0.0.0:9960` 上启动，并提供API访问。

### API文档

启动服务后，可以通过访问 `http://localhost:9960/docs` 查看自动生成的API文档。

## API接口说明

### 容器管理

#### 获取容器空闲时间

```
GET /api/containers/freetime/{name}
```

返回指定容器的运行状态和空闲时间（秒）。

#### 重启容器

```
PUT /api/containers/restart/{name}
```

重启指定名称的容器。

#### 创建容器

```
POST /api/containers/create
```

请求体：
```json
{
  "image": "镜像名称",
  "port": 端口号,
  "container_name": "容器名称"
}
```

### 实例监控

#### 获取实例空闲时间

```
GET /api/instances/freetime
```

返回服务器实例的空闲时间（当没有运行中的容器时开始计算）。

## 项目结构

```
aigc_manager_client/
├── api/                # API接口定义
│   ├── __init__.py
│   ├── api.py          # API实现
│   └── router.py       # 路由注册
├── models/             # 数据模型
│   ├── __init__.py
│   └── api_models.py   # API请求/响应模型
├── utils/              # 工具类
│   ├── __init__.py
│   ├── docker_utils.py # Docker操作工具
│   └── resp.py         # 响应格式化工具
├── main.py             # 应用入口
├── requirements.txt    # 项目依赖
└── run.sh              # 启动脚本
```

## 开发指南

### 添加新的API接口

1. 在 `api/api.py` 中定义新的路由和处理函数
2. 如需新的请求/响应模型，在 `models/api_models.py` 中定义
3. 如需新的Docker操作，在 `utils/docker_utils.py` 中实现

## 许可证

[MIT](LICENSE)
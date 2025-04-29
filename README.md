# AIGC Manager Client

这是一个用于获取Docker容器运行日志的FastAPI应用。

## 功能

- 获取所有Docker容器列表
- 获取指定Docker容器的运行日志

## 安装

1. 克隆仓库

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

## 运行

```bash
python main.py
```

服务器将在 `http://localhost:8000` 启动。

## API文档

启动服务后，可以访问以下URL查看API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API端点

### 获取所有Docker容器

```
GET /api/docker/containers
```

返回所有Docker容器的列表，包括运行中和已停止的容器。

### 获取容器日志

```
GET /api/docker/logs/{container_id}
```

参数：
- `container_id`: Docker容器ID或名称
- `tail`: (可选) 获取最后N行日志，默认为100
- `since`: (可选) 获取指定时间后的日志，格式为ISO时间或相对时间，如'1h'

## 示例

### 获取所有容器

```bash
curl http://localhost:8000/api/docker/containers
```

### 获取指定容器的最近50行日志

```bash
curl "http://localhost:8000/api/docker/logs/container_id?tail=50"
```

### 获取指定容器过去1小时的日志

```bash
curl "http://localhost:8000/api/docker/logs/container_id?since=1h"
```

## 注意事项

- 需要在运行此应用的机器上安装Docker
- 运行此应用的用户需要有访问Docker守护进程的权限
from fastapi import FastAPI
import uvicorn
from api.router import api_router

app = FastAPI(title="AIGC Manager Client", description="API for managing Docker containers and logs")

# 注册API路由
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "AIGC Manager Client API"}


def main():
    """启动FastAPI应用服务器"""
    uvicorn.run("main:app", host="0.0.0.0", port=9960, reload=True)


if __name__ == "__main__":
    main()

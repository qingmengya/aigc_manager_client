from pydantic import BaseModel


class Response():
    """
    api 接口的返回
    """
    statusCode: str
    message: str
    data: any

class CreateContainerReq(BaseModel):
    image: str
    port: int
    container_name: str
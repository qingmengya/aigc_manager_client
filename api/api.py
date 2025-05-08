import json
import os.path
from datetime import datetime
from fastapi import APIRouter

from models.api_models import CreateContainerReq
from utils.docker_utils import DockerUtils
from utils.resp import resp_success, resp_failed

router = APIRouter(prefix="/api", tags=["api"])


@router.get('/containers/freetime/{name}')
async def get_containers_free_time(name: str):
    """
    获取指定容器名的空闲时间
    :param name: str eg:sd-fangkaijing-20250428110101
    :return: {
        name: sd-fangkaijing-20250428110101
        status:running,
        free:1800
    }
    """
    is_running, container_id = DockerUtils.get_container_status_and_id(name)
    free_time = 99999999
    path = os.path.join('/var/lib/docker/containers', container_id, f'{container_id}-json.log')
    print(path)
    is_exists = os.path.exists(path)
    if is_exists:
        modification_time = os.path.getmtime(path)
        current_time = datetime.now().timestamp()
        free_time = int(current_time - modification_time)

    return resp_success(data={
        "name": name,
        "is_running": is_running,
        "free": free_time
    })


@router.get('/instances/freetime')
async def get_instances_free_time():
    """
    获取实例的空闲时间,没有一个运行的 docker 开始算空闲
    :return:
    """
    free_time = DockerUtils.get_instances_free_time()
    return resp_success(data=free_time)

@router.put('/containers/restart/{name}')
async def restart_container(name: str):
    """
    重启容器
    :param name:
    :return:
    """
    ok, msg = DockerUtils.restart_container(name)
    if ok:
        return resp_success(data=name)
    return resp_failed(data=None, message=msg)

@router.get('/containers/logs/{name}')
async def get_container_logs(name: str):
    """
    获取容器的日志
    :param name:
    :return:
    """
    is_running, container_id = DockerUtils.get_container_status_and_id(name)
    path = os.path.join('/var/lib/docker/containers', container_id, f'{container_id}-json.log')
    is_exists = os.path.exists(path)
    if is_exists:
        with open(path, 'r') as f:
            logs = json.loads(f.read())
        return resp_success(data=logs)
    return resp_failed(data=None, message='暂未找到日志')


@router.get('/containers/all/running')
async def get_containers():
    """
    获取所有运行的容器
    :return:
    """
    containers = DockerUtils.get_all_running_containers()
    return resp_success(data=containers)


@router.post('/containers/create')
async def create_container(request: CreateContainerReq):
    """
    创建容器
    :param
    :return:
    """
    image = request.image
    port = request.port
    container_name = request.container_name
    # 如果已经是存在且运行，就直接返回就行了。保证幂等
    all_containers = DockerUtils.get_all_running_containers()
    if all_containers and container_name in all_containers:
        return resp_success(data=container_name)
    ok, msg = DockerUtils.create_container(image, port, container_name)
    if ok:
        return resp_success(data=container_name)
    return resp_failed(data=None, message=msg)


@router.delete('/containers/delete/{name}')
async def delete_container(name: str):
    """
    删除容器
    :param name:
    :return:
    """
    ok, msg = DockerUtils.delete_container(name)
    if ok:
        return resp_success(data=name)
    return resp_failed(data=None, message=msg)


@router.get('/containers/health')
async def get_containers_health():
    return resp_success(data=DockerUtils.is_docker_running())

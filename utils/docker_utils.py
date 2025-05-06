import os.path
from datetime import datetime

import docker

from utils.resp import resp_success

docker_client = docker.from_env()


class DockerUtils:

    @staticmethod
    def get_container_status_and_id(container_name):
        try:
            container = docker_client.containers.get(container_name)
            if container.status == "running":
                return True, container.id
            else:
                return False, container.id
        except Exception as e:
            print(f"APIError: {e}")
            return False, ""

    @staticmethod
    def get_all_running_containers():
        """
        获取所有运行的容器
        :return:
        """
        containers = docker_client.containers.list(all=True)
        running_containers = []
        for container in containers:
            if container.status == "running":
                running_containers.append(container.name)

        return running_containers

    @staticmethod
    def get_instances_free_time():
        free_time = 0
        free_tag_path = os.path.join(os.path.expanduser('~'), "free_tag.txt")
        containers = docker_client.containers.list(all=True)
        running_containers = []
        for container in containers:
            if container.status == "running":
                running_containers.append(container.name)

        # 判断容器是否在运行
        if len(running_containers) == 0:
            if not os.path.exists(free_tag_path):
                open(free_tag_path, 'w').close()
            modification_time = os.path.getmtime(free_tag_path)
            current_time = datetime.now().timestamp()
            free_time = int(current_time - modification_time)
        else:
            if os.path.exists(free_tag_path):
                os.remove(free_tag_path)

        return free_time

    @staticmethod
    def create_container(image, port, container_name):
        """
        创建容器,幂等。同一个容器名不会重复创建
        :param image:
        :param port:
        :param container_name:
        :return:
        """
        image_name = 'sd-webui:1101'
        # if image == 'sd-webui-1.6.0':
        #     image_name = 'sd-webui-180:1'
        # elif image == 'sd-webui-1.10.1':
        #     image_name = 'sd-webui-180:1'
        # else:
        #     image_name = image
        print(f"image_name: {image_name}, port:{port}, name:{container_name}")

        try:
            container = docker_client.containers.run(
                image=image_name,
                name=container_name,
                detach=True,
                ports={f"{port}/tcp": port},
                volumes={
                    "/mnt/sdwebui_public/public/models/Stable-diffusion/": {
                        "bind": "/home/stable-diffusion-webui/models/Stable-diffusion",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/ControlNet/": {
                        "bind": "/home/stable-diffusion-webui/models/ControlNet",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/hypernetworks/": {
                        "bind": "/home/stable-diffusion-webui/models/hypernetworks",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/BLIP/": {
                        "bind": "/home/stable-diffusion-webui/models/BLIP",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/torch_deepdanbooru/": {
                        "bind": "/home/stable-diffusion-webui/models/torch_deepdanbooru",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/OpenTalker/": {
                        "bind": "/home/stable-diffusion-webui/models/OpenTalker",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/VAE/": {
                        "bind": "/home/stable-diffusion-webui/models/VAE",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/models/Lora/": {
                        "bind": "/home/stable-diffusion-webui/models/Lora/Lora",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/localizations20240322/": {
                        "bind": "/home/stable-diffusion-webui/localizations",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/outputs/": {
                        "bind": "/home/stable-diffusion-webui/outputs",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/embeddings/": {
                        "bind": "/home/stable-diffusion-webui/embeddings",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/samples/": {
                        "bind": "/home/stable-diffusion-webui/samples",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/styles/styles.csv": {
                        "bind": "/home/stable-diffusion-webui/styles.csv",
                        "mode": "rw"
                    },
                    "/mnt/sdwebui_public/public/config.json": {
                        "bind": "/home/stable-diffusion-webui/config.json",
                        "mode": "rw"
                    },
                    "/home/miniodata/.minio.sys/": {
                        "bind": "/home/stable-diffusion-webui/.minio.sys",
                        "mode": "rw"
                    }
                },
                runtime='nvidia',
                device_requests=[
                    docker.types.DeviceRequest(count=-1, capabilities=[['gpu']])
                ],
                privileged=True,
                remove=True,
                command=f"/home/miniconda3/envs/sd_python310/bin/python launch.py --port {port}"
            )
            return True, ""
        except Exception as e:
            print(f"APIError: {e}")
            return False, str(e)

    @staticmethod
    def delete_container(container_name):
        try:
            all_containers = DockerUtils.get_all_running_containers()
            # 已经没有了，直接返回
            if container_name not in all_containers:
                return True, ""
            container = docker_client.containers.get(container_name)
            container.stop(timeout=1)
            # container.remove()
            return True, ""
        except Exception as e:
            print(f"APIError: {e}")
            return False, f"删除容器失败：{e}"

    @staticmethod
    def is_docker_running():
        """
        查看 docker 是否启动
        :return:
        """
        try:
            docker_client.ping()
            return True
        except Exception as e:
            print(f"APIError: {e}")
            return False

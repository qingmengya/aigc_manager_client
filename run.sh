#!/usr/bin/env bash

function start() {
  # 验证 mnt 挂载
  while ! mountpoint -q /mnt ; do
      echo "waiting for /mnt to be mounted..."
      sleep 3
  done
  echo "mnt mount success"

  #验证minio启动，有些目录是从 minio 挂载的，一定要等minio 启动
  while ! curl  http://127.0.0.1:9003 >> /dev/null 2>&1 ; do
      echo "waiting for minio to be ready..."
      sleep 3
  done
  echo "minio ready"

  echo "starting dokcer..."

  run_client
}

function run_client() {
  git pull
  pip install -r requirements.txt
  python3 main.py
}


start
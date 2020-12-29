# ベースイメージ
FROM python:3.7-buster as base

RUN apt-get update \
    && apt-get install -y ca-certificates \ 
    && apt-get -y clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt .
RUN pip install -r requirements.txt


# Dev Container イメージ、docker-compose.yml の target
FROM base as devcontainer

RUN apt-get update \
    && apt-get install -y ffmpeg

WORKDIR /workspace
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt


# アプリケーション実行イメージ
FROM base as runner

WORKDIR /workspace
COPY rpi-sky-renderer.py .
CMD ["/workspace/rpi-sky-renderer.py"]

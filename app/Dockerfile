# ubuntuのイメージをプルし、Pythonをインストールしていく
FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

# pythonをインストール
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y python3.8 python3.8-dev \
    && source ~/.bashrc \
    && apt-get -y install vim


# 作業ディレクトリを設定
WORKDIR /usr/src/app


# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive


# pipとその他依存関係のインストール
RUN apt-get install -y curl \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && apt-get install -y python3.8-distutils \
    && apt-get install -y python3-distutils \
    && python3.8 get-pip.py \
    && pip install --upgrade pip \
    && apt-get install -y build-essential libssl-dev libffi-dev python-dev python3-dev libpq-dev


# install psycopg2 dependencies
#RUN apt-get -y install postgresql-dev gcc python3-dev musl-dev 


# install potgis dependencies
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y libgeos-dev binutils libproj-dev gdal-bin libgdal-dev \
    && apt-get install -y python3-gdal



# ホストのpipfileをコンテナの作業ディレクトリにコピー
COPY ./requirements.txt /usr/src/app/

# requirements.txtからパッケージをインストールしてDjango環境を構築
RUN pip install -r requirements.txt



RUN apt-get install -y netcat \
    && apt-get install -y expect


# entrypoint.shをコピー
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh


# ホストのカレントディレクトリ（現在はappディレクトリ）を作業ディレクトリにコピー
COPY . /usr/src/app/


# entrypoint.shを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
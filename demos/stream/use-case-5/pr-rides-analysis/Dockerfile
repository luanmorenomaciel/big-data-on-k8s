# FROM python:3.7-slim-stretch = [335 MB]

# docker image
FROM python:3.7-slim-stretch
MAINTAINER Luan Moreno M. Maciel <luan.moreno@owshq.com>

# copy requirements
COPY requirements.txt /

# install libraries
RUN pip install -r /requirements.txt
RUN pip install --upgrade pip

# copy files
COPY . /app

# set work directory
WORKDIR /app

# initiate app
ENTRYPOINT faust -A src.app worker -l info
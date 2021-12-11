# docker image
FROM python:3.9
LABEL Luan Moreno M. Maciel <luan.moreno@owshq.com>

# copy requirements
COPY requirements.txt /

# install libraries
RUN pip install -r /requirements.txt
RUN apt-get update -y && apt-get install -y curl

# copy files
COPY . /app

# set work directory
WORKDIR /app

# run program [exec]
CMD ["python","cli.py"]
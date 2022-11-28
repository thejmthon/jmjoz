FROM python:3.10-slim-buster

RUN apt update && apt upgrade -y
RUN apt install git -y

COPY requirements.txt /requirements.txt
RUN cd /
RUN pip3 install -U pip && pip3 install -U -r requirements.txt
RUN mkdir /sbb_b0
WORKDIR /sbb_b0
CMD ["python3","-m","sbb_b"]

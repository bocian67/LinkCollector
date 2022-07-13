# syntax=docker/dockerfile:1
FROM python:3.10.4-buster
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 9999
CMD [ "python3", "main.py"]
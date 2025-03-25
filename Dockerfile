FROM python:3.12

WORKDIR /workspace

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir -p /workspace/logs

RUN touch /workspace/logs/log.txt

COPY src/ .
FROM python:3.9.16-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PYTHONWARNINGS="ignore"
ENV DEBIAN_FRONTEND="noninteractive"
ENV TZ='Africa/Nairobi'

WORKDIR /project

RUN  apt-get -y update && apt-get -y --no-install-recommends install tzdata cron supervisor

COPY . .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && rm requirements.txt && mv supervisord.conf /etc/supervisord.conf
CMD ["supervisord","-c","/etc/supervisord.conf"]

FROM python:3.11.4
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron ffmpeg python3 python3-pip tree -y
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
RUN pip3 install piper-tts==1.2.0
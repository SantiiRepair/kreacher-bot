FROM python:3.11.1
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron ffmpeg python3 python3-pip tree -y
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
COPY . /kreacher/
WORKDIR /kreacher/
RUN pip3 install --no-deps -U pytgcalls==3.0.0.dev24 tgcalls==3.0.0.dev6 && pip3 install -r requirements.txt
CMD ["bash","scripts/setup.sh"]
CMD ["bash","scripts/start.sh"]
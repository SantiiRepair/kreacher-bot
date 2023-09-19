FROM python:3.11.1
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron ffmpeg python3 python3-pip tree -y
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
COPY . /kreacher/
WORKDIR /kreacher/
RUN make install
CMD ["bash","start.sh"]
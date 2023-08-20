FROM python:3.11.1
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron curl espeak expect ffmpeg git libespeak1 python3 python3-pip tree -y
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
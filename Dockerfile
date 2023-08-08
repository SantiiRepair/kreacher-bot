FROM python:3.11.1
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron curl expect ffmpeg git python3 python3-pip tree -y
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
COPY . /container/
WORKDIR /container/
RUN make install
CMD ["bash","start.sh"]
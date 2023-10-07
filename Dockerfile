FROM python:3.11.5
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron ffmpeg tree -y
RUN pip3 install -U pip
RUN pip3 install --upgrade pip
COPY . /kreacher/
WORKDIR /kreacher/
RUN pip install --no-deps -U pytgcalls==3.0.0.dev24 tgcalls==3.0.0.dev6 && pip install -r requirements.txt
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm -rf google-chrome-stable_current_amd64.deb; apt-get update
ENTRYPOINT ["python", "-m", "bot"]
FROM python:3.11.5
RUN apt-get update && apt-get upgrade -y
RUN apt-get install cron ffmpeg tree -y
RUN pip install --upgrade pip
COPY . /kreacher/
WORKDIR /kreacher/
RUN make install
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm -rf google-chrome-stable_current_amd64.deb; apt-get update
ENTRYPOINT ["python", "-m", "bot"]
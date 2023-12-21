FROM golang:1.21.5
RUN apt-get update && apt-get upgrade -y
RUN apt-get install git-all ffmpeg tree -y
COPY . /kreacher/
WORKDIR /kreacher/
RUN cp -r bin/* /usr/bin
RUN yt-dlp --update-to master
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm -rf google-chrome-stable_current_amd64.deb
RUN make install 
ENTRYPOINT ["make", "start"]
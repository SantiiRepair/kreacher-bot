FROM golang:1.21.5
RUN apt-get update && apt-get upgrade -y
RUN apt-get install ffmpeg tree -y
RUN go mod tidy
COPY . /kreacher/
WORKDIR /kreacher/
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm -rf google-chrome-stable_current_amd64.deb
RUN make install
ENTRYPOINT ["make", "start"]
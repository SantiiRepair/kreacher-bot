FROM golang:latest
COPY . /wd/
WORKDIR /wd/
RUN bash install.sh
RUN make install
ENTRYPOINT ["make", "start"]
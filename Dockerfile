FROM golang:latest
COPY . /wd/
WORKDIR /wd/
RUN bash setenv.sh
RUN make install
ENTRYPOINT ["make", "start"]
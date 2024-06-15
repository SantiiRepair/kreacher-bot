FROM golang:latest
COPY . /wd/
WORKDIR /wd/
RUN bash setup.sh
RUN make install
ENTRYPOINT ["make", "start"]
FROM golang:1.21.5
COPY . /kreacher/
WORKDIR /kreacher/
RUN bash setenv.sh
RUN make install
ENTRYPOINT ["make", "start"]
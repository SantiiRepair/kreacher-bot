FROM golang:1.21.5
COPY . /kreacher/
WORKDIR /kreacher/
CMD ["bash", "setenv.sh"]
ENTRYPOINT ["make", "start"]
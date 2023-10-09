FROM python:3.11.5
RUN apt-get update && apt-get upgrade -y
RUN apt-get install ffmpeg tree -y
RUN pip install --upgrade pip
COPY . /kreacher/
WORKDIR /kreacher/
RUN make install
CMD ["bash", "webdriver.sh"]
ENTRYPOINT ["make", "start"]
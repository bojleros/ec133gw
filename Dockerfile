FROM alpine
MAINTAINER Bartek R "bojleros@gmail.com"
RUN apk add --no-cache py3-flask \
  && apk add --no-cache --repository http://nl.alpinelinux.org/alpine/edge/testing py3-serial \
  && pip3 install modbus-tk \
  && rm -rf /var/cache/apk/*
ENV APP_DIR /app
COPY ec133gw/* /app/
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["main.py"]

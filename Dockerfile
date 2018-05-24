FROM bojleros/flask:0.0.1
MAINTAINER Bartek R "bojleros@gmail.com"
RUN apk add --no-cache --repository http://nl.alpinelinux.org/alpine/edge/testing py3-serial
ENV APP_DIR /app
COPY ec133gw/* /app/
WORKDIR /app
ENTRYPOINT ["python3"]
CMD ["main.py"]


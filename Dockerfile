FROM alpine:latest
RUN apk add --no-cache py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install paho-mqtt

#ARG INTERVAL=500
#ENV A_INTERVAL=$INTERVAL
#RUN echo "buildArgs demo:  INTERVAL=${INTERVAL} "


ENTRYPOINT ["python3"]
CMD ["app.py", "100", "500",  "1"]
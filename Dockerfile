from alpine:latest
RUN apk add --no-cache py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install paho-mqtt

ARG INTERVAL
ENV ainterval = $INTERVAL

ENTRYPOINT ["python3"]
CMD ["app.py", "5000", "${ainterval}",  "1"]
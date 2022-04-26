from alpine:latest
RUN apk add --no-cache py3-pip \
    && pip3 install --upgrade pip

WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install paho-mqtt

ENV INTERNAL = 300

ENTRYPOINT ["python3"]
CMD ["app.py", "5000", "${INTERVAL}",  "1"]
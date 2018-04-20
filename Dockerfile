FROM python:alpine3.7

RUN addgroup -g 1000 python \
    && adduser -u 1000 -G python -s /bin/sh -D python

COPY . /opt/app
WORKDIR /opt/app

RUN chmod g+rw /opt/app && \
    chown python:python /opt/app;

RUN python3 -m pip install -r requirements.txt

# Expose RethinkDB client port.
EXPOSE 28015

CMD ["python3", "main.py"]

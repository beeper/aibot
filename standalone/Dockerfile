FROM dock.mau.dev/maubot/maubot:standalone

ENV UID=1337 \
    GID=1337

COPY . /opt/beeper/aibot
WORKDIR /opt/beeper/aibot

RUN apk remove py3-sqlalchemy \
    && apk add --virtual .build-deps python3 python3-dev gfortran musl-dev libffi-dev build-base py3-numpy \
    && pip3 install --upgrade pip setuptools wheel \
    && pip3 install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

VOLUME /data

CMD ["/opt/beeper/aibot/standalone/docker-run.sh"]

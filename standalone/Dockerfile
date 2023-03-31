FROM dock.mau.dev/maubot/maubot:standalone

ENV UID=1337 \
    GID=1337

COPY . /opt/beeper/aibot
WORKDIR /opt/beeper/aibot

VOLUME /data

CMD ["/opt/beeper/aibot/standalone/docker-run.sh"]

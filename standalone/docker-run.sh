#!/bin/sh

function fixperms {
  chown -R $UID:$GID /var/log /data /opt/beeper
}

cd /opt/beeper/aibot

fixperms
exec su-exec $UID:$GID python3 -m maubot.standalone -m maubot.yaml \
  -c /data/config.yaml -b standalone/example-config.yaml

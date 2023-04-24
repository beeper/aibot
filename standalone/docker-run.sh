#!/bin/sh

function fixperms {
  chown -R $UID:$GID /var/log /data /opt/beeper
}

cd /opt/beeper/aibot

fixperms
exec su-exec $UID:$GID python3 -m maubot.standalone -m maubot.yaml \
  -c standalone/config.yaml -b standalone/example-config.yaml

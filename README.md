# aibot

A maubot for ChatGPT

## Building the standalone Docker image

Add config.yaml to standalone

```
$ docker build --tag aibot . -f standalone/Dockerfile
```

Or: run

```
python3 -m maubot.standalone -m maubot.yaml \
-c standalone/config.yaml -b standalone/example-config.yaml
```

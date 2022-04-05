#!/bin/bash
# https://zulip.com/api/writing-bots
source /home/zqli/workspace/python/server/python-zulip-api/zulip-api-py3-venv/bin/activate
zulip-run-bot jarvis --config-file /home/zqli/workspace/python/server/python-zulip-api/zuliprcs/zuliprc-jarvis

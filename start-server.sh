#!/bin/bash
# Serve research hub on port 8080
cd /root/.openclaw/workspace/research-hub
nohup python3 -m http.server 8080 --directory /root/.openclaw/workspace/research-hub &>/tmp/research-hub-server.log &
echo "Research hub server started on port 8080 (PID $!)"

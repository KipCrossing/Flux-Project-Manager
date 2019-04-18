#!/usr/bin/env bash


while true; do
  echo "git pull"
  git pull
  echo "Run projectbot.py"
  python3 projectbot.py &
  sleep 600
  pkill -9 -f projectbot.py
  echo "Killed and loop"
  sleep 5
done

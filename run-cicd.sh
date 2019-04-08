#!/usr/bin/env bash


while sleep 60; do
  echo "git pull"
  git pull
  echo "Run main.py"
  python3 main.py
done

#!/bin/bash

while true
do
  cd <insert bot path here>
  git fetch
  git pull
  echo "Next fetch in 1 minute"
  sleep 1m
done

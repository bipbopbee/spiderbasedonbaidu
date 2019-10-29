#!/bin/bash
content=$1
ps -ef | grep ${content} | grep -v grep | awk '{print $2}' | xargs kill -9

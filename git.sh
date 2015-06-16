#!/bin/bash

git init
git add .
git commit -m "first commit"
git remote add origin ssh://git@gitlab.mudan.com/tanhao/ipMonitor.git
git push -u origin master

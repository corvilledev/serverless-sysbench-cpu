#!/bin/bash

sudo apt update -q
sudo apt install -yq git
git submodule sync
git submodule update --init
ci-base/install.sh circleci sysbench
./run.sh

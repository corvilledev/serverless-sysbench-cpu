#!/bin/bash
export FLAVOR_NAME=machine_medium
export IMAGE_NAME=ubuntu

sudo apt update -q
sudo apt install -yq git
sudo git submodule sync
sudo git submodule update --init
ci-base/install.sh circleci sysbench
./run.sh

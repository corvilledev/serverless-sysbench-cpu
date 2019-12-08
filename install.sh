#!/bin/bash
ci-base/install_python.sh

sysbench_version=${sysbench_version:-1.0.8}

sudo apt -y -q install tee wget

wget -q https://github.com/akopytov/sysbench/archive/${sysbench_version}.tar.gz
tar xf ${sysbench_version}.tar.gz

cd sysbench-${sysbench_version}
./${1}_install.sh

make clean
./autogen.sh
./configure --without-gcc-arch --without-mysql
make
sudo make install

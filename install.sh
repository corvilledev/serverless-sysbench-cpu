#!/bin/bash
ci-base/install_python.sh

sysbench_version=${sysbench_version:-1.0.8}

sudo apt install tee


wget -q https://github.com/akopytov/sysbench/archive/${sysbench_version}.tar.gz
tar xf ${sysbench_version}.tar.gz

cd sysbench-${sysbench_version}
if [[ "$TRAVIS_CPU_ARCH" == ppc64le ]]; then
    # Use a luajit that supports ppc64{,le}
    rm -rf third_party/luajit
    git clone --single-branch --branch ppc64-port --depth 2 https://github.com/PPC64/LuaJIT.git third_party/luajit
    sed -i -e 's:third_party/luajit/Makefile::' configure.ac
    sed -i -e 's:luajit/inc:luajit/src:' -e 's:lib/libluajit-5.1.a:src/libluajit.a:'  m4/sb_luajit.m4
    # broken test
    rm tests/t/opt_luajit_cmd.t
fi

make clean
./autogen.sh
./configure --without-gcc-arch --without-mysql
make
sudo make install

#!/bin/bash

iterations=${iterations:-3}
threads="$(seq $(($(nproc)*2)))"

for i in $(seq 1 $iterations) ; do
    for thread in $threads ; do
        sysbench --threads=$thread --time=30 cpu --cpu-max-prime=64000 run | tee output-$i-$thread.txt
        cb-client sysbench_cpu < output-$i-$thread.txt
    done
done

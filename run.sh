#!/bin/bash

iterations=${iterations:-3}
nproc=$(nproc)
threads="$(for i in $(seq 0 9); do I=$(bc <<< "ibase=2; 10^$i") ; [[ "$I" -le "$((nproc*2))" ]] && echo $I ; done)"

for i in $(seq 1 $iterations) ; do
    for thread in $threads ; do
        sysbench --threads=$thread --time=30 cpu --cpu-max-prime=64000 run | tee output-$i-$thread.txt
        cb-client sysbench_cpu < output-$i-$thread.txt
    done
done

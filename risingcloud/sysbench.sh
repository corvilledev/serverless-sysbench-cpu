#!/bin/bash

threads=$(jq '.threads | values // 1' request.json)
time=$(jq '.time | values // 5' request.json)
max_prime=$(jq '.max_prime | values // 64000' request.json)

if [[ "$threads" =~ ^.*_cpu$ ]] ; then
    factor=$(echo "threads" | grep -oE '\d')
    cpu_number=$(nproc)
    threads=$((factor * cpu_number))
fi

echo sysbench --threads=$threads --time=$time cpu --cpu-max-prime=$max_prime run >&2

sysbench --threads=$threads --time=$time cpu --cpu-max-prime=$max_prime run

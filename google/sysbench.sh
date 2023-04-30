#!/bin/bash

# Read input from environment variables
threads=${THREADS:-1}
time=${TIME:-5}
max_prime=${MAX_PRIME:-64000}

if [[ "$threads" =~ ^.*_cpu$ ]] ; then
    factor=$(echo "threads" | grep -oE '\d')
    cpu_number=$(nproc)
    threads=$((factor * cpu_number))
fi

echo sysbench --threads=$threads --time=$time cpu --cpu-max-prime=$max_prime run >&2

sysbench --threads=$threads --time=$time cpu --cpu-max-prime=$max_prime run

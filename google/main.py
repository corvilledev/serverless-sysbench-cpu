import os
import subprocess
from google.cloud import functions

def run_sysbench(request):
    request_json = request.get_json(silent=True)

    threads = request_json.get('threads', 1) if request_json else 1
    time = request_json.get('time', 5) if request_json else 5
    max_prime = request_json.get('max_prime', 64000) if request_json else 64000

    cmd = f'./sysbench.sh {threads} {time} {max_prime}'
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')

    return {"result": result}


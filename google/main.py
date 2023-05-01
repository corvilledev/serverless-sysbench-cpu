import json
from flask import jsonify
from pyperformance.run import run_benchmarks

def run_sysbench(request):
    try:
        # Run the pyperformance benchmarks
        result = run_benchmarks(benchmarks=["bm_telco"], options=None)

        # Process the results
        result_json = json.dumps(result.as_dict(), indent=4)

        return jsonify({"status": "success", "message": "Pyperformance benchmarks have been executed.", "results": result_json})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



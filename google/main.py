import json
import importlib.util
import pkg_resources
import os
from pathlib import Path
from flask import jsonify, request

def run_sysbench(request):
    try:
        # Get the benchmark name from the query parameter
        benchmark_name = request.args.get('benchmark', 'bm_telco')

        # Validate the benchmark name
        benchmarks_path = pkg_resources.resource_filename('pyperformance', 'data-files/benchmarks')
        allowed_benchmarks = [p.name for p in Path(benchmarks_path).iterdir() if p.is_dir()]

        if benchmark_name not in allowed_benchmarks:
            return jsonify({"status": "error", "message": f"Invalid benchmark name. Allowed benchmarks: {', '.join(allowed_benchmarks)}"})
        
        # Load the chosen benchmark
        benchmark_file = os.path.join(benchmarks_path, benchmark_name, 'run_benchmark.py')
        spec = importlib.util.spec_from_file_location(f"{benchmark_name}_module", benchmark_file)
        benchmark_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(benchmark_module)

        # Run the chosen benchmark
        def run_benchmark(loops=1):
            filename = os.path.join(benchmarks_path, benchmark_name, "data", "telco-bench.b")
            return benchmark_module.bench_telco(loops, filename)

        result = run_benchmark()

        # Process the results
        result_dict = {"benchmark": benchmark_name, "result": result}
        result_json = json.dumps(result_dict, indent=4)

        return jsonify({"status": "success", "message": f"Pyperformance benchmark '{benchmark_name}' has been executed.", "results": result_json})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


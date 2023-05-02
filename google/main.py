import json
import importlib.util
import pkg_resources
import os
from pathlib import Path
from flask import jsonify, request
from concurrent.futures import ThreadPoolExecutor, as_completed

# Calculate allowed benchmarks once
benchmarks_path = pkg_resources.resource_filename('pyperformance', 'data-files/benchmarks')
ALLOWED_BENCHMARKS = [p.name for p in Path(benchmarks_path).iterdir() if p.is_dir()]

def run_benchmark(benchmark_name, loops):
    # Load the chosen benchmark
    benchmark_file = os.path.join(benchmarks_path, benchmark_name, 'run_benchmark.py')
    spec = importlib.util.spec_from_file_location(f"{benchmark_name}_module", benchmark_file)
    benchmark_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(benchmark_module)

    # Find the appropriate function to run the benchmark
    for attr_name in dir(benchmark_module):
        attr = getattr(benchmark_module, attr_name)
        if callable(attr) and attr_name.startswith('bench_'):
            benchmark_function = attr
            break
    else:
        raise RuntimeError(f"Unable to find a suitable function to run the benchmark '{benchmark_name}'")

    # Run the chosen benchmark
    if benchmark_name == "bm_telco":
        filename = os.path.join(benchmarks_path, benchmark_name, "data", "telco-bench.b")
        result = benchmark_function(loops, filename)
    else:
        result = benchmark_function(loops)

    return {"benchmark": benchmark_name, "result": result}

def run_sysbench(request):
    try:
        # Get the benchmark names from the query parameter
        req_data = request.get_json()
        benchmark_names = req_data.get("benchmark", ["bm_telco"])
        loops = req_data.get("loops", 1)

        try:
            loops = int(loops)
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid loops value. Must be an integer."})

        results = {}
        for benchmark_name in benchmark_names:
            # Validate the benchmark name
            if benchmark_name not in ALLOWED_BENCHMARKS:
                results[benchmark_name] = {"error": f"Invalid benchmark name. Allowed benchmarks: {', '.join(ALLOWED_BENCHMARKS)}"}
                continue

            # Load the chosen benchmark
            benchmark_file = os.path.join(benchmarks_path, benchmark_name, 'run_benchmark.py')
            spec = importlib.util.spec_from_file_location(f"{benchmark_name}_module", benchmark_file)
            benchmark_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(benchmark_module)

            # Find the appropriate function to run the benchmark
            for attr_name in dir(benchmark_module):
                attr = getattr(benchmark_module, attr_name)
                if callable(attr) and attr_name.startswith('bench_'):
                    benchmark_function = attr
                    break
            else:
                results[benchmark_name] = {"error": f"Unable to find a suitable function to run the benchmark '{benchmark_name}'"}
                continue

            # Run the chosen benchmark
            if benchmark_name == "bm_telco":
                filename = os.path.join(benchmarks_path, benchmark_name, "data", "telco-bench.b")
                result = benchmark_function(loops, filename)
            else:
                result = benchmark_function(loops)

            results[benchmark_name] = {"benchmark": benchmark_name, "result": result}

        # Process the results
        result_json = json.dumps(results, indent=4)

        return jsonify({"status": "success", "message": "Pyperformance benchmarks have been executed.", "results": result_json})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

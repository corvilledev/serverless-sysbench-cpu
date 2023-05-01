import json
from flask import jsonify, request
from pyperformance.run import run_benchmarks

def run_sysbench(request):
    try:
        # Get the benchmark name from the query parameter
        benchmark_name = request.args.get('benchmark', 'bm_telco')

        # Validate the benchmark name
        allowed_benchmarks = [
            'bm_2to3', 
            'bm_async_generators', 
            'bm_async_tree',
            'bm_asyncio_tcp',
            'bm_chameleon',
            'bm_chaos',
            'bm_comprehensions',
            'bm_concurrent_imap',
            'bm_coroutines',
            'bm_coverage',
            'bm_crypto_pyaes',
            'bm_dask',
            'bm_deepcopy',
            'bm_deltablue',
            'bm_django_template',
            'bm_docutils',
            'bm_dulwich_log',
            'bm_fannkuch',
            'bm_float',
            'bm_gc_collect',
            'bm_gc_traversal',
            'bm_generators',
            'bm_genshi',
            'bm_go',
            'bm_hexiom',
            'bm_hg_startup',
            'bm_html5lib',
            'bm_json_dumps',
            'bm_json_loads',
            'bm_logging',
            'bm_mako',
            'bm_mdp',
            'bm_meteor_contest',
            'bm_nbody',
            'bm_nqueens',
            'bm_pathlib',
            'bm_pickle',
            'bm_pidigits',
            'bm_pprint',
            'bm_pyflate',
            'bm_python_startup',
            'bm_raytrace',
            'bm_regex_compile',
            'bm_regex_dna',
            'bm_regex_effbot',
            'bm_regex_v8',
            'bm_richards',
            'bm_richards_super',
            'bm_scimark',
            'bm_spectral_norm',
            'bm_sqlalchemy_declarative',
            'bm_sqlalchemy_imperative',
            'bm_sqlglot',
            'bm_sqlite_synth',
            'bm_sympy',
            'bm_telco',
            'bm_tomli_loads',
            'bm_tornado_http',
            'bm_typing_runtime_protocols',
            'bm_unpack_sequence',
            'bm_xml_etree'                     
        ]

        if benchmark_name not in allowed_benchmarks:
            return jsonify({"status": "error", "message": f"Invalid benchmark name. Allowed benchmarks: {', '.join(allowed_benchmarks)}"})

        # Run the pyperformance benchmarks
        result = run_benchmarks(benchmarks=[benchmark_name], options=None)

        # Process the results
        result_json = json.dumps(result.as_dict(), indent=4)

        return jsonify({"status": "success", "message": f"Pyperformance benchmark '{benchmark_name}' has been executed.", "results": result_json})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

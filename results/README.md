# Example results

Both folders are **synthetic, classical executions**. `signed-graph/` contains exact enumeration and classical simulated annealing; `synthetic-vectors/` contains PCA/k-means on generated numerical vectors. Neither contains source music or real tune rows.

Each `run.json` records the UTC execution time, input/manifest hashes, hashes of the analysis modules, dependency versions, settings and output hashes. Timings and timestamps are not performance comparisons. Re-run into a new ignored `local-runs/` directory; never overwrite saved outputs.

The IrishMAN baseline verification is aggregate-only and lives in `docs/baseline-verification.json`. Its input is not publicly redistributed.

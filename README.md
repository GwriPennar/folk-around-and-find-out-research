# Quantum-assisted discovery of related folk melodies

**A hybrid quantum-classical approach to musical similarity and clustering.**

Folk melodies change as people play, remember and adapt them. Finding related versions means weighing many similarities that can disagree. We investigate whether quantum annealing can help organise those relationships into useful groups, with classical computing preparing the musical evidence and evaluating the answers.

This is research into **quantum-assisted unsupervised learning**, within the broad QML umbrella. Our specific quantum method is annealing for combinatorial optimisation. The examples executed in this release are classical; neither PCA nor classical simulated annealing is a quantum computation. We claim no quantum advantage.

## Why give this problem to a quantum annealer?

A resembles B, B resembles C, yet A and C may disagree. Pairwise scores alone do not select a consistent grouping. Assignments, competing relationships and constraints create a combinatorial search problem that can be expressed as a binary quadratic model. Quantum annealing is a candidate way to search that model; whether it helps is the experiment, not the premise.

**Our pipeline:** notation → classical features → similarity graph → optimisation model → classical / direct-QPU / managed-hybrid solver → constraint checks and musical review.

Our overall hybrid workflow and D-Wave's managed hybrid solver service are different things. We will report direct-QPU and managed-hybrid experiments separately, with end-to-end costs and strong classical controls.

## Read the research

- [Research brief](docs/research-brief.md): motivation, past formulations, evidence and next experiments.
- [Download the PDF](docs/Quantum-Assisted-Folk-Research.pdf): self-contained research briefing.
- [48-tune classical baseline](docs/classical-baseline.md): features, axes, K comparisons and local replay instructions.
- [Synthetic annealing formulation](docs/annealing-model.md): all 64 assignments, QUBO equations and classical sampling.
- [Evidence register](docs/evidence.md) and [data/publication boundary](docs/data-boundary.md).
- [Immersive briefing](https://folk-around-and-find-out.ark1v3.chatgpt.site/) and [official NQCC event account](https://www.nqcc.ac.uk/uk-quantum-hackathon-2026/).

## Run without private data or quantum access

Python 3.12:

```sh
python -m venv .venv
# Activate the environment using your shell's normal command.
python -m pip install -r requirements.txt
python -m unittest discover -s tests
python -m folk_research.annealing --input examples/signed-graph.json --manifest examples/signed-graph.manifest.json --output-dir local-runs/graph-001
python -m folk_research.classical --input examples/synthetic-vectors.json --manifest examples/synthetic-vectors.manifest.json --output-dir local-runs/vectors-001
```

Choose a new output directory for every run. Both supplied inputs are synthetic: six artificial graph nodes and 48 artificial 16D vectors. They are not melodies, musical-family evidence or a reproduction of the IrishMAN result. No credentials, network requests or provider calls are used by the analysis modules.

The thin [research notebook](notebooks/research-journey.ipynb) calls the same modules. Install `requirements-dev.txt` for notebook execution and PDF tooling. Committed notebook outputs are cleared. Saved [example outputs](results/README.md) include figures, scores and hashed run records.

The real 48-tune analysis was replayed locally. Record-level IrishMAN inputs are withheld pending clarification of redistribution terms; public readers can inspect the explanation and run the same replay code with authorised local inputs. See the exact distinction in the [baseline guide](docs/classical-baseline.md).

## Research direction

D-Wave is the primary quantum route. First establish useful musical evidence, then compare identical bounded optimisation problems using exact methods, strong classical solvers, classical simulated annealing, direct QPU and managed hybrid routes. Signed-graph grouping and paths of related songs are proposed extensions. IBM/Qiskit remains a separate project.

Website implementation, player code, raw music, private research history and correspondence are excluded. See [PUBLISHING.md](PUBLISHING.md) for the short release process. The code's MIT licence does not grant rights to third-party datasets.

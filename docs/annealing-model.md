# A small annealing problem you can inspect completely

This example is synthetic. A-F are artificial nodes, not tunes. Positive weights favour putting endpoints together; negative weights favour separating them. There are no fixed group sizes. An assignment can put every node on the same side; the objective, not a hidden constraint, decides whether that is worthwhile.

For binary group assignments x_i in {0,1}, let d_ij = x_i + x_j - 2*x_i*x_j, which is 1 exactly when the endpoints differ.

Minimise disagreement:

```
C(x) = sum over positive edges w_ij * d_ij
     + sum over negative edges |w_ij| * (1 - d_ij)
```

Thus, with each undirected edge stored once:

```
linear[i]      = sum of signed weights incident to i
quadratic[i,j] = -2 * w_ij
constant      = sum of |w_ij| over negative edges
```

The constant matters when comparing physical objective values. In this upper-triangular QUBO convention each pair is counted once; do not double it using a symmetric matrix multiplication without adjusting coefficients. No variable-fixing or group-size penalty is added. Complementing all bits gives the same partition and energy.

The triangle A-B-C contains two positive edges and one negative edge, so all preferences cannot hold simultaneously. Missing links contribute zero. The committed graph has an exact minimum disagreement of 2 and two complementary optimal bit strings, `000111` and `111000`, in A-F order.

## What runs

`folk_research.annealing` enumerates all 64 assignments and compares QUBO energy with an independently written edge-disagreement calculation. Its small Metropolis simulated annealer uses 10 fixed seeds, 64 reads per seed, 100 sweeps, and a geometric temperature schedule from 4.0 to 0.05. Each sweep attempts each variable once in shuffled order. Each returned sample is the best state seen during that read, not a Boltzmann sample or a calibrated uncertainty estimate.

The saved run reached the optimum in 640 of 640 best-so-far reads. That result concerns an easy, tiny synthetic example and these settings. It says nothing about quantum performance, large-instance scaling or musical validity. Tests do not require stochastic success on every read: they verify reproducibility, valid energies and exact lower bounds.

Outputs include all enumerated energies, all sampled results, a BQM coefficient file, a figure and a hashed run record. The displayed node positions are a circular layout, not musical distances. Node colours show one exact optimum.

## How the same model becomes QPU input

The `bqm.json` output describes binary linear biases, pairwise biases and a constant offset. A future Ocean adapter can construct a binary `dimod.BinaryQuadraticModel` from those coefficients and submit it through an embedding composite and QPU sampler. This release intentionally contains no executable provider submission or credentials.

Before a real run, verify coefficient scaling, embedding, chain-strength choices and decoding; record the solver identity, logical/physical problem size, reads, timing and constraint/objective checks. Re-evaluate returned assignments using the original graph objective. Compare against exact solutions where feasible and strong classical heuristics at larger sizes. Quantum annealing samples low-energy assignments; optimality is not guaranteed.

A managed-hybrid submission is a separate solver lane. Neither route makes this two-way partition automatically solve unknown-K clustering, minimum-weight song paths or musical-family discovery.

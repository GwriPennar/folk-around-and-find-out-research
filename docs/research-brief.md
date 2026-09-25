# Quantum-assisted discovery of related folk melodies

## 1. The musical challenge and quantum motivation

A hybrid quantum-classical approach to musical similarity and clustering.

Folk melodies change as people play, remember and adapt them. Finding related versions means weighing many similarities that can disagree. We investigate whether quantum annealing can help organise those relationships into useful groups, with classical computing preparing the musical evidence and evaluating the answers.

The NQCC hackathon use case concerned discovery of melodic variant families in folk-music archives. Team 8's continuation asks two distinct questions: do our measurements capture musically meaningful relationships, and can a quantum optimiser improve the search over possible groupings?

A pair of tunes can resemble one another in contour but differ in rhythm or ornamentation. Pairwise preferences can conflict across a whole collection. Choosing group memberships while respecting these relationships and constraints is a combinatorial optimisation task. Binary choices and pairwise interactions can be represented as a QUBO/BQM, making quantum annealing a plausible method to investigate. The mapping itself is not evidence of speedup or usefulness.

Quantum-assisted unsupervised learning is an appropriate qualified QML description for the research programme. Our method is quantum annealing for an optimisation stage; we are not demonstrating a quantum neural network, quantum feature extraction or quantum PCA. Graph partitioning with annealers has published precedent, so we do not claim that this mapping is novel.

## 2. Where quantum enters the hybrid pipeline

Notation → classical parsing and features → similarity graph → optimisation model → solver → validation and musical interpretation.

Classical preparation converts symbolic music into measurements and candidate relationships. A graph expresses those relationships. We then choose an objective and constraints, encode them mathematically and send the same bounded problem to comparable solvers. The returned assignments must be checked against the original objective and constraints before assessing musical value.

Three solver lanes remain separate: strong classical methods, direct-QPU annealing, and a managed quantum-classical hybrid service. Our pipeline is hybrid whenever classical preparation/evaluation surrounds a quantum stage. That does not mean every local example uses quantum hardware. D-Wave's managed hybrid service combines solver components internally; a successful service result alone does not measure the quantum contribution.

PCA is a classical display method. K-means is a classical clustering baseline. Simulated annealing is also classical. These methods let us investigate representation quality and establish controls before attributing any benefit to a QPU.

## 3. What the team tried and reported

The original assignment model gives each tune one yes-or-no variable per possible group. Similarity rewards encourage related tunes to share a group. Penalties enforce exactly one assignment per tune and fixed group sizes.

The 12-tune case prescribed three groups of four: 36 logical binary variables and 234 interactions. The 24-tune case prescribed six groups of four: 144 variables and 2,016 interactions. The event material reports an embedding using 1,764 physical qubits for the latter. Logical variables and physical qubits are different quantities: embedding can use chains of physical qubits to represent one logical variable.

These are controlled recovery tests, not unrestricted discovery of the number or sizes of families. The optimiser is given structural information even though the reference family identities are withheld from fitting.

Historical-reported: the small direct-QPU test matched the classical simulated-annealing result, with reference ARI 1. The 24-tune direct-QPU penalty sweep returned no fully feasible samples. A separate managed-hybrid CQM report records 108 feasible samples out of 125 and ARI 1 for the reported solution. These event observations have not been independently rerun in this public release or tied to a complete public provider record. They are not a controlled quantum-advantage comparison.

Saved local computation with an updated parser found matching valid solutions on bounded assignment cases using classical simulated annealing. Those computations cannot be combined with older event energies as one controlled experiment. Larger 48- and 145-tune studies did not establish reliable family recovery. Optimising a supplied score more effectively can still miss musical relationships.

## 4. What the classical evidence tells us

The selected 48-tune baseline uses 16 standardised summary measurements, k-means in the full feature space and PCA only for display. Six provisional reference groups of eight were selected deliberately; this is not a random archive sample. K=6 is an inherited comparison point, not a discovered optimum.

The first three components explain 45.38%, 20.40% and 11.96% of feature variance, totalling 77.74%. This is variance retained, not musical accuracy. At K=6 the silhouette is 0.275489 and reference ARI is 0.365545. Among K=2 through 8, silhouette prefers K=7 and reference agreement prefers K=8. Neither establishes the true family count.

Three length columns are perfectly correlated in this cohort and one feature is constant. Summary features discard much of melodic order. In a later feature-removal exploration, reducing redundancy changed geometry but did not consistently improve clustering. These findings motivate representation experiments, not a blanket conclusion that one model is better.

A separate 958-record exploration removed the 42 overlapping benchmark IDs from a strict 1,000-record pool, leaving no IDs from the 48-tune benchmark. ID disjointness does not exclude musical relatives or create an independent population holdout. Its rhythm study showed that ABC note-unit conventions affect features; normalising units changed neighbours and partitions without proving improved musical correctness. These later studies are summarised as exploratory local work, not independently reproduced public benchmarks.

## 5. The next quantum question

A proposed signed graph distinguishes evidence favouring joining from evidence favouring separation. Missing edges mean no encoded evidence. A binary split can use one logical variable per tune, avoiding the original one-hot assignment structure. This is a different problem and does not make unrestricted multi-family discovery a six-variable task.

Our public six-node synthetic demonstrator verifies this mapping against all 64 assignments and compares classical simulated annealing. It has deliberately conflicting edges. It is an explanation and correctness control, not a musical benchmark, scalability demonstration or quantum run.

Future D-Wave experiments should freeze the graph, objective, grouping rules and resource budget. Compare feasibility, objective value, stability and end-to-end cost across repeated runs and strong classical controls. Measure musical usefulness separately using defensible held-out labels and listening/domain review. Any recursive splitting scheme needs explicit stopping and complexity rules; we do not implement it here.

Song paths are a further possible optimisation task: order songs so adjacent links express resemblance. A path of similarities is not proof of historical evolution. IBM/Qiskit stays a separate notebook project. Negative or inconclusive annealing results remain scientifically useful when the experiment and limitations are clear.

## References and release boundary

- [Official NQCC hackathon account](https://www.nqcc.ac.uk/uk-quantum-hackathon-2026/).
- [Graph Partitioning using Quantum Annealing on the D-Wave System](https://arxiv.org/abs/1705.03082).
- [D-Wave: hybrid computing](https://docs.dwavequantum.com/en/latest/concepts/hybrid.html).
- [Evidence register](evidence.md): source and reproduction status for the numerical statements.
- [Data boundary](data-boundary.md): IrishMAN record-level inputs are not redistributed.

This is a public research briefing, not a peer-reviewed paper or an advantage claim. Required copyright attribution is retained; contributor rosters and private correspondence are excluded.

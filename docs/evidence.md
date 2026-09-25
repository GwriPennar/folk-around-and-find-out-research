# Evidence register

| ID | Bounded statement | Evidence status | Source / verification | Limitation |
|---|---|---|---|---|
| E01 | The event reports small direct-QPU and hybrid-CQM results, plus failed larger cases. | historical-reported | Team 8 final presentation pp.6-13 and technical report pp.1-3; public narrative in the linked briefing | Original artefacts and complete provider records are not distributed; not independently reproduced here. |
| E02 | The saved 48-record vectors reproduce the baseline's seven partitions, PCA geometry and scores. | locally-reproduced; inputs withheld | This release's classical module was run against the frozen local numeric input; see baseline-verification.json | Computational agreement, not musical validation; public checkout lacks the IrishMAN input. |
| E03 | All 64 synthetic graph assignments have matching independent and QUBO energies. | publicly-reproducible | results/signed-graph, input manifest, module and tests | Six artificial nodes; no QPU execution. |
| E04 | The synthetic PCA/k-means workflow runs without musical data. | publicly-reproducible | results/synthetic-vectors, generator, manifest and module | Artificial features and labels; no musical interpretation. |
| E05 | Removing duplicate length features did not consistently improve the 48-record exploration. | exploratory-local; summarised | Saved 9 September 2026 feature-ablation report, 20 seeds per K | Full experiment not independently rerun in this release. |
| E06 | The 958-record analysis found sensitivity to rhythm-unit normalisation. | exploratory-local; summarised | Saved 9 September 2026 discovery and rhythm reports | One seed with multiple starts; ID disjointness is not population independence. |
| E07 | Signed grouping, path objectives and controlled QPU comparisons could extend the research. | planned | Research brief, section 5 | No performance or historical-evolution claim. |

The older 12/24 assignment model, the classical 48-record feature model and the synthetic signed graph are different formulations. Their energies and scores must not be pooled. The updated Living Notebook provider record says NOT_RUN; it must not be treated as the event's hardware evidence.

Source index: [NQCC](https://www.nqcc.ac.uk/uk-quantum-hackathon-2026/), [public project briefing](https://folk-around-and-find-out.ark1v3.chatgpt.site/), [annealing graph-partitioning precedent](https://arxiv.org/abs/1705.03082), [D-Wave hybrid methods](https://docs.dwavequantum.com/en/latest/concepts/hybrid.html), [scikit-learn PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html), [scikit-learn k-means](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html).

The replay design and 48-tune explanation are adapted from Team 8's private classical-ML research brief and replay script (16 September 2026), with the existing project copyright notice preserved. Public adaptation removes website dependencies and adds explicit input/manifest handling. Private source locators and personal attributions are not reproduced.

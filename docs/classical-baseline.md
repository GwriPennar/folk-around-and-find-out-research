# The classical musical baseline within the hybrid programme

This investigates the measurements that may feed an optimiser. It is entirely classical. The numerical findings below describe a selected IrishMAN cohort; the public runnable fixture is synthetic and has different scores.

## What the map represents

The example contains 48 IrishMAN tune records selected into six provisional reference groups of eight. Those reference labels are used for comparison after fitting; they are not inputs to k-means. This selected benchmark is useful for controlled exploration, not an unbiased sample of the full archive or a demonstration of natural family sizes.

Each particle represents one record. K-means assigns its colour; principal component analysis (PCA) supplies its three-dimensional position. The six displayed colours come from the inherited choice **K=6**. K-means discovers assignments for that requested number of groups; it does not independently discover that six is the correct number.

The current map is the Living Notebook integration baseline. It is distinct from the earlier ten-feature exploratory work and the saved UberMAX PCA/MiniBatch pipeline. Do not transfer the 48-tune axes or scores to either of those studies.

## From notation to the three axes

The saved feature table has 16 columns: note, event and interval counts; pitch range and distinct-pitch count; rest proportion; mean absolute interval, interval standard deviation and interval entropy; descending, repeated and ascending-note proportions; step and leap proportions; mean duration and duration standard deviation.

Each column is standardised across these 48 records: subtract its mean and divide by its standard deviation, with constant columns remaining zero. This puts different measurement scales on a comparable footing. It does not make them equally meaningful musically or remove redundancy.

The same 16D table feeds two separate operations:

1. **K-means** groups records by Euclidean distance using all 16 dimensions, with seed 42 and 20 initialisations.
2. **PCA** finds mutually perpendicular weighted combinations of the measurements, ordered by the variance they capture. The first three supply X, Y and Z for display. They are not time, geographic coordinates or three individual musical properties.

| Display axis | Main influences in this fitted model | Feature variance retained |
|---|---|---:|
| X = PC1 | Interval variability (+0.31), interval entropy (+0.31), pitch range (+0.29), repetition (-0.29) | 45.38% |
| Y = PC2 | Leap proportion (+0.37), mean absolute interval (+0.32), note and event counts (each -0.29) | 20.40% |
| Z = PC3 | Step proportion (+0.47), repetition (-0.45), ascending (+0.32) and descending (+0.31) proportions | 11.96% |

These are the largest coefficients, not complete formulas. Together the axes retain **77.74% of variance in the standardised measurements**, not 77.74% musical accuracy. Axis signs can reverse without changing relationships. All axes use one common spatial scale. Camera movement and colour changes do not alter the fitted clustering.

## What the current results tell us

At K=6, the silhouette is 0.2755 and adjusted Rand index (ARI) against the provisional reference labels is 0.3655. Silhouette compares within-group closeness with separation from other groups; it is not a correctness percentage. ARI measures agreement between two partitions after adjusting for chance; it is not the proportion of tunes classified correctly.

| K | Silhouette in 16D | Reference-group ARI |
|---:|---:|---:|
| 2 | 0.250472 | 0.124536 |
| 3 | 0.264249 | 0.265215 |
| 4 | 0.270938 | 0.298209 |
| 5 | 0.263168 | 0.364612 |
| 6 | 0.275489 | 0.365545 |
| 7 | 0.279217 | 0.327112 |
| 8 | 0.269133 | 0.393816 |

The two measures prefer different choices within the tested range. Neither establishes an optimal musical K. We need stable results under resampling, a stated definition of musical relatedness and independent listening or domain review.

On average, 70.42% of each tune's five nearest neighbours remain neighbours in the 3D view. Some apparent neighbours are projection artefacts, so the inspector uses distances in all 16 dimensions. A shared colour or a short distance is a candidate relationship to investigate, not proof of a shared melody or ancestry.

Three length columns are perfectly correlated in this sample, and rest proportion is constant. The summaries also discard much of the order of notes. These limitations motivate testing feature weighting and sequence-aware similarity; a more powerful optimiser cannot repair an unsuitable musical representation by itself.

## Replaying authorised local inputs

This module starts from **saved standardised vectors**, not raw notation. It does not re-parse the archive, re-extract features or re-standardise those vectors. The existing 48-record numeric export is a JSON object with `points` (each with `id`, `family`, a 16-value `vector` and saved three-value `xyz`), `pca.variance` and `models` for K=2 through 8 with saved `labels`, `silhouette` and `ari`.

Use an authorised local export, stored outside version control. A manifest binds its exact bytes; making a manifest does not establish provenance or permission. Collaborators should compare its hash with the aggregate verification record and the original source manifest.

```sh
python tools/local_manifest.py --input local-inputs/living.json --output local-inputs/living.manifest.json
python -m folk_research.classical --input local-inputs/living.json --manifest local-inputs/living.manifest.json --output-dir local-runs/irishman-001
```

The replay checks every partition up to label permutation, silhouette and reference ARI, PCA explained variance, and pairwise distances in the three displayed components. This preserves geometry when PCA signs reverse. A mismatch is an error rather than a silently updated baseline.

The release includes no IrishMAN rows or real tune coordinates. The generated `examples/synthetic-vectors.json` is a separate teaching fixture with arbitrary numeric dimensions and known generation labels. Its coordinates and loadings have no musical meaning.

## Where listening fits

The separately hosted/private-source observatory can identify a selected tune and, when authorised local notation is available, synthesise it for comparison. That is a qualitative inspection aid, not validation by itself. This research release exports a static figure and analysis tables; it does not include the website player or music.

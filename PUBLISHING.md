# Publishing research safely

1. Work in the private development repository. Copy only intended research changes to a branch here; never merge private history. Keep website/player source, correspondence, raw notation, audio and record-level IrishMAN inputs out. New data needs explicit redistribution evidence.
2. Run the tests, both synthetic examples, notebook and publication check. Use a new local-runs directory for each run. Check claims against the evidence register; label historical, reproduced, synthetic and proposed results separately.
3. Review the full diff and PDF pages. The publication policy lists reviewed files and binary hashes; update it deliberately after reviewing new files or regenerated figures/PDFs. Preserve licence notices. Cleared notebook outputs are required. Automated checks assist review; they cannot establish data rights or absence of every possible secret.
4. Use one public PR, require successful CI, review and merge, then tag the release and update the separately hosted briefing. Repository ownership and Git commit identities remain visible.

Run `python tools/check_publication.py` and `python tools/verify_release.py` after installing requirements-dev.txt. The latter executes the notebook in memory and compares regenerated synthetic results with the saved release evidence. It makes no provider calls.

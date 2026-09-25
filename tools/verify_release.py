"""Reproduce public examples and notebook without changing tracked outputs."""
from pathlib import Path
import json, tempfile, sys, math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from folk_research import annealing, classical
from folk_research.records import digest
from nbclient import NotebookClient
import nbformat
def same(a,b):
    if isinstance(a,float) and isinstance(b,(float,int)): return math.isclose(a,b,rel_tol=1e-8,abs_tol=1e-10)
    if isinstance(a,dict) and isinstance(b,dict): return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list) and isinstance(b,list): return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
for directory in (ROOT/'results').iterdir():
    if not directory.is_dir(): continue
    record=json.loads((directory/'run.json').read_text())
    for name,expected in record['output_sha256'].items():
        if digest(directory/name)!=expected: raise AssertionError('Saved output digest mismatch')
    for name,expected in record['code_sha256'].items():
        if digest(ROOT/'folk_research'/name)!=expected: raise AssertionError('Source digest mismatch')
with tempfile.TemporaryDirectory(prefix="folk-reproduction-") as tmp:
    for module, name, result in [(annealing,"signed-graph","signed-graph"),(classical,"synthetic-vectors","synthetic-vectors")]:
        out=Path(tmp)/name
        module.run(ROOT/f"examples/{name}.json",ROOT/f"examples/{name}.manifest.json",out)
        actual=json.loads((out/"summary.json").read_text())
        expected=json.loads((ROOT/f"results/{result}/summary.json").read_text())
        if not same(actual,expected): raise AssertionError(f"Saved summary differs: {name}")
    notebook=nbformat.read(ROOT/"notebooks/research-journey.ipynb",as_version=4)
    NotebookClient(notebook,timeout=180,kernel_name="python3",resources={"metadata":{"path":str(ROOT)}}).execute()
print("Both synthetic summaries reproduced; notebook executed without saved outputs or provider calls.")

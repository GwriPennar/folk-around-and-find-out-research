"""Small, inspectable input and run records; never record local absolute paths."""
import hashlib
import json
import platform
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_input(input_path, manifest_path, expected_kind=None):
    manifest = json.loads(Path(manifest_path).read_text())
    if manifest.get('input_sha256') != digest(input_path):
        raise ValueError('Input digest does not match the manifest')
    if expected_kind and manifest.get('kind') != expected_kind:
        raise ValueError('Unexpected input kind')
    return json.loads(Path(input_path).read_text()), manifest

def new_output(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=False)
    return path

def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')

def record_run(output, input_path, manifest_path, configuration, summary):
    record = dict(evidence_state='local-classical', executed_at_utc=datetime.now(timezone.utc).isoformat(),
                  input_sha256=digest(input_path), manifest_sha256=digest(manifest_path),
                  code_sha256={p.name: digest(p) for p in sorted(Path(__file__).parent.glob('*.py'))},
                  python=platform.python_version(),
                  packages={p: version(p) for p in ['numpy','scikit-learn','matplotlib','scipy','threadpoolctl']},
                  configuration=configuration, summary=summary,
                  output_sha256={p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()})
    write_json(output/'run.json', record)

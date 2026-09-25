"""Bind an authorised local numeric export to its digest; does not grant data rights."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
with a.output.open('x') as f:
 json.dump(dict(schema_version=1,kind='local-irishman48-standardised-vectors',input_sha256=hashlib.sha256(a.input.read_bytes()).hexdigest()),f,indent=2)
 f.write('\n')

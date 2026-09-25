"""A small publication check: source files, approved binary assets and built output.
Prints locations/categories only, never matched private values. No network writes.
"""
from pathlib import Path
import argparse,base64,hashlib,io,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
SKIP={'.git','node_modules','dist','export','__pycache__','.venv','.sites-runtime','local-runs','local-inputs'}
PATTERNS={
 'personal-email':re.compile(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}',re.I),
 'local-machine-path':re.compile(r'/(?:Users|home)/[^\s/]+|[A-Z]:\\Users\\',re.I),
 'private-collaboration-link':re.compile(r'(?:[\w-]+\.slack\.com|mail\.google\.com|docs\.google\.com|colab\.research\.google\.com)',re.I),
 'private-key':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'access-token':re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{30,}|(?:DEV|PROD)-[a-f0-9]{32,})'),
}
FORBIDDEN_SUFFIX={'.abc','.mid','.midi','.mp3','.wav','.flac','.parquet','.pkl','.pickle','.sqlite','.db','.zip','.tar','.gz','.tsx','.js','.mjs','.html','.css'}
FORBIDDEN_PARTS={'private','recovery','correspondence','local-data','local-runs','sites','vendor'}
TEXT_SUFFIX={'.py','.md','.txt','.ts','.tsx','.js','.mjs','.json','.yaml','.yml','.html','.css','.svg','.csv','.cff','.toml','.ipynb'}

def text_findings(text,policy):
 for path,entry in policy.get('licence_exceptions',{}).items():
  licence=ROOT/path
  if licence.is_file() and hashlib.sha256(licence.read_bytes()).hexdigest()==entry['sha256']:
   text=text.replace(licence.read_text(),'')
 findings=[key for key,rx in PATTERNS.items() if rx.search(text)]
 terms=set(re.findall(r'[A-Za-z]+',text.casefold()))
 if any(hashlib.sha256(term.encode()).hexdigest() in policy.get('name_term_hashes',[]) for term in terms):findings.append('team-name')
 # Portable HTML embeds Markdown/JSON downloads; inspect those as well.
 for encoded in re.findall(r'data:(?:text/(?:plain|markdown)|application/json);base64,([A-Za-z0-9+/=]+)',text):
  try:findings+=text_findings(base64.b64decode(encoded).decode('utf8'),policy)
  except (ValueError,UnicodeError):findings.append('unreadable-embedded-document')
 return sorted(set(findings))

def scan(root,policy,build=False):
 findings=[];files=[]
 for path in sorted(root.rglob('*')):
  rel=path.relative_to(root)
  if any(part in SKIP for part in rel.parts) or path.name in {'.bundled-modules.json','.DS_Store'}:continue
  if path.is_symlink():findings.append((str(rel),'symlink'));continue
  if not path.is_file():continue
  files.append(path);name=rel.as_posix()
  if path.name.startswith('.env') or path.name=='notation.local.json' or any(p in FORBIDDEN_PARTS for p in rel.parts) or path.suffix in FORBIDDEN_SUFFIX:
   findings.append((name,'excluded-private-or-source-data-file'))
  if not build and name not in policy['files'] and name!='publication-policy.json':findings.append((name,'new-file-needs-public-review'))
  raw=path.read_bytes()
  if path.suffix=='.pdf':
   try:
    from pypdf import PdfReader
    pdf=PdfReader(io.BytesIO(raw));text='\n'.join(p.extract_text() or '' for p in pdf.pages)+'\n'+str(pdf.metadata)
    if pdf.attachments:findings.append((name,'pdf-embedded-attachment'))
   except Exception:findings.append((name,'pdf-inspection-unavailable'));text=''
  elif path.suffix in TEXT_SUFFIX or path.name in {'LICENSE','.gitignore','.gitattributes','SHA256SUMS.txt'} or path.name.endswith('.LICENSE'):
   try:text=raw.decode('utf8')
   except UnicodeDecodeError:findings.append((name,'unreadable-text'));text=''
  else:text=''
  if path.suffix=='.ipynb':
   try:
    notebook=json.loads(text)
    if any(c.get('outputs') or c.get('execution_count') is not None for c in notebook.get('cells',[])):findings.append((name,'notebook-output-needs-clearing'))
   except ValueError:findings.append((name,'invalid-notebook'))
  exemption=policy.get('licence_exceptions',{}).get(name,{})
  if build and path.name in {'LICENSE','THIRD-PARTY-NOTICES.txt'}:
   exemption=next((e for e in policy.get('licence_exceptions',{}).values() if e.get('sha256')==hashlib.sha256(raw).hexdigest()),{})
  permitted=exemption.get('rules',[]) if exemption.get('sha256')==hashlib.sha256(raw).hexdigest() else []
  findings.extend((name,rule) for rule in text_findings(text,policy) if rule not in permitted)
  if not build and path.suffix not in TEXT_SUFFIX and path.name not in {'LICENSE','.gitignore','.gitattributes'} and not path.name.endswith('.LICENSE'):
   if policy.get('binary_sha256',{}).get(name)!=hashlib.sha256(raw).hexdigest():findings.append((name,'binary-asset-needs-visual-review'))
  if path.suffix=='.pdf' and not build and policy.get('binary_sha256',{}).get(name)!=hashlib.sha256(raw).hexdigest():findings.append((name,'pdf-needs-visual-review'))
 return findings,len(files)

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',type=Path,action='append',default=[]);args=parser.parse_args()
 policy=json.loads((ROOT/'publication-policy.json').read_text())
 findings,count=scan(ROOT,policy)
 for directory in args.build:
  if not directory.is_dir():findings.append((str(directory),'missing-build'));continue
  found,n=scan(directory,policy,build=True);findings += [(str(directory)+'/'+p,r) for p,r in found];count+=n
 for path,rule in findings:print(f'{rule}: {path}')
 print(f'Publication check: {count} files; {len(findings)} findings. No matched values printed.')
 return bool(findings)
if __name__=='__main__':sys.exit(main())

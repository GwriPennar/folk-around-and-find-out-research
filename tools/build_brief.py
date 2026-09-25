"""Build the public brief from reviewed Markdown and aggregate evidence."""
from pathlib import Path
import re,json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Preformatted,Image
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
ROOT=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyResearch',fontName='Helvetica',fontSize=10.5,leading=15,spaceAfter=12,textColor=colors.HexColor('#25364b')))
styles.add(ParagraphStyle(name='ResearchTitle',fontName='Helvetica-Bold',fontSize=23,leading=27,spaceAfter=20,textColor=colors.HexColor('#12344a')))
styles.add(ParagraphStyle(name='ResearchSmall',fontName='Helvetica',fontSize=8.5,leading=12,spaceAfter=9))
styles.add(ParagraphStyle(name='ResearchCode',fontName='Courier',fontSize=7.5,leading=10,spaceAfter=10))
def safe(text):
 text=text.replace('→',' -> ').replace('–','-').replace('—','-').replace('’',"'")
 text=html.escape(text)
 text=re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#127c82">\1</link>',text)
 text=re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',text)
 return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
def p(s,style='BodyResearch'):return Paragraph(safe(s),styles[style])
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#127c82'));c.line(44,807,551,807)
 c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#52677c'))
 c.drawString(44,25,'Folk Around And Find Out | Team 8 | Public research v0.1.0 | 25 Sep 2026')
 c.drawRightString(551,25,str(doc.page))
text=(ROOT/'docs/research-brief.md').read_text();sections=text.split('\n## ')[1:]
flow=[]
for i,section in enumerate(sections[:5]):
 if flow:flow.append(PageBreak())
 title,body=section.split('\n',1)
 if i==0:
  flow.extend([p('Quantum-assisted discovery\nof related folk melodies','ResearchTitle'),p('A hybrid quantum-classical approach to musical similarity and clustering.')])
 else:flow.append(p(title,'ResearchTitle'))
 for para in body.strip().split('\n\n'):
  if para.startswith('A hybrid quantum-classical'):continue
  flow.append(p(para))
flow.extend([PageBreak(),p('The 48-tune baseline: features and axes','ResearchTitle')])
flow.append(p('Six provisional reference groups of eight. Classical k-means uses all 16 standardised features; PCA supplies only the displayed position. This is a deliberately selected cohort, not a random sample.'))
flow.append(p('Features: note, event and interval counts; pitch range; distinct-pitch count; rest proportion; mean absolute interval, interval standard deviation and interval entropy; descending, repeated and ascending-note proportions; step and leap proportions; mean duration and duration standard deviation.'))
flow.append(p('Standardisation subtracts each feature mean and divides by its standard deviation; a constant column becomes zero. It equalises measurement scales, not musical importance. The replay starts from the saved standardised vectors.'))
rows=[['Axis','Main weights in this fitted model','Variance'],['PC1 / X','Interval variability +0.31; interval entropy +0.31; pitch range +0.29; repetition -0.29','45.38%'],['PC2 / Y','Leaps +0.37; mean absolute interval +0.32; note/event counts each -0.29','20.40%'],['PC3 / Z','Steps +0.47; repetition -0.45; ascending +0.32; descending +0.31','11.96%']]
def table(rows,widths):
 t=Table([[p(str(v),'ResearchSmall') for v in row] for row in rows],colWidths=widths)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e5f1f1')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,-1),.3,colors.lightgrey)]));return t
flow.append(table(rows,[62,351,80]));flow.append(Spacer(1,12))
flow.append(p('Each component is a weighted mixture, not time, geography or a single musical property. Signs can reverse without changing geometry. A common spatial scale is required. On average, 70.42% of five nearest neighbours remain neighbours in 3D; full-feature distances are more informative than screen distance.'))
run=json.loads((ROOT/'docs/baseline-verification.json').read_text())
rows=[['K','Silhouette in 16D','Reference ARI']]+[[k,f"{v['silhouette']:.6f}",f"{v['reference_ari']:.6f}"] for k,v in run['summary']['scores'].items()]
flow.append(table(rows,[62,215,216]))
flow.extend([PageBreak(),p('A complete synthetic annealing example','ResearchTitle')])
flow.append(p('A-F are artificial nodes, not tunes. Solid positive links favour joining; dashed negative links favour separation. The circular drawing is not a similarity-distance map. Colours show one exact optimal binary assignment.'))
flow.append(Image(str(ROOT/'results/signed-graph/signed-graph.png'),width=440,height=314))
flow.append(p('For x in {0,1}, disagreement d(i,j) = x(i) + x(j) - 2*x(i)*x(j). Positive links pay w*d; negative links pay |w|*(1-d). Minimise the sum.'))
flow.append(p('The QUBO has linear bias equal to incident signed weights, pair bias -2*w, and constant equal to the sum of negative-edge magnitudes. Each undirected pair is counted once. All 64 assignments match an independent graph calculation. The minimum is 2, attained by complementary assignments 000111 and 111000.'))
flow.append(p('Classical Metropolis simulated annealing used 10 seeds, 64 reads per seed and 100 sweeps, cooling geometrically from 4.0 to 0.05. The saved run reached 2 in all 640 best-so-far reads. This tiny control gives no evidence about QPU benefit or scaling. No hardware calls were made.'))
flow.extend([PageBreak(),p('Reproduce and interpret responsibly','ResearchTitle')])
flow.append(p('Public repository: https://github.com/GwriPennar/folk-around-and-find-out-research. Python 3.12. The public notebook calls the same reusable modules as the command line. Choose a new output folder on each run.'))
flow.append(Preformatted('python -m pip install -r requirements.txt\npython -m unittest discover -s tests\npython -m folk_research.annealing \\\n  --input examples/signed-graph.json \\\n  --manifest examples/signed-graph.manifest.json \\\n  --output-dir local-runs/graph-001\npython -m folk_research.classical \\\n  --input examples/synthetic-vectors.json \\\n  --manifest examples/synthetic-vectors.manifest.json \\\n  --output-dir local-runs/vectors-001',styles['ResearchCode']))
flow.append(p('Both bundled inputs are synthetic. IrishMAN record-level inputs remain local because the dataset card has conflicting MIT metadata and research-only/non-commercial wording. The real baseline was verified locally; this public checkout does not reproduce it without authorised local inputs. See docs/classical-baseline.md for the JSON contract and manifest/replay commands.'))
flow.append(p('The private-source observatory can identify and play an authorised local tune selection. This package supplies static scientific figures and analysis code, not the website player, notation or audio.'))
flow.append(p('Evidence labels distinguish historical-reported hardware activity, locally reproduced musical analysis with withheld inputs, publicly reproducible synthetic examples and planned experiments. A hybrid-service success does not isolate quantum contribution. Musical resemblance does not prove ancestry, provenance or ownership.'))
for line in sections[5].split('\n')[1:]:
 if line.startswith('- [') and 'https://' in line:flow.append(p(line[2:],'ResearchSmall'))
flow.append(p('Detailed source/evidence register: docs/evidence.md. Data boundary: docs/data-boundary.md. Existing copyright notices are preserved. This is exploratory research, not a peer-reviewed paper or quantum-advantage claim.','ResearchSmall'))
SimpleDocTemplate(str(ROOT/'docs/Quantum-Assisted-Folk-Research.pdf'),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=50,bottomMargin=46,title='Quantum-assisted discovery of related folk melodies',author='Folk Around And Find Out - Team 8',subject='Hybrid quantum-classical research: motivation, evidence, classical controls and reproducibility').build(flow,onFirstPage=footer,onLaterPages=footer)

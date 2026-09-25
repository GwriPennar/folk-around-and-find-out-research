import itertools,json,tempfile,unittest
from pathlib import Path
from folk_research.annealing import exact,graph_cost,to_qubo,qubo_energy,anneal,validate_graph
from folk_research.records import load_input,new_output
ROOT=Path(__file__).resolve().parents[1]
class ResearchTests(unittest.TestCase):
 def setUp(self):self.graph=json.loads((ROOT/'examples/signed-graph.json').read_text())
 def test_all_assignments(self):
  rows=exact(self.graph);self.assertEqual(len(rows),64)
  for a,e in rows:
   self.assertAlmostEqual(e,graph_cost(self.graph,{n:1-v for n,v in a.items()}))
  self.assertGreater(min(e for _,e in rows),0) # frustrated triangle cannot satisfy every edge
 def test_positive_and_negative_edges(self):
  for weight in [2,-3]:
   graph=dict(nodes=['A','B'],edges=[['A','B',weight]])
   for a,b in itertools.product([0,1],repeat=2):
    expected=(2 if a!=b else 0) if weight>0 else (3 if a==b else 0)
    self.assertEqual(qubo_energy(to_qubo(graph),dict(A=a,B=b)),expected)
 def test_sa_reproducible_valid_and_bounded(self):
  first=anneal(self.graph,42,8,30);self.assertEqual(first,anneal(self.graph,42,8,30))
  optimum=min(e for _,e in exact(self.graph))
  for a,e in first:
   self.assertGreaterEqual(e,optimum);self.assertAlmostEqual(e,graph_cost(self.graph,a))
 def test_digest_and_overwrite(self):
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'input.json';p.write_text('{}')
   with self.assertRaises(ValueError):load_input(p,ROOT/'examples/signed-graph.manifest.json')
   with self.assertRaises(FileExistsError):new_output(folder)
 def test_invalid_graph(self):
  self.graph['edges'].append(self.graph['edges'][0])
  with self.assertRaises(ValueError):validate_graph(self.graph)
if __name__=='__main__':unittest.main()

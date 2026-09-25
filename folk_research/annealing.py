"""Synthetic signed-graph disagreement, QUBO, exact enumeration and classical SA."""
import argparse
import csv
import itertools
import math
import random
from pathlib import Path
from .records import load_input, new_output, write_json, record_run

def validate_graph(graph):
    if graph.get('synthetic') is not True or graph.get('nodes') != list('ABCDEF'):
        raise ValueError('This demonstrator requires six synthetic nodes A-F')
    seen = set()
    for a,b,w in graph['edges']:
        if a not in graph['nodes'] or b not in graph['nodes'] or a == b:
            raise ValueError('Invalid graph edge')
        pair = tuple(sorted((a,b)))
        if pair in seen or isinstance(w,bool) or not isinstance(w,(int,float)) or not math.isfinite(w) or w == 0:
            raise ValueError('Edges must be unique and have finite nonzero weights')
        seen.add(pair)

def graph_cost(graph, assignment):
    # Independent definition: pay for each relationship the assignment violates.
    return sum(abs(w) for a,b,w in graph['edges']
               if (w > 0 and assignment[a] != assignment[b]) or
                  (w < 0 and assignment[a] == assignment[b]))

def to_qubo(graph):
    linear = {node: 0.0 for node in graph['nodes']}
    quadratic = {}
    offset = 0.0
    for a,b,w in graph['edges']:
        linear[a] += w
        linear[b] += w
        quadratic[tuple(sorted((a,b)))] = -2*w
        if w < 0:
            offset += -w
    return linear, quadratic, offset

def qubo_energy(model, assignment):
    linear, quadratic, offset = model
    return offset + sum(w*assignment[a] for a,w in linear.items()) + sum(
        w*assignment[a]*assignment[b] for (a,b),w in quadratic.items())

def exact(graph):
    model = to_qubo(graph)
    rows = []
    for bits in itertools.product([0,1], repeat=len(graph['nodes'])):
        assignment = dict(zip(graph['nodes'],bits))
        cost, energy = graph_cost(graph,assignment), qubo_energy(model,assignment)
        if not math.isclose(cost, energy, abs_tol=1e-10):
            raise AssertionError('QUBO differs from independent graph objective')
        rows.append((assignment,cost))
    return rows

def anneal(graph, seed, reads=64, sweeps=100):
    if reads < 1 or sweeps < 2:
        raise ValueError('Positive reads and at least two sweeps required')
    rng = random.Random(seed)
    model = to_qubo(graph)
    rows = []
    for _ in range(reads):
        state = {n:rng.randrange(2) for n in graph['nodes']}
        energy = qubo_energy(model,state)
        best, best_energy = dict(state),energy
        for step in range(sweeps):
            temperature = 4.0*(0.05/4.0)**(step/(sweeps-1))
            order = list(graph['nodes']); rng.shuffle(order)
            for node in order:
                state[node] ^= 1
                candidate = qubo_energy(model,state)
                delta = candidate-energy
                if delta <= 0 or rng.random() < math.exp(-delta/temperature):
                    energy = candidate
                    if energy < best_energy:
                        best,best_energy = dict(state),energy
                else:
                    state[node] ^= 1
        rows.append((best,best_energy))
    return rows

def run(input_path, manifest_path, output_dir):
    graph,manifest = load_input(input_path,manifest_path,'synthetic-signed-graph')
    validate_graph(graph)
    rows = exact(graph); optimum = min(cost for _,cost in rows)
    seeds = list(range(10)); reads = 64; sweeps = 100
    samples = [(seed,a,e) for seed in seeds for a,e in anneal(graph,seed,reads,sweeps)]
    output = new_output(output_dir)
    with (output/'exact.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['assignment','graph_cost','qubo_energy'])
        writer.writerows([''.join(map(str,a.values())),e,qubo_energy(to_qubo(graph),a)] for a,e in rows)
    with (output/'sa.csv').open('w',newline='') as f:
        writer=csv.writer(f,lineterminator='\n');writer.writerow(['seed','read','best_assignment','best_energy'])
        writer.writerows([s,i%reads,''.join(map(str,a.values())),e] for i,(s,a,e) in enumerate(samples))
    linear,quadratic,offset = to_qubo(graph)
    write_json(output/'bqm.json',dict(vartype='BINARY',linear=linear,
               quadratic=[[a,b,w] for (a,b),w in quadratic.items()],offset=offset))
    summary=dict(synthetic=True,backend='classical-exact-and-simulated-annealing',assignments_verified=len(rows),
                 optimum=optimum,optimal_assignments=[''.join(map(str,a.values())) for a,e in rows if e==optimum],
                 reads=len(samples),best_energy=min(e for _,_,e in samples),
                 optimal_best_so_far_reads=sum(math.isclose(e,optimum,abs_tol=1e-10) for _,_,e in samples))
    write_json(output/'summary.json',summary)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(7,5))
    coordinates={n:(math.cos(i*math.pi/3),math.sin(i*math.pi/3)) for i,n in enumerate(graph['nodes'])}
    assignment=min(rows,key=lambda r:r[1])[0]
    for a,b,w in graph['edges']:
        x,y=coordinates[a],coordinates[b]
        ax.plot([x[0],y[0]],[x[1],y[1]],color='#178478' if w>0 else '#b84462',
                linestyle='-' if w>0 else '--',linewidth=abs(w))
    for n,(x,y) in coordinates.items():
        ax.scatter(x,y,s=650,c='#d4e9ff' if assignment[n]==0 else '#ffd9ab',edgecolors='#172c43',zorder=3)
        ax.text(x,y,n,ha='center',va='center',zorder=4)
    ax.set_title('Synthetic signed graph | one exact optimal assignment')
    ax.text(.5,-.08,'Solid: favour together. Dashed: favour apart. Colours: binary assignment.',transform=ax.transAxes,ha='center',fontsize=9)
    ax.set_aspect('equal');ax.axis('off');fig.tight_layout();fig.savefig(output/'signed-graph.png',dpi=160);plt.close(fig)
    record_run(output,input_path,manifest_path,dict(seeds=seeds,reads_per_seed=reads,sweeps=sweeps,
               temperature_start=4.0,temperature_end=0.05,sample_policy='best-so-far per read'),summary)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);args=p.parse_args()
    print(run(args.input,args.manifest,args.output_dir))

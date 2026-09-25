"""PCA and K-means on saved standardised vectors; no parsing or quantum calls."""
import argparse
import csv
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import adjusted_rand_score, silhouette_score, pairwise_distances
from threadpoolctl import threadpool_limits
from .records import load_input,new_output,write_json,record_run

FEATURES=['note_count','event_count','interval_count','pitch_range','unique_pitch_count','rest_ratio',
          'mean_abs_interval','interval_std','interval_entropy','descending_ratio','repeat_ratio',
          'ascending_ratio','step_ratio','leap_ratio','mean_duration','duration_std']

def run(input_path,manifest_path,output_dir):
    data,manifest=load_input(input_path,manifest_path)
    if manifest.get('kind') not in {'synthetic-standardised-vectors','local-irishman48-standardised-vectors'}:
        raise ValueError('Unsupported vector input kind')
    points=data['points'];X=np.asarray([p['vector'] for p in points],dtype=float)
    if X.shape!=(48,16) or not np.isfinite(X).all():
        raise ValueError('Expected 48 finite, standardised 16D vectors')
    synthetic=manifest['kind'].startswith('synthetic')
    if bool(data.get('synthetic',False))!=synthetic:
        raise ValueError('Manifest and data disagree on synthetic status')
    if not synthetic and ('models' not in data or any('xyz' not in p for p in points)):
        raise ValueError('Local replay requires saved assignments and coordinates')
    families=[p['family'] for p in points]
    with threadpool_limits(limits=1):
        pca=PCA(n_components=16,svd_solver='full');coordinates=pca.fit_transform(X)
        fitted={k:KMeans(n_clusters=k,n_init=20,random_state=42,algorithm='lloyd').fit(X) for k in range(2,9)}
        scores={k:dict(silhouette=float(silhouette_score(X,m.labels_)),
                       reference_ari=float(adjusted_rand_score(families,m.labels_)),inertia=float(m.inertia_))
                for k,m in fitted.items()}
    if not synthetic:
        saved=np.asarray([p['xyz'] for p in points])
        # Pairwise geometry is invariant to arbitrary PCA signs and orthogonal rotations.
        if not np.allclose(pairwise_distances(coordinates[:,:3]),pairwise_distances(saved),atol=1e-6,rtol=1e-7):
            raise AssertionError('PCA geometry differs from the saved baseline')
        if not np.allclose(pca.explained_variance_ratio_[:3],data['pca']['variance'][:3],atol=1e-8):
            raise AssertionError('PCA variance differs from the saved baseline')
        for k,model in fitted.items():
            expected=data['models'][str(k)]
            if adjusted_rand_score(model.labels_,expected['labels'])!=1:
                raise AssertionError('Cluster partition differs from saved baseline')
            if abs(scores[k]['silhouette']-expected['silhouette'])>1e-8 or abs(scores[k]['reference_ari']-expected['ari'])>1e-8:
                raise AssertionError('Cluster metrics differ from saved baseline')
    output=new_output(output_dir)
    with (output/'k-comparison.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['k','silhouette_16d','reference_ari','inertia'])
        w.writerows([k,*scores[k].values()] for k in fitted)
    with (output/'coordinates.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['record','PC1','PC2','PC3','cluster_k6'])
        w.writerows([p['id'],*coordinates[i,:3],int(fitted[6].labels_[i])] for i,p in enumerate(points))
    with (output/'loadings.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['feature','PC1','PC2','PC3'])
        names=[f'synthetic_dimension_{i+1}' for i in range(16)] if synthetic else FEATURES
        w.writerows([name,*pca.components_[:3,i]] for i,name in enumerate(names))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    xyz=coordinates[:,:3];mid=(xyz.max(0)+xyz.min(0))/2;radius=max(float(np.ptp(xyz,axis=0).max())*.55,.1)
    fig=plt.figure(figsize=(8,6));ax=fig.add_subplot(111,projection='3d')
    ax.scatter(*xyz.T,c=fitted[6].labels_,cmap='tab10',s=35)
    for setter,centre in zip([ax.set_xlim,ax.set_ylim,ax.set_zlim],mid):setter(centre-radius,centre+radius)
    ax.set_box_aspect((1,1,1))
    for i,setter in enumerate([ax.set_xlabel,ax.set_ylabel,ax.set_zlabel]):setter(f'PC{i+1}: {pca.explained_variance_ratio_[i]:.1%}')
    ax.set_title(('SYNTHETIC vectors - not IrishMAN' if synthetic else 'Local IrishMAN48 replay')+'\nClassical K-means in 16D; PCA for display')
    fig.tight_layout();fig.savefig(output/'pca.png',dpi=160);plt.close(fig)
    summary=dict(synthetic=synthetic,backend='classical',records=48,dimensions=16,
                 variance=pca.explained_variance_ratio_[:3].tolist(),scores=scores,
                 saved_baseline_verified=not synthetic)
    write_json(output/'summary.json',summary)
    record_run(output,input_path,manifest_path,dict(k=list(range(2,9)),seed=42,n_init=20,
        input='already-standardised; no new scaling',pca_solver='full',clustering_space='16D'),summary)
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args()
    print(run(a.input,a.manifest,a.output_dir))

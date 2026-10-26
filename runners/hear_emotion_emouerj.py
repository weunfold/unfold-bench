"""LAION Humaneness Ears on emoUERJ (pt-BR, 8 actors, 4 emotions: anger, happiness, neutral,
sadness; CC BY 4.0). Two scores:
  1. zero-shot: argmax over emotion groups of Ears' display z-scores (no labels used);
  2. probe: logistic regression on Ears' 192 raw scores, leave-one-speaker-out (8 folds), like the card's
     actor-CV adapters (CREMA-D 0.63, RAVDESS 0.66 for Base).
CPU only; RSS watchdog at 10 GB. Needs numpy, scikit-learn and a local copy of the Ears model repository.
Usage: hear_emotion_emouerj.py EARS_REPO WAV_DIR OUT_JSON [base|medium]"""
import json, os, subprocess, sys, threading, time
from pathlib import Path
import numpy as np

repo, wavs, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); size = sys.argv[4] if len(sys.argv) > 4 else 'base'
def _guard():
    while True:
        r = int(subprocess.run(['ps', '-o', 'rss=', '-p', str(os.getpid())], capture_output=True, text=True).stdout or 0) * 1024
        if r > 10e9: print(json.dumps({'abort': 'rss_limit', 'rss_gb': round(r / 1e9, 2)}), flush=True); os._exit(3)
        time.sleep(0.5)
threading.Thread(target=_guard, daemon=True).start()
sys.path.insert(0, str(repo))
from inference import Predictor

LABEL = {'a': 'anger', 'h': 'happiness', 'n': 'neutral', 's': 'sadness'}
GROUPS = {'anger': ['Anger', 'Impatience_and_Irritability', 'Bitterness', 'Contempt', 'Malevolence_Malice'],
          'happiness': ['Elation', 'Amusement', 'Contentment', 'Hope_Enthusiasm_Optimism', 'Pleasure_Ecstasy', 'Triumph', 'Affection'],
          'sadness': ['Sadness', 'Disappointment', 'Distress', 'Helplessness', 'Pain', 'Longing'],
          'neutral': ['Concentration', 'Contemplation', 'Emotional_Numbness']}
P = Predictor(repo, size, 'cpu', threads=4)
rows, t_all = [], []
for f in sorted(wavs.glob('*.wav')):
    t = time.perf_counter(); r = P.predict(f); t_all.append(time.perf_counter() - t)
    z = r['scores_z']; grp = {g: float(np.mean([z[f'emo_{n}'] for n in ns if z.get(f'emo_{n}') is not None])) for g, ns in GROUPS.items()}
    rows.append({'file': f.name, 'speaker': f.name[:3], 'gender': f.name[0], 'label': LABEL[f.name[3]],
                 'zero_shot': max(grp, key=grp.get), 'groups': grp, 'raw': list(r['scores_raw'].values()),
                 'valence_z': z.get('eiv_extra:Valence'), 'arousal_z': z.get('eiv_extra:Arousal'),
                 'bursts': len(r['burst_event_proposals'])})
y = np.array([r['label'] for r in rows]); spk = np.array([r['speaker'] for r in rows])
zs = np.array([r['zero_shot'] for r in rows])
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import balanced_accuracy_score, confusion_matrix
X = np.array([r['raw'] for r in rows]); pred = np.empty_like(y)
for s in sorted(set(spk)):
    tr, te = spk != s, spk == s
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.1)).fit(X[tr], y[tr]); pred[te] = clf.predict(X[te])
labs = ['anger', 'happiness', 'neutral', 'sadness']
res = {'model': f'humaneness-ears-{size}', 'n': len(rows), 'speakers': sorted(set(spk)),
       'cpu_s_per_clip_p50': round(float(np.median(t_all)), 3), 'clip_s_p50': None,
       'zero_shot': {'acc': round(float((zs == y).mean()), 3), 'uar': round(float(balanced_accuracy_score(y, zs)), 3),
                     'confusion_rows_gold': confusion_matrix(y, zs, labels=labs).tolist()},
       'probe_loso': {'acc': round(float((pred == y).mean()), 3), 'uar': round(float(balanced_accuracy_score(y, pred)), 3),
                      'confusion_rows_gold': confusion_matrix(y, pred, labels=labs).tolist()},
       'labels': labs, 'rows': [{k: v for k, v in r.items() if k != 'raw'} for r in rows]}
json.dump(res, open(out, 'w'), indent=1); os.chmod(out, 0o600)
print(json.dumps({k: res[k] for k in ['model', 'n', 'cpu_s_per_clip_p50', 'zero_shot', 'probe_loso']}))

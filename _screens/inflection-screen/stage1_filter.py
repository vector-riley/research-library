"""Stage 1 of the GXO-style inflection screen.

Input: a JSON dump of Baba's data_comps grid (us_only=true, limit>=2500, sort=ticker),
saved by the MCP host when the result is too large to return inline.
Output: universe_us.csv, stage1_survivors.csv, stage1_ranked.csv in --out.

Thresholds are calibrated so that GXO passes every gate (see README.md).
Run:  python3 stage1_filter.py --dump path/to/data_comps.json --out outputs/YYYY.MM.DD
"""
import argparse, csv, json, statistics as st
from collections import defaultdict

KEYS = ['cid','ticker','name','sector','industry','bucket','mcap','tev','price_ltm_pct','drawdown',
        'drawdown_window_start','pctile','pctile_metric','pctile_months','dislocated','ebitda_margin',
        'ufcf_margin','ev_ebitda_fy','ev_ebitda_fy1','net_debt_ltm_ebitda','revenue_cagr','ebitda_cagr',
        'rev_revision','ebitda_revision','ebitda_inflection','ebitda_turn_pct','rev_turn_pct','ebitda_brokers',
        'pretax_lfcf_yield_fy','pretax_lfcf_yield_fy1','pretax_lfcf_conversion','fdso_cagr_prior','founder_led',
        'screens_flagged','score','score_rank']
EXCL_SECT = {'Financials','Financial Services','Utilities','Energy'}
EXCL_IND = {'Biotechnology','Pharmaceuticals','Drug Manufacturers - Specialty & Generic','Gold and Silver',
            'Precious Metals and Minerals','Uranium','Lithium','Copper','Diversified Metals & Mining',
            'Oil & Gas Exploration & Production'}

def num(v):
    try:
        return float(v) if v not in (None, '', 'None') else None
    except (TypeError, ValueError):
        return None

def load(dump):
    raw = open(dump).read()
    obj = json.loads(raw)
    if isinstance(obj, list):              # host wrapper [{type:text, text:...}]
        obj = json.loads(obj[0]['text'])
    return obj['rows']

def peer_medians(rows):
    ind, sec = defaultdict(list), defaultdict(list)
    for r in rows:
        m = num(r.get('ebitda_margin'))
        if m is not None and -1 < m < 1.5:
            ind[r['industry']].append(m); sec[r['sector']].append(m)
    return ({k: st.median(v) for k, v in ind.items() if len(v) >= 5},
            {k: st.median(v) for k, v in sec.items()})

def passes(r, indmed, secmed, reasons):
    mcap, brokers, m = num(r.get('mcap')), num(r.get('ebitda_brokers')), num(r.get('ebitda_margin'))
    dd, pct, ltm = num(r.get('drawdown')), num(r.get('pctile')), num(r.get('price_ltm_pct'))
    rev, lev = num(r.get('ebitda_revision')), num(r.get('net_debt_ltm_ebitda'))
    if r['sector'] in EXCL_SECT or r['industry'] in EXCL_IND: reasons['sector/industry'] += 1; return False
    if mcap is None or mcap < 1e9: reasons['mcap<1bn'] += 1; return False
    if brokers is None or brokers < 3: reasons['brokers<3'] += 1; return False
    if m is None: reasons['no margin'] += 1; return False
    # Gate 1: underperforming. Two of three: 3yr drawdown <= -20%, own-history EV/EBITDA pctile <= 25%, LTM price <= -10%
    under = sum([dd is not None and dd <= -0.20, pct is not None and pct <= 0.25, ltm is not None and ltm <= -0.10])
    if under < 2: reasons['not underperforming (need 2 of 3)'] += 1; return False
    # Gate 2: room to expand. EBITDA margin <= 15% absolute, or below industry (else sector) median and <= 30%
    ref = indmed.get(r['industry'], secmed.get(r['sector']))
    if not ((m <= 0.15) or (ref is not None and m < ref and m <= 0.30)): reasons['margin not below peers'] += 1; return False
    # Gate 3: unproven. 12m consensus EBITDA revision between -30% and +10% (street has not underwritten it, and the story is not broken)
    if rev is None or rev < -0.30 or rev > 0.10: reasons['ebitda revision outside -30%..+10%'] += 1; return False
    # Gate 4: balance sheet survivable. Net debt / LTM EBITDA <= 5x (None allowed)
    if lev is not None and lev > 5: reasons['leverage>5x'] += 1; return False
    r['_under'] = under; r['_indmed'] = round(ref, 3) if ref else None
    return True

def similarity(r):
    """Lower = closer to GXO's fingerprint: cheap vs own history, drawn down, well below peer margin, flat revisions."""
    pct = num(r.get('pctile')); pct = 0.5 if pct is None else pct
    dd = num(r.get('drawdown')); dd = -0.2 if dd is None else dd
    m = num(r.get('ebitda_margin')); ref = r.get('_indmed') or m
    gap = (ref - m) / ref if ref and ref > 0 else 0
    rev = abs(num(r.get('ebitda_revision')) or 0)
    r['_gap'] = round(gap, 2)
    return round(1.5 * pct + 1.0 * (1 - min(1, abs(dd) / 0.4)) + 1.5 * (1 - min(1, gap)) + 1.0 * min(1, rev / 0.1), 3)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dump', required=True); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    rows = load(a.dump)
    with open(f'{a.out}/universe_us.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=KEYS); w.writeheader(); [w.writerow({k: r.get(k) for k in KEYS}) for r in rows]
    indmed, secmed = peer_medians(rows)
    reasons = defaultdict(int)
    surv = [r for r in rows if passes(r, indmed, secmed, reasons)]
    for r in surv: r['_sim'] = similarity(r)
    surv.sort(key=lambda r: r['_sim'])
    cols = ['ticker','industry','mcap','price_ltm_pct','drawdown','pctile','ebitda_margin','_indmed','_gap','ebitda_revision',
            'ev_ebitda_fy','net_debt_ltm_ebitda','ebitda_brokers','bucket','_sim','cid','name','sector']
    with open(f'{a.out}/stage1_ranked.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction='ignore'); w.writeheader(); [w.writerow(r) for r in surv]
    print(f'universe {len(rows)}  survivors {len(surv)}  rejects {dict(reasons)}')

if __name__ == '__main__':
    main()

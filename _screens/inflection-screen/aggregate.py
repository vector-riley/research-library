"""Stage 4: collect the per-ticker JSON records written by the stage 3 subagents into one ranked table.
Run:  python3 aggregate.py --run outputs/YYYY.MM.DD   -> writes ranked.md and ranked.csv in that folder."""
import argparse, csv, glob, json, os

def load_descriptions(run):
    fn = os.path.join(run, 'descriptions.json')
    try: return json.load(open(fn))
    except Exception: return {}

def load_universe(run):
    fn = os.path.join(run, 'universe_us.csv')
    if not os.path.exists(fn): return {}
    return {r['ticker']: r for r in csv.DictReader(open(fn))}

def fnum(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def rescore_d(r, uni):
    """Stabilization-based D: 0 if 4m revision < -3% or target already in consensus; else by gap or by 4m band."""
    u = uni.get(r.get('ticker'), {}); turn = fnum(u.get('ebitda_turn_pct'))
    if turn is not None and turn < -0.03: return 0, 'still falling'
    tgt = fnum(g(r,'margin_framing','target_level_pct')); street = fnum(g(r,'street','consensus_margin_at_target_year_pct'))
    if tgt is not None and street is not None:
        gap = (tgt - street) * 100
        return (2 if gap >= 100 else 1 if gap >= 25 else 0), f'gap {gap:+.0f} bps'
    if turn is None: return None, 'no 4m data'
    return (2 if -0.03 <= turn <= 0.05 else 1 if turn <= 0.10 else 0), f'4m {turn:+.1%}'


def g(d, *path):
    for p in path:
        if not isinstance(d, dict) or p not in d: return None
        d = d[p]
    return d

def fmt(v, kind):
    if v is None: return ''
    try:
        if kind == 'pct': return f'{100*float(v):.0f}%'
        if kind == 'pct1': return f'{float(v):.1f}%'
        if kind == 'x': return f'{float(v):.1f}x'
        if kind == 'bn': return f'{float(v)/1e9:.1f}'
        if kind == 'int': return f'{int(v)}'
    except (TypeError, ValueError): return str(v)
    return str(v)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True); a = ap.parse_args()
    recs = []
    for fn in sorted(glob.glob(os.path.join(a.run, 'candidates', '*.json'))):
        try: recs.append(json.load(open(fn)))
        except Exception as e: print('skip', fn, e)
    uni = load_universe(a.run); desc = load_descriptions(a.run)
    for r in recs:
        d2, why = rescore_d(r, uni); r['_d2'] = d2; r['_d2_why'] = why
        base = sum((g(r,'score',k) or 0) for k in ('A_underperformance','B_catalyst','C_numeric_framing'))
        r['_total2'] = base + d2 if d2 is not None else g(r,'score','total')
    recs.sort(key=lambda r: (-(r['_total2'] or 0), r.get('ticker','')))
    cols = ['ticker','business','total2','setup','A','B','C','D2','D2_why','D_agent','total_agent','disq','mcap_bn','ltm_price','drawdown','pctile','ebitda_margin','ind_median','ev_ebitda',
            'nd_ebitda','rev_12m','catalyst','months','numeric','target','target_yr','street_at_target','gap_bps','verdict']
    rows = []
    for r in recs:
        rows.append({
            'ticker': r.get('ticker'), 'business': (desc.get(r.get('ticker')) or {}).get('business', ''),
            'ltm_price': fmt(fnum(uni.get(r.get('ticker'), {}).get('price_ltm_pct')), 'pct'),
            'total2': r['_total2'], 'total_agent': g(r,'score','total'), 'A': g(r,'score','A_underperformance'),
            'B': g(r,'score','B_catalyst'), 'C': g(r,'score','C_numeric_framing'), 'D2': r['_d2'], 'D2_why': r['_d2_why'], 'D_agent': g(r,'score','D_unproven'),
            'setup': 'yes' if (not r.get('disqualified') and (g(r,'score','B_catalyst') or 0) >= 2 and (g(r,'score','C_numeric_framing') or 0) >= 2 and ((r['_d2'] if r['_d2'] is not None else g(r,'score','D_unproven')) or 0) >= 1) else '',
            'disq': 'yes' if r.get('disqualified') else '', 'mcap_bn': fmt(g(r,'quant','mcap_usd'),'bn'),
            'drawdown': fmt(g(r,'quant','drawdown'),'pct'), 'pctile': fmt(g(r,'quant','pctile_ev_ebitda_60m'),'pct'),
            'ebitda_margin': fmt(g(r,'quant','ebitda_margin_ltm'),'pct1' if (g(r,'quant','ebitda_margin_ltm') or 0) > 1 else 'pct'),
            'ind_median': fmt(g(r,'quant','industry_median_margin'),'pct'), 'ev_ebitda': fmt(g(r,'quant','ev_ebitda_fy'),'x'),
            'nd_ebitda': fmt(g(r,'quant','net_debt_ltm_ebitda'),'x'), 'rev_12m': fmt(g(r,'quant','ebitda_revision_12m'),'pct'),
            'catalyst': ','.join(g(r,'catalyst','type') or []), 'months': g(r,'catalyst','months_since_primary'),
            'numeric': g(r,'margin_framing','numeric'), 'target': g(r,'margin_framing','target_level_pct'),
            'target_yr': g(r,'margin_framing','target_year'), 'street_at_target': g(r,'street','consensus_margin_at_target_year_pct'),
            'gap_bps': g(r,'street','gap_bps_vs_target'), 'verdict': (r.get('verdict') or '')[:160]})
    with open(os.path.join(a.run, 'ranked.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); [w.writerow(x) for x in rows]
    with open(os.path.join(a.run, 'ranked.md'), 'w') as f:
        f.write(f'# Inflection screen, ranked candidates ({os.path.basename(a.run)})\n\n')
        f.write('Score components: A underperformance (0-2), B catalyst (0-3), C numeric margin framing (0-3), D unproven vs street (0-2). D2 is the stabilization-based unproven score (0 if the 4-month forward EBITDA revision is below -3% or the target is already in consensus; a prior 12-month cut alone does not zero it). D_agent is the original subagent score under the older rule. Score = A + B + C + D2. Setup = yes when not disqualified and B >= 2, C >= 2, D2 >= 1 all hold: the archetype is the conjunction, not the sum.\n\n')
        f.write('| Ticker | Business | Score | Setup | A | B | C | D2 | D2 basis | D agent | Score agent | DQ | Mcap $bn | LTM price | Drawdown | Own-hist pctile | EBITDA mgn | Ind. median | EV/EBITDA | ND/EBITDA | 12m EBITDA rev | Catalyst | Months | Numeric? | Target % | Yr | Street @ yr | Gap bps | Verdict |\n')
        f.write('|' + '---|'*29 + '\n')
        for x in rows:
            f.write('| ' + ' | '.join(str(x[c]) if x[c] is not None else '' for c in cols) + ' |\n')
    print(f'{len(rows)} records -> {a.run}/ranked.md')

if __name__ == '__main__':
    main()

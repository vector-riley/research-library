"""Stage 4: collect the per-ticker JSON records written by the stage 3 subagents into one ranked table.
Run:  python3 aggregate.py --run outputs/YYYY.MM.DD   -> writes ranked.md and ranked.csv in that folder."""
import argparse, csv, glob, json, os

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
    recs.sort(key=lambda r: (-(g(r,'score','total') or 0), r.get('ticker','')))
    cols = ['ticker','total','setup','A','B','C','D','disq','mcap_bn','drawdown','pctile','ebitda_margin','ind_median','ev_ebitda',
            'nd_ebitda','rev_12m','catalyst','months','numeric','target','target_yr','street_at_target','gap_bps','verdict']
    rows = []
    for r in recs:
        rows.append({
            'ticker': r.get('ticker'), 'total': g(r,'score','total'), 'A': g(r,'score','A_underperformance'),
            'B': g(r,'score','B_catalyst'), 'C': g(r,'score','C_numeric_framing'), 'D': g(r,'score','D_unproven'),
            'setup': 'yes' if (not r.get('disqualified') and (g(r,'score','B_catalyst') or 0) >= 2 and (g(r,'score','C_numeric_framing') or 0) >= 2 and (g(r,'score','D_unproven') or 0) >= 1) else '',
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
        f.write('Score components: A underperformance (0-2), B catalyst (0-3), C numeric margin framing (0-3), D unproven vs street (0-2). Setup = yes when not disqualified and B >= 2, C >= 2, D >= 1 all hold: the archetype is the conjunction, not the sum.\n\n')
        f.write('| Ticker | Score | Setup | A | B | C | D | DQ | Mcap $bn | Drawdown | Own-hist pctile | EBITDA mgn | Ind. median | EV/EBITDA | ND/EBITDA | 12m EBITDA rev | Catalyst | Months | Numeric? | Target % | Yr | Street @ yr | Gap bps | Verdict |\n')
        f.write('|' + '---|'*24 + '\n')
        for x in rows:
            f.write('| ' + ' | '.join(str(x[c]) if x[c] is not None else '' for c in cols) + ' |\n')
    print(f'{len(rows)} records -> {a.run}/ranked.md')

if __name__ == '__main__':
    main()

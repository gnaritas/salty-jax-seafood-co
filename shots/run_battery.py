#!/usr/bin/env python3
"""Threaded OpenRouter gemini-2.5-flash vision battery for Salty Jax shots.
Resizes scale-1 copies, runs defect-hunt with calibrated guards, saves vision-results.json."""
import json, os, base64, urllib.request, concurrent.futures, subprocess, re

D = os.path.dirname(os.path.abspath(__file__))
ENV = {}
for line in open(os.path.expanduser('~/.hermes/.env')):
    line = line.strip()
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1); ENV[k] = v.strip().strip('"').strip("'")
KEY = ENV.get('OPENROUTER_API_KEY')
assert KEY, 'no OPENROUTER key'

shots = [f for f in sorted(os.listdir(D)) if f.endswith('.png') and not f.startswith('r_')]
shots.append(os.path.join('..', 'public', 'og.png'))

# resized copies (desktop->1265w, mobile/og stay <=1200)
work = []
from PIL import Image as PImage
for s in shots:
    p = os.path.join(D, s)
    im = PImage.open(p)
    if 'og' in s or im.width <= 1265:
        work.append(p); continue
    q = os.path.join(D, 'r_' + s)
    im.resize((1265, int(im.height * 1265 / im.width)), PImage.LANCZOS).save(q)
    work.append(q)

PROMPT = ("You are doing a strict layout defect sweep of one full-page website screenshot (business: Salty Jax Seafood Co., seafood restaurant demo site, Ocean Springs MS).\n"
"Look for REAL defects only: text clipped or overflowing its box or viewport, overlapping elements that collide, glued blocks (zero gap between distinct sections where siblings have clear separation), misaligned columns/rows in grids, broken/ugly wrapping of words, invisible text (text color near background color), a nav bar with uneven item spacing, a button whose label touches its edges, a map or image area that failed to paint (solid gray), headings cut off, footer columns ragged at baseline.\n"
"Do NOT flag: decorative faint circles/shapes behind hero text (intentional), intentional double short rules under headings, uneven line counts across columns in the footer, responsive single-column stacking on mobile shots, 1-2px alignment nits, scrollbar-gutter right-edge proximity, normal hyphenation/wrapping inside paragraphs, tight line-height inside headings that are still readable, small-caps tracking.\n"
"First line of your answer: VERDICT: CLEAN or VERDICT: DEFECTS. If DEFECTS, list each as '- <defect> @ <location>' with max 3 items, most severe first. Be terse. No praise.")

def call(path):
    b = base64.b64encode(open(path,'rb').read()).decode()
    body = {"model":"google/gemini-2.5-flash","messages":[{"role":"user","content":[
        {"type":"text","text":PROMPT},
        {"type":"image_url","image_url":{"url":"data:image/png;base64,"+b}}]}],
        "max_tokens":280,"temperature":0.1}
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
        headers={'Authorization':'Bearer '+KEY,'Content-Type':'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.loads(r.read())
            txt = j['choices'][0]['message']['content'].strip()
            v = 'DEFECTS' if 'VERDICT: DEFECTS' in txt else ('CLEAN' if 'VERDICT: CLEAN' in txt else 'UNPARSED')
            return {'shot':os.path.basename(path),'verdict':v,'text':txt}
        except Exception as e:
            if attempt == 2: return {'shot':os.path.basename(path),'verdict':'ERROR','text':str(e)[:150]}

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
    results = list(ex.map(call, work))

json.dump(results, open(os.path.join(D,'vision-results.json'),'w'), indent=1)
for r in results:
    print(r['shot'], r['verdict'])
    if r['verdict'] == 'DEFECTS':
        print('   ', r['text'].replace('\n',' | ')[:400])
n_def = sum(1 for r in results if r['verdict']=='DEFECTS')
print(f'BATTERY: {len(results)} shots, {n_def} flagged, {sum(1 for r in results if r["verdict"] in ("ERROR","UNPARSED"))} unusable')

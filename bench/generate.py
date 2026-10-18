"""Generate one site per brief with the DeepSeek API (no agent harness).

Usage: DEEPSEEK_API_KEY=... python3 bench/generate.py [model]
Reads prompts/system.txt and prompts/briefs/*.txt, writes sites/<brief>.html
and results/usage.json.
"""
import concurrent.futures as cf, json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = sys.argv[1] if len(sys.argv) > 1 else 'deepseek-flash'
KEY = os.environ['DEEPSEEK_API_KEY']
SYSTEM = open(f'{ROOT}/prompts/system.txt').read()
SUFFIX = ('\n\nMake it a single long one-page website (hero + at least 4 sections + footer). '
          'It must be stunning to look at and delightful to use.')


def generate(name):
    brief = open(f'{ROOT}/prompts/briefs/{name}.txt').read()
    if SUFFIX.strip() not in brief:
        brief += SUFFIX
    body = json.dumps({'model': MODEL, 'max_tokens': 64000, 'messages': [
        {'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': brief}]}).encode()
    req = urllib.request.Request('https://api.deepseek.com/chat/completions', body,
                                 {'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    start = time.time()
    resp = json.load(urllib.request.urlopen(req, timeout=900))
    text = resp['choices'][0]['message']['content']
    blocks = re.findall(r'```[\w-]*\n(.*?)```', text, re.S)
    open(f'{ROOT}/sites/{name}.html', 'w').write(max(blocks, key=len) if blocks else text)
    return name, {'usage': resp.get('usage', {}), 'secs': round(time.time() - start, 1)}


names = sorted(f[:-4] for f in os.listdir(f'{ROOT}/prompts/briefs') if f.endswith('.txt'))
results = {}
with cf.ThreadPoolExecutor(len(names)) as pool:
    for fut in cf.as_completed([pool.submit(generate, n) for n in names]):
        name, info = fut.result()
        results[name] = info
        print(name, info['usage'].get('completion_tokens'), f"{info['secs']}s", flush=True)
json.dump(dict(sorted(results.items())), open(f'{ROOT}/results/usage.json', 'w'), indent=1)

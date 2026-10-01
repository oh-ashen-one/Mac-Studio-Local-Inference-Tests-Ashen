#!/usr/bin/env python3
"""Serve saved status/results on loopback. Never imports an inference library."""
import argparse
import json
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]


def state(comparison):
    specs=json.loads((ROOT/'config/models.lock.json').read_text())['models']
    models=[]
    for m in specs:
        present=all((ROOT/'models'/m['id']/f['path']).is_file() and (ROOT/'models'/m['id']/f['path']).stat().st_size==f['bytes'] for f in m['files'])
        models.append({'id':m['id'],'quantization':m['quantization'],'total_bytes':m['total_bytes'],'present':present})
    long_runs=[]
    for result_file in (ROOT/'results').glob('*200k*/result.json'):
        try:
            result=json.loads(result_file.read_text());result.pop('output_text',None);result.pop('output_token_ids',None);long_runs.append(result)
        except (OSError,ValueError):pass
    progress=ROOT/'work/long-context-live.json'
    long_live=json.loads(progress.read_text()) if progress.exists() else None
    if long_live:
        long_live.pop('output_text',None);long_live.pop('output_token_ids',None)
    peers=ROOT/'research/external-benchmarks.json';campaign=ROOT/'research/campaign-status.json'
    return {'long_runs':long_runs,'long_live':long_live,'peers':json.loads(peers.read_text()) if peers.exists() else None,'campaign':json.loads(campaign.read_text()) if campaign.exists() else None,'ready':(ROOT/'work/READY.json').exists() and all(m['present'] for m in models),
            'models':models,'live':json.loads((ROOT/'work/live-results.json').read_text()) if (ROOT/'work/live-results.json').exists() else None,'comparison':json.loads(comparison.read_text()) if comparison.exists() else None}


def handler_for(comparison):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.path=urlsplit(self.path).path
            if self.path=='/':body=(ROOT/'viewer/index.html').read_bytes();mime='text/html; charset=utf-8'
            elif self.path=='/api/state':body=json.dumps(state(comparison)).encode();mime='application/json'
            else:self.send_error(404);return
            if self.path=='/':print(json.dumps({'event':'page_open','user_agent':self.headers.get('User-Agent','')}),flush=True)
            self.send_response(200);self.send_header('Content-Type',mime)
            self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)))
            self.end_headers();self.wfile.write(body)
        def log_message(self,*args):pass
    return Handler


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--port',type=int,default=18765)
    p.add_argument('--comparison',type=Path,default=ROOT/'work/comparison.json');a=p.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',a.port),handler_for(a.comparison))
    print(f'Local saved-results preview: http://127.0.0.1:{a.port} — no inference',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()

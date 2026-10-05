#!/usr/bin/env python3
"""Build a deterministic public-code corpus; never execute the downloaded code."""
import hashlib,io,json,tarfile,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REV='3bb231a6a5dc02b95658877318bf61501a7209e9'
url=f'https://codeload.github.com/python/cpython/tar.gz/{REV}'
archive=urllib.request.urlopen(url,timeout=120).read()
rows=[];parts=[];size=0
with tarfile.open(fileobj=io.BytesIO(archive),mode='r:gz') as tar:
    for member in sorted(tar.getmembers(),key=lambda m:m.name):
        name=member.name.split('/',1)[-1]
        if not member.isfile() or not name.startswith('Lib/') or not name.endswith('.py') or '/test' in name:continue
        data=tar.extractfile(member).read()
        text=data.decode('utf-8',errors='replace')
        parts.append(f'\n### FILE: {name}\n{text}\n');size+=len(data)
        rows.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        if size>=6*1024**2:break
out=ROOT/'work/context-corpus.txt';out.parent.mkdir(exist_ok=True)
out.write_text(''.join(parts))
manifest={'source':'https://github.com/python/cpython','revision':REV,'license':'Python Software Foundation license; see upstream LICENSE','archive_sha256':hashlib.sha256(archive).hexdigest(),'corpus_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'files':rows,'corpus_bytes':out.stat().st_size,'note':'Deterministic source-file concatenation; each tokenizer selects a 200000-token window. Performance corpus only, not a task-completion evaluation.'}
(ROOT/'work/context-corpus-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Corpus bytes:',out.stat().st_size,'Files:',len(rows),'SHA256:',manifest['corpus_sha256'])

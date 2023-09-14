import os
import json
from netfile_client.NetFileClient import NetFileClient

print('Replace this with python script to pull and redact files')

os.makedirs('netfile_redacted', exist_ok=True)

REPO_OWNER = os.getenv('REPO_OWNER')

print(REPO_OWNER)

if REPO_OWNER == 'ChenglimEar':
    data = {'msg':'hello'}
    with open('netfile_redacted/data.json','w') as f:
        json.dump(data,f)
else:
    nf = NetFileClient()
    nf.fetch('filings')


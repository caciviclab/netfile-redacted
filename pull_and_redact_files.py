import os
import json
from netfile_client.NetFileClient import NetFileClient

print('Replace this with python script to pull and redact files')

os.makedirs('netfile_redacted', exist_ok=True)

REPO_OWNER = os.getenv('REPO_OWNER')

if REPO_OWNER == 'ChenglimEar':
    print(f'Simulating NetFile response for {REPO_OWNER}')
    data = {'msg':'hello'}
    with open('netfile_redacted/data.json','w') as f:
        json.dump(data,f)
else:
    print(f'Making NetFile API calls')
    nf = NetFileClient()
    nf.fetch('filings')


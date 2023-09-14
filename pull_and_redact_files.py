import os
import json
from netfile_client.NetFileClient import NetFileClient

print('Replace this with python script to pull and redact files')

os.makedirs('netfile_redacted', exist_ok=True)

REPO_NAME = os.getenv('REPO_NAME')

print(REPO_NAME)

if REPO_NAME == 'netfile_redacted':
    data = {'msg':'hello'}
    with open('netfile_redacted/data.json','w') as f:
        json.dump(data,f)
else:
    nf = NetFileClient()
    nf.fetch('filings')


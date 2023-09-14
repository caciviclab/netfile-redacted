import os
import json
from netfile_client.NetFileClient import NetFileClient

def redact(data):
    # TODO: add code that will redact data according to configuration
    pass

os.makedirs('netfile_redacted', exist_ok=True)

REPO_OWNER = os.getenv('REPO_OWNER')

if REPO_OWNER == 'ChenglimEar':
    print(f'Simulating NetFile response for {REPO_OWNER}')
    for name in ['filers','filings']:
        with open(f'netfile_samples/{name}.json','r') as f:
            data = json.load(f)
            redact(data)
        with open(f'netfile_redacted/{name}.json','w') as f:
            json.dump(data,f)
else:
    print(f'Making NetFile API calls')
    nf = NetFileClient()
    for name in ['filers', 'filings']:
    #for name in ['filers', 'filings','transactions', 'filing_activities', 'filing_elements', 'elections']:
        data = nf.fetch(name)
        redact(data)
        with open(f'netfile_redacted/{name}.json','w') as f:
            json.dump(data,f)


import os
import json
import yaml
from netfile_client.NetFileClient import NetFileClient

class DataRetriever:
    def __init__(self, config):
        self.config = config

        NETFILE_API_KEY = os.getenv('NETFILE_API_KEY','')
        NETFILE_API_SECRET = os.getenv('NETFILE_API_SECRET','')
        REPO_OWNER = os.getenv('REPO_OWNER','')
        if ((NETFILE_API_KEY != '') and (NETFILE_API_SECRET != '')) or os.path.exists('.env'):
            print(f'Making NetFile API calls')
            self.nf = NetFileClient(api_key='',api_secret='')

        elif (REPO_OWNER != '') and (REPO_OWNER not in ['ChenglimEar']):
            raise Exception('No NetFile credentials provided when expected')
        else:
            print(f'Simulating NetFile response since no credentials provided')
            self.nf = None

        os.makedirs('netfile_redacted', exist_ok=True)

    def fetch_and_redact_all(self):
        data_keys = self.config['redaction_fields'].keys()
        for name in data_keys:
            data = retriever.fetch(name)
            self.redact(data, name)
            with open(f'netfile_redacted/{name}.json','w') as f:
                json.dump(data,f,sort_keys=True,indent=1)


    def fetch(self,name):
        if self.nf is None:
            filepath = f'netfile_samples/{name}.json'
            if os.path.exists(filepath):
                with open(filepath,'r') as f:
                    data = json.load(f)
            else:
                data = []
        else:
            data = self.nf.fetch(name)
        return data

    def redact_path(self, data, path):
        parts = path.split('.',1)
        if len(parts) == 1:
            data[path] = '***'
        elif parts[0] == '[]':
            for i,v in enumerate(data):
                self.redact_path(v, parts[1])
        else:
            self.redact_path(data[parts[0]], parts[1])

    def redact(self, data, data_key):
        fields_to_redact = self.config['redaction_fields'][data_key]

        for item in data:
            for field_path in fields_to_redact:
                self.redact_path(item, field_path)

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    retriever = DataRetriever(config)
    retriever.fetch_and_redact_all()


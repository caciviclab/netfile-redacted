import os
import json
import yaml
from netfile_client.NetFileClient import NetFileClient

class DataRetriever:
    ''' Used to retrieve and redact files
    
        It accesses the NetFile API to get files, redacts the contents 
        and saves it to a local directory. If no credentials are provided for NetFile, 
        it will simply copy files from netfile_samples to simulate data 
        retrieved from NetFile.

        Environment variables used:
          NETFILE_API_KEY: the api key for accessing NetFile API
          NETFILE_API_SECRET: the api secret for accessing NetFile API
        
        '''
    
    def __init__(self, config, dest_dirpath='.local/netfile_redacted'):
        ''' Initialize with redaction configuration, destination directory and NetFile client '''

        self.config = config
        self.dest_dirpath = dest_dirpath

        NETFILE_API_KEY = os.getenv('NETFILE_API_KEY','')
        NETFILE_API_SECRET = os.getenv('NETFILE_API_SECRET','')

        if ((NETFILE_API_KEY != '') and (NETFILE_API_SECRET != '')) or os.path.exists('.env'):
            print(f'Making NetFile API calls')
            self.nf = NetFileClient(api_key='',api_secret='')
        else:
            print(f'Simulating NetFile response since no credentials provided')
            self.nf = None

        os.makedirs(self.dest_dirpath, exist_ok=True)

    def fetch_and_redact_all(self):
        ''' Get names of content to fetch from NetFile, redact and save '''

        data_keys = self.config['redaction_fields'].keys()
        for name in data_keys:
            data = self.fetch(name)
            self.redact(data, name)
            with open(f'{self.dest_dirpath}/{name}.json','w') as f:
                json.dump(data,f,sort_keys=True,indent=1)


    def fetch(self,name):
        ''' Fetch a specific named content, which may be simulated if NetFile client not initialized '''

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
        ''' Redact a specific entry in the JSON data located through a provided path 
        
            Parameters:
              data: the JSON data
              path: the path to the entry to redact
            '''

        parts = path.split('.',1)
        if len(parts) == 1:
            if (type(data) == dict) and (path in data):
                data[path] = '***'
        elif parts[0] == '[]':
            if (type(data) == list):
                for i,v in enumerate(data):
                    self.redact_path(v, parts[1])
        else:
            if (type(data) == dict) and (parts[0] in data):
                self.redact_path(data[parts[0]], parts[1])

    def redact(self, data, data_key):
        ''' Apply all configured redactions for a provided content
         
            Parameters:
              data: the content
              data_key: the name of the content
            '''

        fields_to_redact = self.config['redaction_fields'][data_key]

        for item in data:
            for field_path in fields_to_redact:
                self.redact_path(item, field_path)

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    retriever = DataRetriever(config)
    retriever.fetch_and_redact_all()


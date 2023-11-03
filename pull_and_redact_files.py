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

        self.redaction_fields = config['redaction_fields']
        self.endpoint_spec = config['endpoints']
        self.dest_dirpath = dest_dirpath

        netfile_api_key = os.getenv('NETFILE_API_KEY','')
        netfile_api_secret = os.getenv('NETFILE_API_SECRET','')

        if ((netfile_api_key != '') and (netfile_api_secret != '')) or os.path.exists('.env'):
            print('Making NetFile API calls')
            self.nf = NetFileClient()
        else:
            print('Simulating NetFile response since no credentials provided')
            self.nf = None

        os.makedirs(self.dest_dirpath, exist_ok=True)


    def fetch_and_redact_all(self):
        ''' Get names of content to fetch from NetFile, redact and save '''

        for name, extra_params in self.endpoint_spec.items():
            print(f'Fetch {name} with params {extra_params}')
            data = self.fetch(name, extra_params)
            print(f'Got {name} of {len(data)} rows')

            if name in self.redaction_fields:
                print(f'Redact {name}')
                self.redact(data, name)

            with open(outpath := f'{self.dest_dirpath}/{name}.json','w', encoding='utf8') as f:
                print(f'Save {name} to {outpath}')
                json.dump(data,f,sort_keys=True,indent=1)


    def fetch(self,name, extra_params):
        ''' Fetch a specific named content, which may be simulated if NetFile client not initialized '''

        if self.nf is None:
            filepath = f'netfile_samples/{name}.json'
            if os.path.exists(filepath):
                with open(filepath,'r', encoding='utf8') as f:
                    data = json.load(f)
            else:
                data = []
        else:
            print(f'Pass extra_params {extra_params} to self.nf.fetch')
            data = self.nf.fetch(name, params=extra_params)
        return data


    def redact_path(self, data, path):
        ''' Redact a specific entry in the JSON data located through a provided path 
        
            Parameters:
              data: the JSON data
              path: the path to the entry to redact
            '''

        parts = path.split('.',1)
        if len(parts) == 1:
            if isinstance(data, dict) and (path in data):
                data[path] = '***'
        elif parts[0] == '[]':
            if isinstance(data, list):
                for i,v in enumerate(data):
                    self.redact_path(v, parts[1])
        else:
            if isinstance(data, dict) and (parts[0] in data):
                self.redact_path(data[parts[0]], parts[1])


    def redact(self, data, data_key):
        ''' Apply all configured redactions for a provided content
         
            Parameters:
              data: the content
              data_key: the name of the content
            '''

        fields_to_redact = self.redaction_fields[data_key]

        for item in data:
            for field_path in fields_to_redact:
                self.redact_path(item, field_path)


def main():
    ''' Pull and redact data based what specified in on config.yaml '''
    with open('config.yaml', 'r', encoding='utf8') as f:
        config = yaml.safe_load(f)

    retriever = DataRetriever(config)
    retriever.fetch_and_redact_all()


if __name__ == '__main__':
    main()

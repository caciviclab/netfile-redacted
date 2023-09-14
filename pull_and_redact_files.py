import os
import json

print('Replace this with python script to pull and redact files')

os.makedirs('netfile_redacted')
data = {'msg':'hello'}
with open('netfile_redacted/data.json','w') as f:
  json.dump(data,f)

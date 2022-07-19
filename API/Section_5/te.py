import json
import subprocess


password = ''

with open('config.json', 'r') as f:
  data = json.load(f)



for d in data['connection']['mysql']['password']:
    if d!='&':
        password+=d
    else:
        password+='\&'


val = subprocess.check_call("./execute.sh '%s'" % password, shell=True)


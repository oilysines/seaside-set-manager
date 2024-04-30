import os
import json

path = os.getcwd()

file = open(r'%s\banpattern.json' % path)
data = json.load(file)

for i in data['bans']:
    print(i['pattern'])

file.close()

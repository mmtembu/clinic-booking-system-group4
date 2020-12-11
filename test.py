import json
import os

data = {}
data['info'] = []

data['info'].append({
    'species' : 'human',
    'name' : 'mangaliso',
    'address' : '839 bluegum street',
    'gender' : 'male'
})

data['info'].append({
    'species' : 'moncalamari',
    'name' : 'stowza',
    'address' : '45 loveday street',
    'gender' : 'male'
})

with open(os.getcwd()+'/info.json', 'w') as outfile:
    json.dump(data, outfile)
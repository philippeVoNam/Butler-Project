import json

with open('data.json') as json_file:
    data = json.load(json_file)
    for p in data['Tuesday']:
        print('Task: ' + p['task'])
        print('startTime: ' + p['startTime'])
        print('endTime: ' + p['endTime'])
        print('duration: ' + p['duration'])
        print('')
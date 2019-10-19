# Schedule of Day
2019-October-18 09:51:31

- Have a schedule for :
  - when to wake up
  - when to go to school
  - when to do hmk
    - specify which hmk todo
  - when to eat
  - when to OW 
  - when to sleep
  - when to DropGenie

- whenever I run 
  - butler --schedule --show
    - shows two tables
      - one for the day
      - another for the week
  - butler  --schedule 
    - shows the current task I should be doing and how much time left on it 

How the schedule data is stored :
    - JSON ? 

JSON Data stored and read :
- https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

Example JSON :

{
    "Monday": [
        {
            "task": "P",
            "startTime": "stackabuse.com",
            "endTime": "Nebraska",
            "duration": "10"
        },
        {
            "task": "T",
            "startTime": "stackabuse.com",
            "endTime": "Nebraska",
            "duration": "10"
        },
        {
            "task": "S",
            "startTime": "stackabuse.com",
            "endTime": "Nebraska",
            "duration": "10"
        }
    ],
    "Tuesday": [
        {
            "task": "V",
            "startTime": "stackabuse.com",
            "endTime": "Nebraska",
            "duration": "10"
        },
        {
            "task": "B",
            "startTime": "stackabuse.com",
            "endTime": "Nebraska",
            "duration": "10"
        },
        {
            "task": "N",
            "startTime": "stackabuse.com",
            "endTime": "Nebraska",
            "duration": "10"
        }
    ]
}

ordered by time 
druation in min 
Monday :
    - task
    - startTime
    - endTime
    - duration

Read JSON File :

```python
import json

with open('data.json') as json_file:
    data = json.load(json_file)
    for p in data['Monday']:
        print('Task: ' + p['task'])
        print('startTime: ' + p['startTime'])
        print('endTime: ' + p['endTime'])
        print('')
```

- Each Task should be 25 min 
- after each task 5 min break 

- class Schedule :
  - show schedule day
  - show schedule week
  - output task and time left - depending on current time and day 
  
  - get current day string 
  - get current time string 

- tables : from terminaltables import AsciiTable
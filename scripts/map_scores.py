import json
import os
import time
import datetime
import dateutil.parser

fp = open(os.path.abspath('/Users/squinones14/tmp/es-tutorial-research/recency_output.json'))
output = json.load(fp)

output = output['hits']['hits']
scores = [score['fields']['published'] for score in output]

for score in scores:
    print(int(time.mktime(dateutil.parser.parse(score[0]).timetuple())))

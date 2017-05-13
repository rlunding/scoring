from datetime import timedelta
import dateutil.parser
import json
from pprint import pprint

with open('push_test/push_test_at_44.txt') as data_file:
    data = json.load(data_file)

time_array = []
for log in data['logs']:
    time_receiver = dateutil.parser.parse(log['timestamp_receiver'])
    time_sender = dateutil.parser.parse(log['timestamp_sender'])
    time_diff = time_receiver - time_sender
    time_array.append(time_diff.total_seconds())

with open('push_test/push_test_diff_time.txt', "w+") as write_file:
    for item in time_array:
        write_file.write("%s\n" % item)


pprint(time_array)

#pprint(data[''])
from datetime import timedelta
import dateutil.parser
import json
from pprint import pprint

file_to_open = 'push_test/push_test_at_44.txt'
file_to_write = 'push_test/push_test_diff_distribution.txt'

with open(file_to_open) as data_file:
    data = json.load(data_file)

time_array = [0] * 30
for log in data['logs']:
    time_receiver = dateutil.parser.parse(log['timestamp_receiver'])
    time_sender = dateutil.parser.parse(log['timestamp_sender'])
    time_diff = time_receiver - time_sender
    time_diff = int(time_diff.total_seconds())
    #time_array.append(time_diff.total_seconds())

    time_array[time_diff] = time_array[time_diff] + 1


with open(file_to_write, "w+") as write_file:
    for item in time_array:
        write_file.write("%s\n" % item)


pprint(time_array)

#pprint(data[''])
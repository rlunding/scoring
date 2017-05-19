from datetime import timedelta
import dateutil.parser
import json
from pprint import pprint

file_to_open = 'stress_test/1_sec_push_at_44.txt'
file_to_write = 'gnuplot/1sec/1_sec_push_at_44_diff_distribution_gnuplot.dat'

with open(file_to_open) as data_file:
    data = json.load(data_file)

time_array = [0] * 60
for log in data['logs']:
    time_receiver = dateutil.parser.parse(log['timestamp_receiver'])
    time_sender = dateutil.parser.parse(log['timestamp_sender'])
    time_diff = time_receiver - time_sender
    time_diff = int(time_diff.total_seconds())
    #time_array.append(time_diff.total_seconds())

    time_array[time_diff] = time_array[time_diff] + 1


with open(file_to_write, "w+") as write_file:
    count = 0
    for item in time_array:
        write_file.write("%s %s\n" % (count, item))
        count = count + 1


pprint(time_array)

#pprint(data[''])
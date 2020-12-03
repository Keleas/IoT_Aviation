import csv
import pandas as pd
from itertools import zip_longest
import json


def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

header = ['time', 'topic', 'message']
data = []
with open('data.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|', lineterminator='\n')
    for row in grouper(3, spamreader):
        # print(len(row))
        # print(list(row))
        data.append(row)
        # print(1, ', '.join(row))

df = pd.DataFrame(data, columns=header)
print(df.head())

msg = df.message.iloc[0][0][1:-1]
# print(msg)

all_keys = ['measurement',
            'aircraft_id', 'cicle',

            'setting1', 'setting2', 'setting3', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21']

json_acceptable_string = msg.replace("'", "\"")
cur_dict = json.loads(json_acceptable_string)
print(cur_dict.keys())
line_data = []
for key in cur_dict.keys():
    if key in ['tags', 'fields']:
        d = cur_dict[key]
        print(d.keys())
        for key in d.keys():
            print(d[key])
            pass
    # print(cur_dict[key])

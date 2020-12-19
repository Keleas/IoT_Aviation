import csv
import json
from itertools import zip_longest
import pandas as pd
from tqdm import tqdm
from src.mqtt_broker.src.case_consumer import crete_tag_time


def grouper(n, iterable, fillvalue=None):
    """
    Group iterable objects by n elements like.
        Example: "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    :param n: count of itarate
    :param iterable: current iterable objects
    :param fillvalue: value for fill nan objects which includes to over iterate
    :return: iterable object by n elements
    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def read_from_raw_data(fname='data.csv'):
    """
    Read data from online writer csv data frame with columns: time, topic and message.
        time_rec - tag time when message was received message
        topic - topic name which was received message
        message - current information, str structure
    :param fname: file path
    :return: df data
    """
    header = ['time_rec', 'topic', 'message']
    data = []
    with open(fname, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|', lineterminator='\n')
        for row in grouper(3, spamreader):
            data.append(row)

    df = pd.DataFrame(data, columns=header)
    return df


def extract_data(df, idx):
    """
    Parse one line data from data frame.
    :param df: pandas data frame
    :param idx: index of data from data frame (df)
    :return: tuple: line of all data with params order:
        'time', 'topic', 'measurement', 'aircraft_id', 'cicle', 'time',
        'setting1', 'setting2', 'setting3',
        's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10',
        's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21'
    """
    topic = df.topic.iloc[idx][0]
    line_data = [topic]   # parsed data

    msg = df.message.iloc[idx][0][1:-1]  # get message with data
    json_acceptable_string = msg.replace("'", "\"")  # replace for parse
    cur_dict = json.loads(json_acceptable_string)  # create dict from str line dict
    for key in cur_dict.keys():  # parse data from keys to one tuple
        if key in ['tags', 'fields']:  # another dict to parse
            d = cur_dict[key]
            for key_ in d.keys():
                line_data.append(d[key_])
        else:
            line_data.append(cur_dict[key])
    return line_data


if __name__ == '__main__':
    df = read_from_raw_data('data.csv')  # create df from raw data

    data = []  # format data to pandas data frame
    for idx in tqdm(range(df.shape[0])):
        data.append(extract_data(df, idx))

    all_keys = [
        'topic',
        'measurement',
        'aircraft_id', 'cicle',
        'time',
        'setting1', 'setting2', 'setting3',
        's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10',
        's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20', 's21'
    ]

    tag_time = crete_tag_time().replace(':', '-')
    final_df = pd.DataFrame(data, columns=all_keys)
    final_df.to_csv(f'../../input/final_df_{tag_time}.csv', index=False)


import os
import csv
import json

DATAFILE = os.path.abspath(os.getcwd() + '/data/household_power_consumption.txt')
INDEX = "energy_use"

class Record:
    _data = {}

    def __init__(self, raw_row):
        self._data['date'] = raw_row[0] if raw_row[0] else None
        self._data['time'] = raw_row[1] if raw_row[1] else None
        self._data['global_active_power'] = float(raw_row[2]) if raw_row[2] else None
        self._data['global_reactive_power'] = float(raw_row[3]) if raw_row[3] else None
        self._data['voltage'] = float(raw_row[4]) if raw_row[4] else None
        self._data['global_intensity'] = raw_row[5] if raw_row[5] else None
        self._data['kitchen'] = float(raw_row[6]) if raw_row[6] else None
        self._data['laundry'] = float(raw_row[7]) if raw_row[7] else None
        self._data['heater'] = float(raw_row[8]) if raw_row[8] else None
        self._data['other'] = float(self.get_other_power())

    def get_other_power(self):
        return self._data['global_active_power']*1000/60 - self._data['kitchen'] - self._data['laundry'] - self._data['heater']

    @staticmethod
    def get_control():
        return {
            "index": {
                "_index": INDEX,
                "_type": "reading",
            }
        }

    def get_document(self):
        return self._data

    def __repr__(self, *args, **kwargs):
        return json.dumps(self.get_control()) + "\n" + json.dumps(self.get_document())


with open(DATAFILE) as datafile:
    reader = csv.reader(datafile, delimiter=";")
    next(reader, None)
    count = 0;
    for row in reader:
        if count >= 1000:
            break

        if "?" in row:
            continue

        post = Record(row)
        print(post)
        count += 1

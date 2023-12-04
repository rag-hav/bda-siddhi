
from PySiddhi.DataTypes.DataWrapper import DoubleType
from PySiddhi.DataTypes.LongType import LongType
from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent
from time import sleep
import os, csv
from collections import defaultdict
from datetime import datetime
import calendar
from info import streams


siddhiManager = SiddhiManager()

with open("staticthreshold.txt", 'r') as f:
    siddhiApp = f.read()

siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)

class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        pass
        # PrintEvent(timestamp, inEvents, outEvents)

inputHandlers = {}

siddhiAppRuntime.addCallback("alerts" , QueryCallbackImpl())

for s in streams[:1]:
    siddhiAppRuntime.addCallback("query_" + s, QueryCallbackImpl())
    inputHandlers[s] = siddhiAppRuntime.getInputHandler(s)

siddhiAppRuntime.start()

events = []

dataset_dir = 'dataset'

for fname in os.listdir(dataset_dir):
    if fname.endswith("Information.csv"):
        continue

    if not fname.startswith("Building"):
        continue

    with open(os.path.join(dataset_dir, fname), 'r') as f:
        reader = csv.reader(f)
        headers = next(reader) # headers
        next(reader) # units

        for line in reader:
            t = datetime.strptime(line[0], "%m/%d/%Y %H:%M")
            timestamp = LongType(calendar.timegm(t.timetuple()))
            for i, e in enumerate(line[1:]):
                try:
                    if (headers[i + 1] == "T_Stair_101"):
                        events.append((timestamp, headers[i + 1], DoubleType(e)))
                except ValueError:
                    pass

print(len(events))
events.sort(key = lambda a : a[0]) # sort by timestamp

import time
t = time.time()

for e in events[:10000]:
    inputHandlers[e[1]].send([ e[0], e[2] ])

print(time.time() - t)





sleep(10)

siddhiManager.shutdown()

from PySiddhi.DataTypes.LongType import LongType
from PySiddhi.core.SiddhiManager import SiddhiManager
from PySiddhi.core.query.output.callback.QueryCallback import QueryCallback
from PySiddhi.core.util.EventPrinter import PrintEvent
from time import sleep
import os, csv
from collections import defaultdict
from datetime import datetime


siddhiManager = SiddhiManager()

with open("echoapp.txt", 'r') as f:
    siddhiApp = f.read()

siddhiAppRuntime = siddhiManager.createSiddhiAppRuntime(siddhiApp)

class QueryCallbackImpl(QueryCallback):
    def receive(self, timestamp, inEvents, outEvents):
        PrintEvent(timestamp, inEvents, outEvents)


siddhiAppRuntime.addCallback("query1", QueryCallbackImpl())
inputHandler = siddhiAppRuntime.getInputHandler("InputStream")

siddhiAppRuntime.start()

events = []

dataset_dir = 'dataset'

for fname in os.listdir(dataset_dir):
    if fname.endswith("Information.csv"):
        continue
    
    if fname.startswith("Building"):
        filetype = 0
    else:
        filetype = 1

    with open(os.path.join(dataset_dir, fname), 'r') as f:
        reader = csv.reader(f)
        headers = next(reader) # headers
        next(reader) # units

        for line in reader:
            timestamp = datetime.strptime(line[0], "%m/%d/%Y %H:%M").timestamp()

            for i, e in enumerate(line[1:]):
                try:
                    events.append((timestamp, headers[i + 1], float(e)))
                except ValueError:
                    pass

events.sort(key = lambda a : a[0]) # sort by timestamp

for e in events:
    inputHandler.send([ e[-1] ])





sleep(10)

siddhiManager.shutdown()

# pylint: disable=C0103
# pylint: disable=C0111

import json
import os

measurementFileName = "measurements"

def Setup():
    # If the file where to store the measurements does not exist, we create a new one.
    if not os.path.exists(measurementFileName):
        f = file(measurementFileName, "w+")
        f.close()

def ProcessMeasurements(measurements):
    measurementJson = None
    try:
        measurementJson = json.loads(measurements)
    except:
        print("Measurements not in a json format")
    if measurementJson:
        StoreMeasurementsOnSystem(measurementJson)
        SendMeasurementsToApi(measurementJson)

def StoreMeasurementsOnSystem(measurementJson):
    print("Storing measurements locally")
    with open(measurementFileName, "a") as measurementFile:
        measurementFile.write(measurementJson)

def SendMeasurementsToApi(measurementJson):
    print("Sending measurements to the api")

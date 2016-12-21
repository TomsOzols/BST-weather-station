# pylint: disable=C0103
# pylint: disable=C0111

import json
# import os
# import Database
import PlotlyClient

measurementFileName = "measurements"
configurationFileName = "BSConfig.json"
measurementTableFid = "measurementTableFid"
plotlyUserName = "plotlyUserName"

# def Setup():
    # Database.InitiateDatabase()

def ProcessMeasurements(measurement):
    measurementJson = None
    configuration = GetConfiguration()
    configurationChanged = False
    try:
        measurementJson = json.loads(measurement)
    except:
        print("Measurements not in a json format")

    if not configuration[measurementTableFid]:
        configuration[measurementTableFid] = CreateNewTableAndGetFid(configuration)
        configurationChanged = True

    if measurementJson:
        # Database.InsertMeasurements(measurementJson)

        # Should move this out.
        plotlyJson = CreatePlotlyMeasurementRowJson(measurementJson)
        try:
            gridUrl = "{}:{}".format(configuration[plotlyUserName], configuration[measurementTableFid])
            PlotlyClient.SendMeasurementsToApi(plotlyJson, gridUrl)
        except:
            newTableFid = CreateNewTableAndGetFid(configuration)
            gridUrl = "{}:{}".format(configuration[plotlyUserName], newTableFid)
            PlotlyClient.SendMeasurementsToApi(plotlyJson, newTableFid)
            configuration[measurementTableFid] = newTableFid
            configurationChanged = True

    if configurationChanged:
        WriteToConfigurationFile(configuration)

def CreateNewTableAndGetFid(configuration):
    newTableFid = PlotlyClient.CreateMeasurementTable()
    configuration[measurementTableFid] = newTableFid
    WriteToConfigurationFile(configuration)
    return newTableFid

def GetConfiguration():
    with open(configurationFileName) as configFile:
        return json.load(configFile)

def WriteToConfigurationFile(configuration):
    with open(configurationFileName, 'w') as outfile:
        json.dump(configuration, outfile)

def CreatePlotlyMeasurementRowJson(measurement):
    return {
        "rows":[
            [measurement["temperature"]],
            [measurement["humidity"]],
            [measurement["windDirection"]],
            [measurement["windSpeed"]],
            [measurement["rain"]]
        ]
    }

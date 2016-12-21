# pylint: disable=C0103
# pylint: disable=C0111

import json
import Database
import PlotlyClient

configurationFileName = "BSConfig.json"
measurementTableFid = "measurementTableFid"
plotlyUserName = "plotlyUserName"

def Setup():
    Database.InitiateDatabase()

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
        sqlLiteTuples = CreateSQLLiteTupleList(measurementJson)
        Database.InsertMeasurements(sqlLiteTuples)

        # Should move this out.
        plotlyJson = CreatePlotlyMeasurementRowsJson(measurementJson)
        try:
            gridUrl = "{}:{}".format(configuration[plotlyUserName], configuration[measurementTableFid])
            PlotlyClient.SendMeasurementsToApi(plotlyJson, gridUrl)
        except:
            userNameAndFid = CreateNewTableAndGetFid(configuration) # Cause plotly rest sucks
            newTableFid = userNameAndFid.split(":")[1]
            gridUrl = "{}:{}".format(configuration[plotlyUserName], newTableFid)
            PlotlyClient.SendMeasurementsToApi(plotlyJson, gridUrl) # Could've sent the measurement on table creation. Dont wanna arse myself for now.
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

temperature = "temperature"
humidity = "humidity"
windDirection = "windDirection"
windSpeed = "windSpeed"
rain = "rain"


def CreatePlotlyMeasurementRow(measurement):
    return [measurement[temperature], measurement[humidity], measurement[windDirection], measurement[windSpeed], measurement[rain]]

def CreatePlotlyMeasurementRowsJson(measurements):
    measurementRows = [CreatePlotlyMeasurementRow(measurement) for measurement in measurements]

    return {
        "rows": measurementRows
    }

def CreateSQLLiteTupleList(measurements):
    return [CreateSQLLiteTuple(measurement) for measurement in measurements]

def CreateSQLLiteTuple(measurement):
    return (
        measurement[temperature],
        measurement[humidity],
        measurement[windDirection],
        measurement[windSpeed],
        measurement[rain])

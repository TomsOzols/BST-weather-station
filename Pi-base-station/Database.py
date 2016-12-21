# pylint: disable=C0103
# pylint: disable=C0111

import sqlite3 as database

temperature = ("REAL", "temperature")
humidity = ("REAL", "humidity")
windDirection = ("INT", "windDirection")
windSpeed = ("REAL", "windSpeed")
rain = ("REAL", "rain")

measurementTableName = "Measurement"
databaseName = "measurements.db"

def InitiateDatabase():
    connectionObject = database.connect(databaseName)
    CreateMeasurementTableIfNotExist(connectionObject)

def CreateMeasurementTableIfNotExist(connectionObject):
    with connectionObject:
        databaseContext = connectionObject.cursor()
        dataColumns = "{},{},{},{},{}".format(
            GetColumnDefinition(temperature),
            GetColumnDefinition(humidity),
            GetColumnDefinition(windDirection),
            GetColumnDefinition(windSpeed),
            GetColumnDefinition(rain))

        allColumns = "(Id INTEGER PRIMARY KEY AUTOINCREMENT, {})".format(dataColumns)
        query = "CREATE TABLE IF NOT EXISTS {} {}".format(measurementTableName, allColumns)
        databaseContext.execute(query)

def GetColumnDefinition(tuple):
    return "{} {}".format(tuple[1], tuple[0])

def InsertMeasurements(measurements):
    # columns = "{},{},{},{},{}".format(temperature[1], humidity[1], windDirection[1], windSpeed[1], rain[1]
    # columnValues = "VALUES({})".format(columns)

    tableDefinition = "({}, {}, {}, {}, {})".format(temperature[1], humidity[1], windDirection[1], windSpeed[1], rain[1])
    columnValues = "VALUES({})".format("?, ?, ?, ?, ?")
    connection = database.connect(databaseName)
    with connection:
        databaseContext = connection.cursor()
        databaseContext.executemany("INSERT INTO {} {} {}".format(measurementTableName, tableDefinition, columnValues), measurements)
        # databaseContext.executemany("INSERT INTO {} {}".format(measurementTableName, columnValues), measurements)
        
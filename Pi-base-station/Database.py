# pylint: disable=C0103
# pylint: disable=C0111

import sqlite3 as database

measurementTableName = "Measurement"
connection = InitiateDatabase()

def InitiateDatabase():
    connectionObject = database.connect("measurements.db")
    CreateMeasurementTableIfNotExist(connectionObject)
    return connectionObject

def CreateMeasurementTableIfNotExist(connectionObject):
    with connectionObject:
        current = connectionObject.cursor()
        current.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tableNames = current.fetchall()
        measurementTableExists = any(table == measurementTableName for table in tableNames)
        if not measurementTableExists:
            # finish writing the table creation by defining the data types being stored.
            current.execute("CREATE TABLE " + measurementTableName + "(Id INTEGER PRIMARY KEY AUTOINCREMENT, )")

def InsertMeasurements(measurements):
    with connection:
        current = connection.cursor()
        # finish writing the insert value definitions
        current.executemany("INSERT INTO " + measurementTableName + "VALUES()", measurements)
        
from collections import namedtuple
Measurement = namedtuple('Measurement', '') # finish this up by defining the field/property names.

## A simple example on how to easily map a namedtuple with the data structure from a database, or maybe incoming measurements
# import sqlite3
# conn = sqlite3.connect('/companydata')
# cursor = conn.cursor()
# cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
# for emp in map(EmployeeRecord._make, cursor.fetchall()):
#     print(emp.name, emp.title)

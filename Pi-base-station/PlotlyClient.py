# pylint: disable=C0103
# pylint: disable=C0111

workingOnRaspberry = True
import json as json
if workingOnRaspberry:
    import requests as requests
    from requests.auth import HTTPBasicAuth

else:
    import Mock.requests as requests
    from Mock.requests.auth import HTTPBasicAuth

plotlyApiBaseUrl = "https://api.plot.ly"
gridApiUrl = "v2/grids"

# The authentication is made using the Plot.ly username and API key
auth = HTTPBasicAuth('BSTGrupa5', 'oEP9bWrgM1vitAjkyszF')
headers = {'Plotly-Client-Platform': 'python'}

staticTable = {
    "data": {
        "cols":{
            "Temperature":{
                "data": [],
                "order": 0
            },
            "Humidity":{
                "data": [],
                "order": 1
            },
            "Wind direction":{
                "data": [],
                "order": 2
            },
            "Wind speed":{
                "data": [],
                "order": 3
            },
            "Rain":{
                "data": [],
                "order": 4
            }
        }
    }}

def SendMeasurementsToApi(rows, tableUrl):
    requestUrl = "{}/{}/{}/row".format(plotlyApiBaseUrl, gridApiUrl, tableUrl)
    request = requests.post(requestUrl, auth=auth, headers=headers, json=rows)
    if request.status_code == 404:
        raise Exception("Missing grid: {}".format(tableUrl))
    print(request.text)

def CreateMeasurementTable():
    requestUrl = "{}/{}".format(plotlyApiBaseUrl, gridApiUrl)
    print(requestUrl)
    print(auth)
    print(headers)
    print(staticTable)
    request = requests.post(requestUrl, auth=auth, headers=headers, json=staticTable)
    print(request.text)
    return json.loads(request.text)

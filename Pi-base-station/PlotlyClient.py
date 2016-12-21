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
    if not (request.status_code == 201):
        raise Exception("Missing grid: {}".format(tableUrl))

def CreateMeasurementTable():
    requestUrl = "{}/{}".format(plotlyApiBaseUrl, gridApiUrl)
    request = requests.post(requestUrl, auth=auth, headers=headers, json=staticTable)
    responseContent = json.loads(request.text)
    return responseContent["file"]["fid"]

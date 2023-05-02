

import requests

domain = "192.168.1.11"

try:
    x = requests.get('http://{}/sensor/get/override'.format(domain))
    command = x.json
except:
    print("1st")
    

    
data = x.json()
print(x.text)


# {"message":"Successfully added.","result":true,"sensor":{"OnID":53,"Humidifier":"1","Fan":"1","waterpump":"0","archived":null,"updated_at":"2023-05-03T01:45:27.000000Z"}}
# 53
# {"message":"Successfully set","result":false,"Override":{"OverrideID":1,"Override":"0","archived":null,"updated_at":"2023-05-02T20:18:38.000000Z"}}
# >>>
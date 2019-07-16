# GPS Data feeder fro GPSD for W3C-VIS-Server

Fetches data from gpsd and feeds latitude and longitude into w3c-visserver.

## Requirements

Feeder uses websocket_client lib to connect to w3c-visserver.

The client can access GPSD. For this it uses the gps3 library: https://pypi.org/project/gps3 or  https://github.com/wadda/gps3 
It uses python requests for talking to Traccar

Install it with 

`pip3 install -r ./requirements.txt`



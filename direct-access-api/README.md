# Direct Access API (DAA)
Powered By
[![N|Solid](https://www.eclipse.org/kuksa/img/kuksa-logo-h-209x79.png)](https://www.eclipse.org/kuksa/)

The API acts as a gateway between in-vehicle platform and vehicle CANBus, which allows in-vehicle applications to exchange RAW CANBus data with the vehicle.

## New Features!

  - Local authentication of In-Vehicle applications based on CANBus interface, mesage Id and read/write function 
  - Creating virtual CANBus interface per In-Vehicle application
  - Batch vehicle data messages sending over Hono
  - Embedded "Driver Authentication" scenario application

## Tech

  -  Direct Access API (DAA) is developed by C++ Language
  -  Direct Access API (DAA) uses [OBU 102] ([obsolete]) device for CANBus communication
  -  Communication between Direct Access API (DAA) and [OBU 102] is carried out over TCP/IP protocol  

## Building from source

Direct Access API (DAA) is automatically build within [agl-kuksa] image. 

## Todos

 - Application based messaging with Hono
 - Server authenticaon mechanism for In-Vehicle applications

License
----

Eclipse Public License v2.0

   [agl-kuksa]: <https://github.com/eclipse/kuksa.invehicle/tree/master/agl-kuksa >
   [OBU 102]:   <https://unex.com.tw/products/dsrc-v2x/technology/v2x-on-board-unit#mainpro>
   [obsolete]:  <http://cvt-project.ir/Admin/Files/eventAttachments/Unex%20OBU-102%20datasheet_258.pdf>

# W3C VIS Server Implementation

The implementation is based on the [specification](https://www.w3.org/TR/2018/CR-vehicle-information-service-20180213/)

The implementation at the moment is in a nacent state and includes only the basic functionalities mentioned in the specification. At the moment, the security related functions have not been touched upon but will be updated shortly. This project uses components from other open source projects namely

1. [Simple-WebSocket-Server](https://gitlab.com/eidheim/Simple-WebSocket-Server) which is under MIT license.
2. [jsoncons](https://github.com/danielaparker/jsoncons) which is under Boost Software License.

This application needs the input vss data to creat the tree structure. The input files can be taken from https://github.com/GENIVI/vehicle_signal_specification/blob/master/vss_rel_1.0.csv and https://github.com/GENIVI/vehicle_signal_specification/blob/master/vss_rel_1.0.json. Clone the files and place them in the build folder where the executables are built. Keep the names of the files the same.

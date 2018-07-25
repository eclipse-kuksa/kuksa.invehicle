# W3C VIS Server Implementation

The implementation is based on the [W3C Vehicle Information Service Specification](https://www.w3.org/TR/2018/CR-vehicle-information-service-20180213/)


The implementation at the moment is in a nacent state and includes only the basic functionalities mentioned in the specification. At the moment, the security related functions have not been touched upon but will be updated shortly. This project uses components from other open source projects namely

1. [Simple-WebSocket-Server](https://gitlab.com/eidheim/Simple-WebSocket-Server) which is under MIT license.
2. [jsoncons](https://github.com/danielaparker/jsoncons) which is under Boost Software License.


# How to build
w3c-visserver can be built as a library which could be used in another application. Eg: could be found in the vehicle2cloud app.
```
cd w3c-visserver
mkdir build
cd build
cmake ..
make
```

# How to run
This application needs the input vss data to create the tree structure. The input files can be taken from https://github.com/GENIVI/vehicle_signal_specification/blob/master/vss_rel_1.0.csv and https://github.com/GENIVI/vehicle_signal_specification/blob/master/vss_rel_1.0.json. Clone the files and place them in the build folder where the executables are built. Keep the names of the files the same.
Add the files to the location where the application executable is run from.

# Implementation

| Feature       | Status        |
| ------------- | ------------- |
| GET/SET       | :heavy_check_mark:|
| PUB/SUB  | :heavy_check_mark: |
| GETMETA  | :heavy_check_mark: |
| Authentification  | :heavy_multiplication_x: |
| Secure WebSocket  | :heavy_multiplication_x: |   


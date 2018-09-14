#
# ******************************************************************************
# Copyright (c) 2018 Robert Bosch GmbH and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/index.php
#
#  Contributors:
#      Robert Bosch GmbH - initial API and functionality
# *****************************************************************************
cmake_minimum_required(VERSION 2.8)

#add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../w3c-visserver ${CMAKE_CURRENT_SOURCE_DIR}/../w3c-visserver/build)

project(vehicle2cloud)

message(STATUS ${CMAKE_CURRENT_SOURCE_DIR})

add_compile_options(-std=c++11 )

add_executable(${PROJECT_NAME}  "src/main.cpp" "src/honoHTTP.cpp")
#target_link_libraries(${PROJECT_NAME} w3c-visserver)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR}/../3rd-party-libs ${CMAKE_CURRENT_SOURCE_DIR}/../3rd-party-libs/Simple-WebSocket-Server ${CMAKE_CURRENT_SOURCE_DIR}/../3rd-party-libs/jsoncons)

add_library(simple-websocket-server INTERFACE)

find_package(Threads REQUIRED)
target_link_libraries(simple-websocket-server INTERFACE ${CMAKE_THREAD_LIBS_INIT})

# Boost
find_package(Boost REQUIRED)
set(Boost_USE_STATIC_LIBS ON)
include_directories(${Boost_INCLUDE_DIRS})
message(STATUS " boost includes ${Boost_INCLUDE_DIRS} ")

find_package(Boost 1.54.0 COMPONENTS system thread REQUIRED)
target_link_libraries(simple-websocket-server INTERFACE ${Boost_LIBRARIES})
target_include_directories(simple-websocket-server INTERFACE ${Boost_INCLUDE_DIR})
message(STATUS " boost libs ${Boost_LIBRARIES} ")

#openssl
find_package(OpenSSL REQUIRED)
target_link_libraries(simple-websocket-server INTERFACE ${OPENSSL_LIBRARIES})
target_include_directories(simple-websocket-server INTERFACE ${OPENSSL_INCLUDE_DIR})
message(STATUS " openssl libraries ${OPENSSL_LIBRARIES}")


target_link_libraries(${PROJECT_NAME}  simple-websocket-server)

configure_file(start.sh ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/CA.pem  ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.pem  ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.key  ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)


# uncomment lines below while building AGL image.
install(TARGETS ${PROJECT_NAME} DESTINATION /usr/bin/vehicle2cloud)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/CA.pem DESTINATION /usr/bin/vehicle2cloud)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.pem DESTINATION /usr/bin/vehicle2cloud)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.key DESTINATION /usr/bin/vehicle2cloud)
install (TARGETS ${CMAKE_CURRENT_SOURCE_DIR}/start.sh DESTINATION /usr/bin/vehicle2cloud)


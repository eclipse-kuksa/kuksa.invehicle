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

add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../w3c-visserver ${CMAKE_CURRENT_SOURCE_DIR}/../w3c-visserver/build)

project(vehicle2cloud)

message(STATUS ${CMAKE_CURRENT_SOURCE_DIR})

add_compile_options(-std=c++11 )

add_executable(${PROJECT_NAME}  "src/main.cpp" "./../elm327/obd.cpp" "src/vssMapper.cpp" "src/honoHTTP.cpp")
target_link_libraries(${PROJECT_NAME} w3c-visserver)
target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../elm327 ${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR}/../w3c-visserver/include  ${CMAKE_CURRENT_SOURCE_DIR}/../w3c-visserver/jsoncons)

# uncomment lines below while building AGL image.
install(TARGETS ${PROJECT_NAME} DESTINATION /usr/bin)
#install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/w3c-visserver/vss_rel_1.0.csv DESTINATION /usr/bin)
#install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/w3c-visserver/vss_rel_1.0.json DESTINATION /usr/bin)

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
project(elm327-visdatafeeder)

SET(COMMTYPE "websocket" CACHE STRING "Type of communication with w3c-server. dbus or websocket")

#add_definitions(-DDEBUG)
add_compile_options(-std=c++11 -Wall -Wextra)
if(${COMMTYPE} STREQUAL "dbus") 
   add_executable(${PROJECT_NAME} "dbus/main.cpp" "src/obd.cpp" "src/vssMapper.cpp" )
else()
   add_executable(${PROJECT_NAME} "websocket/main.cpp" "src/obd.cpp" "src/vssMapper.cpp" "src/actuatorTest.cpp")
endif()
   

target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../3rd-party-libs ${CMAKE_CURRENT_SOURCE_DIR}/../3rd-party-libs/Simple-WebSocket-Server ${CMAKE_CURRENT_SOURCE_DIR}/include ${CMAKE_CURRENT_SOURCE_DIR}/../3rd-party-libs/jsoncons)

add_library(simple-websocket-server INTERFACE)

find_package(Threads REQUIRED)
target_link_libraries(simple-websocket-server INTERFACE ${CMAKE_THREAD_LIBS_INIT})

# Boost
find_package(Boost REQUIRED)
set(Boost_USE_STATIC_LIBS ON)
include_directories(${Boost_INCLUDE_DIRS})
message(STATUS " boost includes ${Boost_INCLUDE_DIRS} ")

find_package(Boost 1.58.0 COMPONENTS system thread REQUIRED)
target_link_libraries(simple-websocket-server INTERFACE ${Boost_LIBRARIES})
target_include_directories(simple-websocket-server INTERFACE ${Boost_INCLUDE_DIR})
message(STATUS " boost libs ${Boost_LIBRARIES} ")

#openssl
find_package(OpenSSL REQUIRED)
target_link_libraries(simple-websocket-server INTERFACE ${OPENSSL_LIBRARIES})
target_include_directories(simple-websocket-server INTERFACE ${OPENSSL_INCLUDE_DIR})
message(STATUS " openssl libraries ${OPENSSL_LIBRARIES}")

if(${COMMTYPE} STREQUAL "dbus") 
  #glib, gobject
  FIND_PACKAGE(PkgConfig)
  PKG_CHECK_MODULES(GLIB glib-2.0)
  PKG_CHECK_MODULES(GObject gobject-2.0)
  PKG_CHECK_MODULES(GIO gio-2.0)

  # Add to include paths
  include_directories(${GLIB_INCLUDE_DIRS})
  add_definitions(${GLIB_CFLAGS_OTHER})

  include_directories(${GObject_INCLUDE_DIR})
  link_directories(${GObject_LIBRARY_DIRS})

  include_directories(${GIO_INCLUDE_DIR})
  link_directories(${GIO_LIBRARY_DIRS})

  #add glib libraries
  target_link_libraries(${PROJECT_NAME} -lgobject-2.0 -lglib-2.0 -lgio-2.0)
  target_link_libraries(${PROJECT_NAME}  simple-websocket-server)
endif()


target_link_libraries(${PROJECT_NAME}  simple-websocket-server)

configure_file(start.sh ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/CA.pem  ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.pem  ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.key  ${CMAKE_CURRENT_BINARY_DIR} COPYONLY)

install(TARGETS ${PROJECT_NAME} DESTINATION /usr/bin/elm327-visdatafeeder)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/CA.pem DESTINATION /usr/bin/elm327-visdatafeeder)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.pem DESTINATION /usr/bin/elm327-visdatafeeder)
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/../examples/demo-certificates/Client.key DESTINATION /usr/bin/elm327-visdatafeeder)
install (FILES ${CMAKE_CURRENT_SOURCE_DIR}/start.sh PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE DESTINATION /usr/bin/elm327-visdatafeeder)

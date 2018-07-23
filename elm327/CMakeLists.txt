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
project(elm327)

#add_definitions(-DDEBUG)
add_compile_options(-std=c++11)

add_executable(${PROJECT_NAME} "main.cpp" "obd.cpp")


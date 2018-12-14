 # ******************************************************************************
 # Copyright (c) 2018 Dortmund University of Applied Sciences and Arts
 #
 # All rights reserved. This program and the accompanying materials
 # are made available under the terms of the Eclipse Public License v2.0
 # which accompanies this distribution, and is available at
 # https://www.eclipse.org/org/documents/epl-2.0/index.php
 #
 #  Contributors:
 #      Pedro Cuadra - initial build system and tooling
 # *****************************************************************************

# Define project
project(agl-kuksa NONE)

# Define required cmake version
cmake_minimum_required(VERSION 2.8)

# Include macros
include(tools/cmake/repo.cmake)
include(tools/cmake/versions.cmake)
include(tools/cmake/git.cmake)
include(tools/cmake/agl.cmake)

# TODO Add depencies check

# Other includes
include(ExternalProject)

# Locate the packages
#set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/Modules/")

# Download the repo command
download_repo()

# Create git directory
set(GIT_ROOT_PATH "${CMAKE_BINARY_DIR}/git")
set(TMP_BUILD_PATH "${CMAKE_BINARY_DIR}/tmp")
file(MAKE_DIRECTORY "${TMP_BUILD_PATH}")
file(MAKE_DIRECTORY "${GIT_ROOT_PATH}")


# Clone meta-kuksa repo
set(META_KUKSA_PATH "${CMAKE_SOURCE_DIR}/meta-kuksa")


# Clone meta-kuksa-dev repo
#set(META_KUKSA_DEV_PATH "${GIT_ROOT_PATH}/meta-kuksa-dev")
#git_clone(meta-kuksa-dev
#  "${META_KUKSA_DEV_URL}"
#  "${META_KUKSA_DEV_VERSION}"
#  "${META_KUKSA_DEV_PATH}")

# Clone meta-rover repo
#set(META_ROVER_PATH "${GIT_ROOT_PATH}/meta-rover")
#git_clone(meta-rover
#  "${META_ROVER_URL}"
#  "${META_ROVER_VERSION}"
#  "${META_ROVER_PATH}")


# Prepare output directories
set(IMAGE_PATH "${CMAKE_BINARY_DIR}/images")
set(SDK_PATH "${CMAKE_BINARY_DIR}/sdk")

file(MAKE_DIRECTORY "${IMAGE_PATH}")
file(MAKE_DIRECTORY "${SDK_PATH}")

# Init AGL repository
setup_agl_env()
agl_repo_init()
agl_build_configure()

add_custom_target(agl-kuksa-config
  COMMAND bash "${AGL_BUILD_TMP_PATH}/agl-kuksa-configure.sh"
  WORKING_DIRECTORY "${AGL_ROOT}")

add_custom_target(agl-kuksa-build
  COMMAND bash "${AGL_BUILD_TMP_PATH}/agl-kuksa-build.sh"
  WORKING_DIRECTORY "${AGL_ROOT}")

# Add agl-kuksa target
add_custom_target(agl-kuksa
  COMMAND bash "${AGL_BUILD_TMP_PATH}/agl-kuksa-build.sh"
  DEPENDS agl-kuksa-config
  WORKING_DIRECTORY "${AGL_ROOT}")

# Add agl-kuksa target with SDK
add_custom_target(agl-kuksa-sdk
  COMMAND bash "${AGL_BUILD_TMP_PATH}/agl-kuksa-buildsdk.sh"
  DEPENDS agl-kuksa-config
  WORKING_DIRECTORY "${AGL_ROOT}")




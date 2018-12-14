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

# For cloning the repository
function(agl_clone)

  message("-- Cloning AGL")

  # Check if test mode is on and skip
  if(AGL_TEST_MODE)
    return()
  endif()

  # Check if the repo already exists
  if (EXISTS "${AGL_ROOT}/.repo")
    message("-- Skipping cloning since repository seams to exists already")
    return()
  endif()

  # Clone the repository using repo command
  execute_process(COMMAND ${REPO} init -u "${AGL_URL}"
    WORKING_DIRECTORY "${AGL_ROOT}")

endfunction(agl_clone)

# For pulling latest version of repository
function(agl_sync)

  message("-- Syncing AGL")

  # Remove patches
  execute_process(COMMAND git checkout -- .
    WORKING_DIRECTORY "${AGL_ROOT}/poky")

  # Check if test mode is on and skip
  if(AGL_TEST_MODE)
    return()
  endif()

  # Pull the latest version
  execute_process(COMMAND ${REPO} sync
    WORKING_DIRECTORY "${AGL_ROOT}")

  execute_process(COMMAND git apply "${CMAKE_SOURCE_DIR}/tools/poky.patch"
    WORKING_DIRECTORY "${AGL_ROOT}/poky")

  execute_process(COMMAND git status
    WORKING_DIRECTORY "${AGL_ROOT}/poky")

endfunction(agl_sync)

# For selecting a version and manifest
function(agl_checkout release version)

  message("-- Checking out to ${release}_${version}")

  # Check if test mode is on and skip
  if(AGL_TEST_MODE)
    return()
  endif()

  # Checkout to the selected version
  execute_process(COMMAND ${REPO} init -b ${release}
    -m "${release}_${version}.xml" -u "${AGL_URL}"
    WORKING_DIRECTORY "${AGL_ROOT}")

endfunction(agl_checkout)

# Append KUKSA layers
function(config_layer layer_name layer_path)
  # Set needed variables for configure file
  set(LAYER_PATH "${layer_path}")
  set(LAYER_FILE_PATH "${AGL_BUILD_BBLAYERS_PATH}/${layer_name}.bblayer")
  set(LAYERS_LIST "${LAYERS_LIST} ${layer_name}" PARENT_SCOPE)
  # Configure bblayer file
  configure_file("${CMAKE_SOURCE_DIR}/tools/cmake/bblayers.configure"
    ${LAYER_FILE_PATH} @ONLY)
endfunction(config_layer)

# Initialize the AGL repository
function(agl_repo_init)

  # Create holder directory
  file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/agl")

  if(AGL_TEST_MODE)
    message("-- AGL Test mode is ON skipping cloning/sync/checkout")
  endif()

  # Clone the repository
  agl_clone()

  # Sync the repository
  agl_sync()

  # Checkout to version
  agl_checkout(${AGL_RELEASE} ${AGL_VERSION})

  # Sync the repository
  agl_sync()

endfunction(agl_repo_init)

macro(setup_agl_env)

  # Get test mode flag from environment
  set(AGL_TEST_MODE $ENV{AGL_TEST_MODE})

  # Add arch definition
  add_definitions(${AGL_ARCH})
  add_definitions(${AGL_ROOT})
  add_definitions(${AGL_LAYERS})
  add_definitions(${AGL_EXTRA_LAYERS})
  add_definitions(${DEV_LAYERS})

  # Default agl layers
  if (NOT DEFINED AGL_ARCH)
    set(AGL_LAYERS "agl-demo agl-netboot agl-appfw-smack")
  endif()

  # Add extra layers
  if (DEFINED AGL_EXTRA_LAYERS)
    set(AGL_LAYERS "${AGL_LAYERS} ${AGL_EXTRA_LAYERS}")
  endif()

  if (DEV_LAYERS)
      message("-- Development mode ON adding agl-devel")
      set(AGL_LAYERS "${AGL_LAYERS} agl-devel")
  endif()

  message("-- Using AGL layers ${AGL_LAYERS}")

  # Default architecture
  if (NOT DEFINED AGL_ARCH)
    set(AGL_ARCH "raspberrypi3")
  endif()

  message("-- Using ${AGL_ARCH} Architecture")

  # Set the AGL repository path
  if (NOT DEFINED AGL_ROOT)
    set(AGL_ROOT "${CMAKE_BINARY_DIR}/agl")
  endif()

  message("-- Using AGL root directory ${AGL_ROOT}")

  set(AGL_BBLAYERS_PATH "${AGL_ROOT}/build/conf/bblayers.conf")
  set(AGL_LOCAL_CONF_PATH "${AGL_ROOT}/build/conf/local.conf")
  set(AGL_BUILD_TMP_PATH "${TMP_BUILD_PATH}/agl-build")
  set(AGL_BUILD_BBLAYERS_PATH "${TMP_BUILD_PATH}/agl-build/bblayers")

endmacro(setup_agl_env)

# Source for creating the
macro(agl_build_configure)

  message("-- Cleaning up previous configuration")
  # Remove previous config files
  file(REMOVE_RECURSE ${AGL_BUILD_TMP_PATH})
  file(MAKE_DIRECTORY ${AGL_BUILD_TMP_PATH})
  file(MAKE_DIRECTORY ${AGL_BUILD_BBLAYERS_PATH})

  message("-- Creating KUKSA Layers files")

  #Clear layers list
  set(LAYERS_LIST "")

  # Meta kuksa layer
  config_layer(meta-kuksa "${META_KUKSA_PATH}")

  # Added meta-virtualization layer for docker
  set(METADIRVIRT "$")
  set(METADIRVIRT "${METADIRVIRT}{METADIR}")
  set(METADIRVIRT "${METADIRVIRT}/meta-virtualization")
  config_layer(meta-virtualization "${METADIRVIRT}")

  if (DEV_LAYERS)
      message("-- Development mode ON adding meta-kuksa-dev")
      config_layer(meta-kuksa-dev "${META_KUKSA_DEV_PATH}")
  endif()

  message("-- Creating SDK/Image Building Script")

  # Add distribution
  set(POKY_DISTRO "kuksa")

  # For agl-kuksa target
  configure_file("${CMAKE_SOURCE_DIR}/tools/agl-build.sh.configure"
    "${AGL_BUILD_TMP_PATH}/agl-kuksa-build.sh"
    @ONLY)
  configure_file("${CMAKE_SOURCE_DIR}/tools/agl-buildsdk.sh.configure"
    "${AGL_BUILD_TMP_PATH}/agl-kuksa-buildsdk.sh"
    @ONLY)
  
  configure_file("${CMAKE_SOURCE_DIR}/tools/agl-configure.sh.configure"
    "${AGL_BUILD_TMP_PATH}/agl-kuksa-configure.sh"
    @ONLY)

endmacro(agl_build_configure)

# Source for creating the
macro(agl_build)

  message("-- Running Building Script")
  # Build AGL target
  execute_process(
    COMMAND bash "${AGL_BUILD_TMP_PATH}/agl-image-build.sh"
    WORKING_DIRECTORY "${AGL_ROOT}")

  message("-- ${AGL_ROOT}")

endmacro(agl_build)

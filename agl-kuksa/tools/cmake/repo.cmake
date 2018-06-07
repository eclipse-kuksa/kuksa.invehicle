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


function(download_repo)

  if(EXISTS "${CMAKE_BINARY_DIR}/bin/repo")
    message("-- Repo command already installed")
  else()
    message("-- Downloading repo command")
    file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/bin/")

    execute_process(COMMAND curl
      https://storage.googleapis.com/git-repo-downloads/repo
      OUTPUT_FILE "${CMAKE_BINARY_DIR}/bin/repo")
    execute_process(COMMAND chmod u+x "${CMAKE_BINARY_DIR}/bin/repo")
  endif()

  # Set the repo command environment variable
  set(REPO "${CMAKE_BINARY_DIR}/bin/repo" PARENT_SCOPE)

endfunction(download_repo)

# TODO: Create repo function to replace variable

# ******************************************************************************
# Copyright (c) 2018 Robert Bosch GmbH and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/index.php
#
#  Contributors:
#      Robert Bosch GmbH - append runc-docker recipe for no-pie and hard-float
# *****************************************************************************

do_compile_prepend() {
	export EXTRA_LDFLAGS="-extldflags '-no-pie -mfloat-abi=hard'"
}

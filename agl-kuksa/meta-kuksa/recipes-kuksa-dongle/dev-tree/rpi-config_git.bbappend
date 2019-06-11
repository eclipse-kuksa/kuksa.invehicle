# ******************************************************************************
# Copyright (c) 2019 Robert Bosch GmbH and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# https://www.eclipse.org/org/documents/epl-2.0/index.php
#
#  Contributors:
#      Robert Bosch GmbH - kuksa dongle API and functionality
# *****************************************************************************

do_deploy_append() {
    echo "dtoverlay=gpio-poweroff,gpiopin=10,active_low=1" >> ${DEPLOYDIR}/bcm2835-bootfiles/config.txt
    echo "dtoverlay=gpio-poweroff,gpiopin=11,active_low=1" >> ${DEPLOYDIR}/bcm2835-bootfiles/config.txt
    echo "dtoverlay=gpio-poweroff,gpiopin=12,active_low=1" >> ${DEPLOYDIR}/bcm2835-bootfiles/config.txt
}


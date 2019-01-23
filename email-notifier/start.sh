#!/bin/sh
#
# Copyright (c) 2018 Robert Bosch GmbH and others.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# http://www.eclipse.org/legal/epl-2.0
#
# SPDX-License-Identifier: EPL-2.0
# Forever checker for people so poor that they do not even have cron
#
# Contributors: Robert Bosch GmbH

echo " Starting DTC E-mail notifier app"

EMAIL_SERVER='1.1.1.1' # enter Email server IP here
PORT='8080'
TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFeGFtcGxlIEpXVCIsImlzcyI6IkVjbGlwc2Uga3Vrc2EiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2MDkzNzI4MDB9.lxYf-N0C66NgJiinrY_pgVpZOxgH0ppnbMsdKfNiQjbMqYTY_nEpXufmjquvBaxiYsRb_3ScXA__gmviWj_PQoU3apuMVxJjAY6xrwaXFw7g-daUi21yqLSfLptH2vqQzhA_Y1LU6u7SjeiEcGRZrgq_bHnjMM61EVDSnKGCClo'


./email-notifier $EMAIL_SERVER $PORT $TOKEN

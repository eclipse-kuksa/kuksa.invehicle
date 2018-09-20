#!/bin/bash
echo " Starting vehicle2cloud app"

HONOIP='11.11.11.111' # enter HONO-HTTP-Adapter IP here
HONOPORT='8080'
HONODEVICE='sensor1'
HONOPW='hono-secret'
TOKEN='eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJFeGFtcGxlIEpXVCIsImlzcyI6IkVjbGlwc2Uga3Vrc2EiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2MDkzNzI4MDB9.lxYf-N0C66NgJiinrY_pgVpZOxgH0ppnbMsdKfNiQjbMqYTY_nEpXufmjquvBaxiYsRb_3ScXA__gmviWj_PQoU3apuMVxJjAY6xrwaXFw7g-daUi21yqLSfLptH2vqQzhA_Y1LU6u7SjeiEcGRZrgq_bHnjMM61EVDSnKGCClo'


./vehicle2cloud $HONOIP $HONOPORT $HONOPW $HONODEVICE $TOKEN

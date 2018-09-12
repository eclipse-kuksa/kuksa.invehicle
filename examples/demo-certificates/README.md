# Demo-Certificates

This folder conatins the demo ssl certificates which are self-signed usning the CA.key file.
The jwt.pub.key holds the public key for deciphering the JWT token found in the example_token.txt. This token has been used by the vehicle2cloud app and the elm327-visdatafeeder app to authenticate with the w3c-visserver-api. The tokens are added in the start.sh file of respective apps.

This token can be viewed using the [JWT Debugger](https://jwt.io/) by copying and pasting it.

# Kuksa Hawkbit

Kuksa's hawkbit downloader. Can query hawkbit and download new artifacts.

Current version is quite stupid: Will download everything it finds in deployment, and we do not have an installer yet, so we can not give any meaningful feedback to Hawkbit yet 

## Requirements

``sudo pip3 install requests``

## Running on AGL-Kuksa image

AGL-Kuksa image includes this app under `/usr/bin/kuksa-hawkbit`. This app is only installed on the image and is not deployed as a service. To start the kuksa-hawkbit dowloader and allow it to check for updates you need to configure the IP-Address of Hawkbit server in the `/usr/bin/kuksa-hawkbit/config.ini` file. Once the hawkbit server is configured, you could start by running `./usr/bin/kuksa-hawkbit/tools/foreverChecker.sh`.

This app will check for the new apps assigned to the device using kuksa-appstore and dowloads and installs the apps.

# Development guide

## Requirements

Python 3.5+ is required and Virtualenvwrapper is highly recommended.

### Virtualenvwrapper installation

Install virtualenvwrapper

    $ pip install virtualenvwrapper
    $ mkdir ~/.virtualenvs
    
Add the following lines to the end of ~/.bashrc

    export WORKON_HOME=~/.virtualenvs
    source `which virtualenvwrapper.sh`
    
Reload bash configuration

    $ source ~/.bashrc

### Project setup

Go to where the project was cloned

    $ cd kuksa-appmanager

Create virtualenv

    $ mkvirtualenv -p `which python3` `basename $PWD`
    (kuksa-appmanager) $ echo $PWD > $VIRTUAL_ENV/.project

Install dependencies

    (kuksa-appmanager) $ pip install -r requirements.txt

## Environment variables

- `HAWKBIT_SERVER` - hawkbit server url (http://...)
- `HAWKBIT_TENANT` - given hawkbit tenant
- `HAWKBIT_DEVICE` - unique for each device
- `HAWKBIT_TOKEN`  - securitytoken for the device

Optional settings: (When it is set hono server will be connected)
- `HONO_SERVER`    - hono host:port for service hono-adapter-mqtt-vertx
- `HONO_USERNAME`  - given username@tenant for registered device
- `HONO_PASSWORD`  - given password for registered device

You can add them to the virtualenv's `activate` script at `~/.virtualenv/kuksa-appmanager/bin/activate`

## Launching the client

    $ python -m kuksa.appmanager

## Notes: 
* python should be > v3.5. If you have mutliple versions installed, make sure you use the correct one e.g. `python3.5 -m kuksa.appmanager`.
* the security token can be generated from hawkbit via `system config -> Allow a gateway to authenticate and manage multiple targets through a gateway security token`
* if you encounter messages like `ERROR - kuksa.appmanager.hawkbit.DeploymentJob - ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))` you may want to check that docker is correcltly installed on your target via, e.g., `docker ps`

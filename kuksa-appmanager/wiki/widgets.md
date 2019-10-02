# AGL Widgets

The AppManager can install AGL widgets which must be supplied in the form of `*.wgt` files.
It uses the `afm-util` program to install and uninstall the widgets.

## App registry

The AppManager keeps a registry of the installed widgets.
It is needed to be able to uninstall the widgets later.

The registry is stored in the JSON file `/var/lib/kuksa-appmanager/appregistry.json`

Example registry JSON:

```json
[
  {
    "id": "appstacle-demo@0.1",
    "installdate": "2019-10-02T13:44:48.235213",
    "type": "widget"
  },
  {
    "id": "other-app@0.2",
    "installdate": "2019-10-02T13:44:49.970568",
    "type": "widget"
  }
]
```


## App launcher

If new widgets are installed (or existing widgets deleted), the AGL app launcher will not show the new widgets automatically.
To update the app launcher it has to be restarted.
This can be done by simply rebooting the device or by restarting the launcher:

```
# afm-util kill launcher@0.1
# afm-util run launcher@0.1
```


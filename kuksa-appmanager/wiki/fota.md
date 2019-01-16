# FOTA

The AppManager provides basic FOTA support, where the firmware files are downloaded, while the flashing itself is left to the OS provider via a set of tools.

Currently AppManager supports only the best case scenario, where a flashing is always successful. A failed flash will be retried indefinitely.

# FOTA steps

1. AppManager downloads all firmware artifacts for the firmwares directory
2. For each firmware (software module) AppManager calls `kuksa-firmware-get-version $firmware_name` to check if it was already installed
3. For each not yet installed firmware Appmanager calls `kuksa-firmware-flash` with the firmware details provided as JSON via `stdin`

# kuksa-firmware-get-version

This tool is expected to write the installed version of the specified firmware (via the first argument) to `stdout`

# kuksa-firmware-flash

The flashing tool is responsible for preparing and executing the actual firmware update which can optionally also reboot the system.

### Firmware JSON example (indented for readability reasons)

```json
{
  "name": "rover-firmware",
  "version": "1.0.0",
  "files": [
    {
      "name":  "system.zip",
      "path":  ".../firmwares/system.zip"
    },
    {
      "name":  "controllerX.zip",
      "path":  ".../firmwares/controllerX.zip"
    }
  ]
}
```

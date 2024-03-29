# nRF5340DK
* https://www.nordicsemi.com/Products/Development-hardware/nRF5340-DK

## Documents
* SDK: https://developer.nordicsemi.com/nRF_Connect_SDK/doc/2.0.0/nrf/index.html
* Flashing: https://developer.nordicsemi.com/nRF_Connect_SDK/doc/2.0.0/zephyr/develop/flash_debug/nordic_segger.html

## Zephyr OS
* https://docs.zephyrproject.org/
* https://docs.zephyrproject.org/2.6.0/boards/arm/nrf5340dk_nrf5340/doc/index.html

## Installation (2022/06, v2.0.0)
1. Install: https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Connect-for-desktop
1. Setup python3 virtualenv (do-oh!)
1. Use manual install process (since desktop app doesn't work): https://developer.nordicsemi.com/nRF_Connect_SDK/doc/2.0.0/nrf/gs_installing.html
1. Install commmand-line utils: https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools
1. Install Segger J-Link: https://developer.nordicsemi.com/nRF_Connect_SDK/doc/2.0.0/zephyr/develop/flash_debug/nordic_segger.html

## Application and add-ons
<img src="nrf-connect-app.png" style="width: 50%; height: %50">

## Building sample 'multicore'
Uses  `nrf5340dk_nrf5340_cpuapp` (application core, app) and `nrf5340dk_nrf5340_cpunet` (network core, net)

Compile and flash:

```bash
source <python env>/bin/activate
cd $SDK_HOME/ncs/nrf/samples/nrf5340/multicore

# multicore target (app + net), use '--sysbuild' for build all cores, use pristine to build every time from scratch:
west build --pristine -b nrf5340dk_nrf5340_cpuapp --sysbuild

# then erase and flash all cores (app+net)
west flash --erase

# do flash only app core of multicore app, use
# west flash --domain hello_world
```

Open terminal outputs - one for app (ttyACM2) and one for net (ttyACM0):
```bash
screen /dev/ttyACM0 
screen /dev/ttyACM2
```

Press 'RESET'-button from motherboard and observe terminals

```
...
*** Booting Zephyr OS build v3.0.99-ncs1 ***
Hello world from nrf5340dk_nrf5340_cpunet
...
...
*** Booting Zephyr OS build v3.0.99-ncs1 ***
Hello world from nrf5340dk_nrf5340_cpuapp
...
```

## Building using custom combos (menu selections)
```bash
west build -b nrf5340dk_nrf5340_cpuapp -t menuconfig

## opens TUI to configure application -> select/remove components into build
```

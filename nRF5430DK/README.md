# nRF5430DK
* https://www.nordicsemi.com/Products/Development-hardware/nRF5340-DK

## Documents
* https://developer.nordicsemi.com/nRF_Connect_SDK/doc/2.0.0/nrf/index.html

## Zephyr OS
* https://docs.zephyrproject.org/
* https://docs.zephyrproject.org/2.6.0/boards/arm/nrf5340dk_nrf5340/doc/index.html

## Installation (2022/06, v2.0.0)
1. Install: https://www.nordicsemi.com/Software-and-Tools/Development-Tools/nRF-Connect-for-desktop
1. Setup python3 virtualenv (do-oh!)
1. Use manual install process (since desktop app doesn't work): https://developer.nordicsemi.com/nRF_Connect_SDK/doc/2.0.0/nrf/gs_installing.html
1. Install commmand-line utils: https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools

## Building sample 'multicore'
Uses  `nrf5340dk_nrf5340_cpuapp` (application core, app) and `nrf5340dk_nrf5340_cpunet` (network core, net)

Compile and flash:

```bash
source <python env>/bin/activate
cd $SDK_HOME/ncs/nrf/samples/nrf5430/multicore

# multicore target (app + net)
west build -b nrf5340dk_nrf5340_cpuapp
west flash --erase
```

Open terminal outputs - one for app and one for net:
```bash
# net
screen /dev/ttyACM0
# app
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
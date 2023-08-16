# Tamarin cable adventures
https://github.com/stacksmashing/tamarin-firmware

## Build (macOS)
How to build TAMARIN CABLE firmware from scratch (read recommendation: https://github.com/bgni/minimal-pico-tinyusb-pio-project)

```
git clone https://github.com/stacksmashing/tamarin-firmware
cd tamarin-firmware
git submodule add https://github.com/hathach/tinyusb
git submodule add https://github.com/raspberrypi/pico-sdk
cd pico-sdk
# Please build with the Pico-SDK Version 4fe995d0ec984833a7ea9c33bac5c67a53c04178
git checkout 4fe995d0ec984833a7ea9c33bac5c67a53c04178
git submodule update --init
cd ..
mkdir build
cd build
export PICO_SDK_PATH=../pico-sdk; cmake ..
make

# install into RPi PICO
cp tamarin_firmware.uf2 /Volumes/RPI-RP2
```

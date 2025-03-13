# Raspberry pico


## Using serprog
Building

```
git clone https://github.com/stacksmashing/pico-serprog
cd pico-serprog
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

# reboot pico with reset pressed and install into pico
cp pico_serprog.uf2 /Volumes/RPI-RP2
```

## Using pico-uart (serial)
Building

```
git clone https://github.com/Noltari/pico-uart-bridge
cd pico-uart-bridge
bash ./build.sh

# reboot pico with reset pressed and install into pico
cp build/uart_bridge.uf2 /Volumes/RPI-RP2
```

# Micro:Bit

## version 1.x
Older model: https://microbit.org/get-started/user-guide/overview/

## btlejack (works with HW 1.x and 2.x, tested 2024/03)
https://github.com/virtualabs/btlejack

1. `pip install btlejack`
1. connect all microbits (3x) to USBv2 (at least with Ubuntu USBv3 some connection issues)
1. `btlejack -i` -> install latest firmware
1. start capturing: `btlejack -d /dev/ttyACM0 -d /dev/ttyACM1 -d /dev/ttyACM2 -c any` 

## version 2.x
Newer model: https://microbit.org/get-started/user-guide/overview/

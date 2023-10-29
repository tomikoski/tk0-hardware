# Bluetooth
Bluetooth / Bluetooth Low Energy hacking

## Demos
* https://github.com/Charmve/BLE-Security-Attack-Defence

## macOS/iOS (packetlogger)
* https://www.bluetooth.com/blog/a-new-way-to-debug-iosbluetooth-applications/
* https://developer.apple.com/bug-reporting/profiles-and-logs/?name=bluetooth

## BT5.0 for Debian12

### Install
`dmesg|grep Bluetooth` shows errors, then: https://linuxreviews.org/Realtek_RTL8761B.

### Testing

```
# list devices
$ hcitool dev
Devices:
	hci1	77:88:99:AA:BB:CC (<-- external)
	hci0	11:22:33:44:55:66 (<-- built-in)

#disable built-in adapter hci0
$ sudo hcitool hci0 down

# shows only one device, external BT5
$ hcitool dev
Devices:
	hci1	77:88:99:AA:BB:CC

$ bluetoothctl
scan on
(...at this point, should be scanning using new BT5 adapter...)
```

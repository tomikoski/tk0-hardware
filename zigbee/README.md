# Zigbee
Various Zigbee stuff

## CC2531 Dongle (sniffer)
* https://www.zigbee2mqtt.io/guide/adapters/flashing/alternative_flashing_methods.html
* https://lemariva.com/blog/2019/08/zigbee-flashing-cc2531-using-raspberry-pi-without-cc-debugger

### Process
* Raspberry PI 4
* Setup wiring
* Flash PACKET-SNIFFER (from TI)

### Wiring
* ref: https://lemariva.com/blog/2019/08/zigbee-flashing-cc2531-using-raspberry-pi-without-cc-debugger
![wiring.png](images/wiring.png)

### Public Zigbee Allience 09 network key
```
5A:69:67:42:65:65:41:6C:6C:69:61:6E:63:65:30:39
```
Configure in wireshark/sniffers to dump Network Key info etc.

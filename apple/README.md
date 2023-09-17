# Apple Stuff

## AirTag

![AirTag research](https://raw.githubusercontent.com/colinoflynn/airtag-re/master/images/frontside-tpnames.jpg)
![Segger pinout](https://c.a.segger.com/fileadmin/images/products/J-Link/Software/pinout-spi-20-pin.gif.webp)

## Wiring
|AirTag|Segger|
|---|---|
|Flash VCC (TP21)|1.8V (Tigard VGT/Powersupply +)|
|Flash SCLK (TP22)|pin 9 (CLK)|
|Flash CS (TP23)|pin 7 (nCS)|
|Flash DI (TP19)|pin 5 (DI)|
|Flash DO (TP20)|pin 13 (DO)|

## Segger JLinkSPI

```
$ JFlashSPI_CL -connect

SEGGER J-Flash SPI V7.92e Command Line Version
JLinkARM.dll V7.92e (DLL compiled Sep 13 2023 15:44:25)

Creating new project file [Default.jflash] ...
Connecting to probe/ programmer...
- Connecting via USB to probe/ programmer device 0
Executing init sequence...
Connecting to SPI Flash...
- VTarget = 1.780V
- Read SPI Flash Id = 0xC8 60 16
- Found SPI Flash: GigaDevice GD25LQ32C
Disconnecting ...
Close project
```

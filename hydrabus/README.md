# Hydrabus (non-NFC)
Contains modified version of Hydrabus SPI script: https://github.com/hydrabus/hydrafw/blob/master/contrib/hydra_spi_dump/hydra_spi_dump.py

## Dumping
Tested with `MX25L1606E` with following dump techniques:

```
# flashrom
flashrom -p serprog:dev=/dev/tty.usbmodem2101 -r dump_flashrom.bin -c "MX25L1605A/MX25L1606E/MX25L1608E"

# hydra_spi_dump.py
python hydra_spi_dump.py dump dump_spi.bin 512 0x0 fast

$ md5sum *.bin
8fc3a35a66a55952bfb684f4cfa8ade2  dump_flashrom.bin
8fc3a35a66a55952bfb684f4cfa8ade2  dump_spi.bin
```

## Dragons ahead!
Make at least 2x dumps per try! Sometimes first SPI dump will fail and I cannot figure out why the hell this just happens. Just retry and observe md5sum to match. 

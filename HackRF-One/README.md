# HackRF One

## Monitor 433.920 (Weather stations, TPMS, etc.)
```
rtl_433 -d 'device=hackrf' -g LNA=40,AMP=14,VGA=30 -s 250k
```

Sample output:
```
...
time      : 2024-03-24 13:31:49
Model     : Markisol     id        : 0204
Control   : ? (8)        Channel   : 0             Zone      : 1             Integrity : CHECKSUM
...
```

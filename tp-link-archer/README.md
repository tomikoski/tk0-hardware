# TP-Link Archer T4U v2 [Realtek RTL8812AU]
Tested with Ubuntu 22.04

## compile drivers for linux
Choose suitable driver from this repo - here we use:

```
git clone https://github.com/lwfinger/rtl8812au
cd rtl8812au
make
sudo insmod 8812au.ko

# should show correct info
lsusb

# should show new interface
rfkill list

# sanity check
sudo depmod 
```


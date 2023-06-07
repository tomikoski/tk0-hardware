# TP-Link Archer T4U v2 [Realtek RTL8812AU]
Tested with Ubuntu 22.04

## compile drivers for linux

```
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
make
sudo insmod 8812au.ko

# should show correct info
lsusb

# should show new interface
rfkill list

# sanity check
sudo depmod 

# if works, we can install it:
sudo make dkms_install
```


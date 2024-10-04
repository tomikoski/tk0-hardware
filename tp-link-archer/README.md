# TP-Link Archer T4U v2 [Realtek RTL8812AU]
* Tested with Ubuntu 22.04
* Tested with Debian 12 (bookworm) - [see this git issue](https://github.com/aircrack-ng/rtl8812au/issues/1157)



## Ubuntu 22.04
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

## Debian 12 (bookworm)
```
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au

# important part for working version!!!
git checkout 63cf0b4

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

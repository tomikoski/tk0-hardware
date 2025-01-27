# QEMU tricks
Random stuff related to QEMU emulation.


## MIPS32 (MIPS-I aka "Malta")
Before starting, change `dist` and `vmlinuz-VERSION-4kc-malta` accordingly. During writeup:
```
# install QEMU
sudo apt install qemu-system-mips

# get images (bookworm)
wget http://ftp.debian.org/debian/dists/bookworm/main/installer-mipsel/current/images/malta/netboot/initrd.gz
wget http://ftp.debian.org/debian/dists/bookworm/main/installer-mipsel/current/images/malta/netboot/vmlinuz-6.1.0-29-4kc-malta

# create disk
qemu-img create -f qcow2 hda.img 2G

# emulate
qemu-system-mips -M malta \
  -m 256 -hda hda.img \
  -kernel vmlinuz-6.1.0-29-4kc-malta \
  -initrd initrd.gz \
  -append "console=ttyS0 nokaslr" \
  -nographic
```

## Useful links
* https://markuta.com/how-to-build-a-mips-qemu-image-on-debian/

# Setup chipwhisperer repos etc.
Setup battletested with Debian12, ackward reboots ahead.

## env
```
sudo apt update && sudo apt upgrade

# python prereqs
sudo apt-get install build-essential gdb lcov pkg-config \
    libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev \
    libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev \
    lzma lzma-dev tk-dev uuid-dev zlib1g-dev curl

sudo apt install libusb-dev make git avr-libc gcc-avr \
    gcc-arm-none-eabi libusb-1.0-0-dev usbutils

python3 -m venv ~/pythons/chipwhisperer
source ~/pythons/chipwhisperer/bin/activate

cd ~/git
git clone https://github.com/newaetech/chipwhisperer
cd chipwhisperer
sudo cp hardware/50-newae.rules /etc/udev/rules.d/50-newae.rules
sudo udevadm control --reload-rules
sudo groupadd -f chipwhisperer
sudo usermod -aG chipwhisperer $USER
sudo usermod -aG plugdev $USER

####################################
# reboot - yes really
####################################

cd ~/git/chipwhisperer
git submodule update --init jupyter

pip install -e .
pip install -r jupyter/requirements.txt
cd jupyter
pip install nbstripout
nbstripout --install

# fix jupyter \o/
pip uninstall traitlets
pip install traitlets==5.9.0
```

## run jupyter notebooks
```
jupyter notebook
```

## build firmwares
```
cd $GITROOT/hardware/victims/firmware/simpleserial-base/
make PLATFORM=CWNANO CRYPTO_TARGET=NONE # SimpleSerial
make PLATFORM=CWNANO CRYPTO_TARGET=NONE S_VER=SS_VER_2_1 # SimpleSerial2
```

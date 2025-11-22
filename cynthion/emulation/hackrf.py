from facedancer import *
from facedancer import main

@use_inner_classes_automatically
class HackRF(USBDevice):
    product_string       : str = "HackRF One (Emulated)"
    manufacturer_string  : str = "Facedancer"
    serial_number_string : str = "1234"
    vendor_id            : int = 0x1d50
    product_id           : int = 0x6089

    class DefaultConfiguration(USBConfiguration):
        class DefaultInterface(USBInterface):
            pass

main(HackRF)

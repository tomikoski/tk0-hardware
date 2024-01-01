import chipwhisperer as cw
import chipwhisperer.common.results.glitch as glitch
import struct
import time
import warnings
from datetime import datetime
import sys

SCOPETYPE = 'CWNANO'
PLATFORM = 'CWNANO'
SS_VER = 'SS_VER_2_1'
print(SS_VER)

try:
    if not scope.connectStatus:
        scope.con()
except NameError:
    scope = cw.scope()

try:
    if SS_VER == "SS_VER_2_1":
        target_type = cw.targets.SimpleSerial2
    elif SS_VER == "SS_VER_2_0":
        raise OSError("SS_VER_2_0 is deprecated. Use SS_VER_2_1")
    else:
        target_type = cw.targets.SimpleSerial
except:
    SS_VER="SS_VER_1_1"
    target_type = cw.targets.SimpleSerial

try:
    target = cw.target(scope, target_type)
except:
    print("INFO: Caught exception on reconnecting to target - attempting to reconnect to scope first.")
    print("INFO: This is a work-around when USB has died without Python knowing. Ignore errors above this line.")
    scope = cw.scope()
    target = cw.target(scope, target_type)

print("INFO: Found ChipWhisperer😍")

time.sleep(0.05)
scope.default_setup()
scope.io.clkout = 7.5E6
def reboot_flush():            
    scope.io.nrst = False
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()


reboot_flush()

print(scope)
print("baud = {}".format(target.baud))

print("Sanity check:")
reboot_flush()
pw = bytearray([0x74, 0x6F, 0x75, 0x63, 0x68])
target.simpleserial_write('p', pw)

val = target.simpleserial_read_witherrors('r', 1, glitch_timeout=10) #For loop check
valid = val['valid']
if valid:
    response = val['payload']
    raw_serial = val['full_response']
    error_code = val['rv']

print(val)

reboot_flush()

# should glitch <100 tries, YMMV
scope.glitch.repeat = 5
scope.glitch.ext_offset = 11
broken = False
count = 0

while broken is False:
    count += 1
    if(count % 100) == 1:
      print(count)
    scope.arm()
    target.simpleserial_write('p', bytearray([0]*5))
    ret = scope.capture()
    
    if ret:
        print('Timeout - no trigger')
        #Device is slow to boot?
        reboot_flush()

    else:
        val = target.simpleserial_read_witherrors('r', 1, glitch_timeout=10)#For loop check
        if val['valid'] is False:
            print("reset")
            reboot_flush()
        else:
            if val['payload'] == bytearray([1]): #for loop check
                broken = True
                print("success at {}".format(count))
                print(val)
                print(val['payload'])
                print(scope.glitch.repeat, scope.glitch.ext_offset)
                print("🐙", end="")
                break
            else:
                pass

# cleanup
scope.dis()
target.dis()                   


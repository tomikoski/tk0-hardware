import chipwhisperer as cw
from importlib import reload
import chipwhisperer.common.results.glitch as glitch
from tqdm.notebook import trange
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

#if "STM" in PLATFORM or PLATFORM == "CWLITEARM" or PLATFORM == "CWNANO":
#    prog = cw.programmers.STM32FProgrammer
#prog = cw.programmers.STM32FProgrammer
# program device
#fw_path = sys.argv[1]
#cw.program_target(scope, prog, fw_path)

time.sleep(0.05)
scope.default_setup()

scope.io.clkout = 7.5E6
def reboot_flush():            
    scope.io.nrst = False
    #scope.io.nrst = "low" # “low” / False: logic 0
    time.sleep(0.05)
    scope.io.nrst = True
    #scope.io.nrst = "high_z" # “high” / True: logic 1
    time.sleep(0.05)
    #Flush garbage too
    target.flush()

cw.set_all_log_levels(cw.logging.CRITICAL)


#Do glitch loop
reboot_flush()

for e in range(0,122):
  for r in range(1,2):
    scope.glitch.repeat = r
    scope.glitch.ext_offset = e
    scope.arm()
    target.write('h' + '0'*4) 
    ret = scope.capture()

    if ret:
      print("timeout")
      reboot_flush()
 
    val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10)
    if val['valid'] is False:
       response = val['payload']
       raw_serial = val['full_response']
       error_code = val['rv']
    else:
       if val['rv'] == 1:
         print(val['payload'])
         break
     
    print(val)

scope.dis()
target.dis()
cw.set_all_log_levels(cw.logging.WARNING)


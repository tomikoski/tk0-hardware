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
#SS_VER = 'SS_VER_2_1'
#SS_VER = 'SS_VER_1_1'

if(len(sys.argv) < 2):
    print("No param")
    sys.exit(1)
else:
    SS_VER = sys.argv[1]
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
    #scope.io.nrst = "low" # “low” / False: logic 0
    time.sleep(0.05)
    scope.io.nrst = True
    #scope.io.nrst = "high_z" # “high” / True: logic 1
    time.sleep(0.05)
    #Flush garbage too
    target.flush()

cw.set_all_log_levels(cw.logging.CRITICAL)


gc = cw.GlitchController(groups=["success", "reset", "normal"], parameters=["repeat", "ext_offset"])
#gc.display_stats()
gc.glitch_plot(plotdots={"success":"+g", "reset":"xr", "normal":None})


gc.set_global_step(1)
#gc.set_range("repeat", 1, 10)
#gc.set_range("ext_offset", 0, 500)
gc.set_range("repeat", 0, 2)
gc.set_range("ext_offset", 120, 125)
scope.glitch.repeat = 0

print(scope)
print("baud: {}\n\n".format(target.baud))

reboot_flush()

start_time = datetime.now().strftime("%H:%M:%S")

for glitch_setting in gc.glitch_values():
   scope.glitch.repeat = glitch_setting[0]
   scope.glitch.ext_offset = glitch_setting[1]
   successes = 0
   resets = 0   

   for i in range(3):
       target.flush()
       scope.arm()
       #Do glitch loop
       #target.simpleserial_write("h", bytearray([0]*4))
       #target.simpleserial_write("h", bytearray([0]*8))
       #target.simpleserial_write("h", bytearray([0]*16))
       #target.write("h0000\n")
       target.simpleserial_write("h", bytearray([])) # tulee tuloksia       
       ret = scope.capture()
       val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10)
       #print(val)
           
       if ret:
           print('Timeout - no trigger')
           gc.add("reset")
           resets += 1
   
           #Device is slow to boot?
           reboot_flush()
   
       else:
           if val['valid'] is False:
               reboot_flush()
               gc.add("reset")
               resets += 1
           else:
               gcnt = struct.unpack("<I", val['payload'])[0]
               if gcnt != 3221785859:
                   print(gcnt)
                   gc.add("success")
                   #print("resp: {}".format(val['full_response']))
                   print("val: {}".format(val))
                   successes += 1
               else:
                   gc.add("normal")
   if successes > 0:                
        print("successes = {}, resets = {}, repeat = {}, ext_offset = {}".format(successes, resets, scope.glitch.repeat, scope.glitch.ext_offset))
        break

end_time = datetime.now().strftime("%H:%M:%S")
print("Done glitching, start: {}, end: {}".format(start_time,end_time))
print("successes = {}, resets = {}".format(successes, resets))

scope.dis()
target.dis()
cw.set_all_log_levels(cw.logging.WARNING)


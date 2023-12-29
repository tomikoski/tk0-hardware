import chipwhisperer as cw
import matplotlib.pylab as plt
import chipwhisperer.common.results.glitch as glitch
import struct
import time
import warnings
from datetime import datetime
import sys

SCOPETYPE = 'CWNANO'
PLATFORM = 'CWNANO'
#SS_VER = 'SS_VER_2_1'

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
    if(SS_VER == "SS_VER_2_1"):
       print("reset target")
       #target.resetcomms() #???

except:
    print("INFO: Caught exception on reconnecting to target - attempting to reconnect to scope first.")
    print("INFO: This is a work-around when USB has died without Python knowing. Ignore errors above this line.")
    scope = cw.scope()
    target = cw.target(scope, target_type)

print("INFO: Found ChipWhisperer😍")

time.sleep(0.05)
scope.default_setup()

if SS_VER == "SS_VER_1_1":
    target.baud = 38400*7.5/7.37

scope.io.clkout = 7.5E6
def reboot_flush():            
    scope.io.nrst = False
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()

gc = cw.GlitchController(groups=["success", "reset", "normal"], parameters=["repeat", "ext_offset"])
#gc.display_stats()
gc.glitch_plot(plotdots={"success":"+g", "reset":"xr", "normal":None})


cw.set_all_log_levels(cw.logging.CRITICAL)

###ORIG
#gc.set_global_step(1)
#gc.set_range("repeat", 1, 7)
#gc.set_range("ext_offset", 1, 200)
#scope.glitch.repeat = 0
###

###FULL SCALE
gc.set_global_step(1)
gc.set_range("repeat", 1, 10)
gc.set_range("ext_offset", 0, 500)
scope.glitch.repeat = 0
###

print(scope)
print("baud = {}".format(target.baud))

reboot_flush()

start_time = datetime.now().strftime("%H:%M:%S")

for glitch_setting in gc.glitch_values():
   scope.glitch.repeat = glitch_setting[0]
   scope.glitch.ext_offset = glitch_setting[1]
   successes = 0
   resets = 0
   #print("ext_offset = {:.3f}; repeat = {:.3f};".format(scope.glitch.ext_offset,scope.glitch.repeat))

   for i in range(5):
       target.flush()
       scope.arm()
       #Do glitch loop
       #target.simpleserial_write("g", bytearray([]))
       target.write("g\n")
       ret = scope.capture()
       val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10) #For loop check
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
               if gcnt != 2500: #for loop check
                   gc.add("success")
                   print(gcnt)
                   print("val: {}".format(val))
                   successes += 1
               else:
                   gc.add("normal")
   if successes > 0:                
        print("successes = {}, resets = {}, repeat = {}, ext_offset = {}".format(successes, resets, scope.glitch.repeat, scope.glitch.ext_offset))

end_time = datetime.now().strftime("%H:%M:%S")
print("Done glitching, start: {}, end: {}".format(start_time,end_time))
print("successes = {}, resets = {}".format(successes, resets))

scope.dis()
target.dis()
cw.set_all_log_levels(cw.logging.WARNING)

import chipwhisperer as cw
from importlib import reload
import chipwhisperer.common.results.glitch as glitch
from tqdm.notebook import trange
import struct
import time
import warnings
from datetime import datetime

SCOPETYPE = 'CWNANO'
PLATFORM = 'CWNANO'
SS_VER = 'SS_VER_2_1'


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
prog = cw.programmers.STM32FProgrammer

time.sleep(0.05)
scope.default_setup()

# program device
#fw_path = sys.argv[1]
#cw.program_target(scope, prog, fw_path)

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


g_step = 1
gc = cw.GlitchController(groups=["success", "reset", "normal"], parameters=["repeat", "ext_offset"])
#gc.display_stats()
gc.glitch_plot(plotdots={"success":"+g", "reset":"xr", "normal":None})
gc.set_global_step(g_step)
#ORIG
gc.set_range("repeat", 1, 10)
gc.set_range("ext_offset", 1, 500)
#gc.set_range("repeat", 1, 3)
#gc.set_range("ext_offset", 294, 309)
scope.glitch.repeat = 0

print(scope)
   
reboot_flush()
sample_size = 1

#print("glitching the following:")
#count=0
#for glitch_setting in gc.glitch_values():
#   print("count {}, offset: {:4.1f}; width: {:4.1f}".format(count, glitch_setting[1], glitch_setting[0]))
#   count+=1

all_successes = ""
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
       target.simpleserial_write("g", bytearray([]))
       ret = scope.capture()
       val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10)#For loop check
       print(val)
           
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
        all_successes += "successes = {}, resets = {}, repeat = {}, ext_offset = {}\n".format(successes, resets, scope.glitch.repeat, scope.glitch.ext_offset)

end_time = datetime.now().strftime("%H:%M:%S")
print("Done glitching, start: {}, end: {}".format(start_time,end_time))
print("successes = {}, resets = {}".format(successes, resets))
if successes > 0:
   print("all_successes = {}".format(all_successes))

scope.dis()
target.dis()
cw.set_all_log_levels(cw.logging.WARNING)


import chipwhisperer as cw
import matplotlib.pylab as plt
from importlib import reload
import chipwhisperer.common.results.glitch as glitch
from tqdm.notebook import trange
import struct
import time
import warnings
from datetime import datetime

SCOPETYPE = 'CWNANO'
PLATFORM = 'CWNANO'
#SS_VER = 'SS_VER_2_1'
SS_VER = 'SS_VER_1_1'


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
print(SS_VER)

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
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()


gc = glitch.GlitchController(groups=["success", "reset", "normal"], parameters=["repeat", "ext_offset"])
#gc.display_stats()
fig = plt.figure()

cw.set_all_log_levels(cw.logging.CRITICAL)

g_step = 1

gc.set_global_step(g_step)
gc.set_range("repeat", 1, 3)
gc.set_range("ext_offset", 1, 50)

gc.set_global_step(1)

reboot_flush()
sample_size = 1
scope.glitch.repeat = 0
broken = False

for glitch_settings in gc.glitch_values():
    scope.glitch.repeat = glitch_settings[0]
    scope.glitch.ext_offset = glitch_settings[1]
    if broken:
        break
    for i in range(50):
        print("ext_offset {}, repeat {}".format(scope.glitch.ext_offset,scope.glitch.repeat))
        scope.arm()
        target.simpleserial_write('p', bytearray([0]*5))
        ret = scope.capture()
        
        if ret:
            print('Timeout - no trigger')
            gc.add("reset")

            #Device is slow to boot?
            reboot_flush()

        else:
            val = target.simpleserial_read_witherrors('r', 1, glitch_timeout=10)#For loop check
            print(val) 
            if val['valid'] is False:
                gc.add("reset")
                reboot_flush()
            else:
                if val['payload'] == bytearray([1]): #for loop check
                    broken = True
                    gc.add("success")
                    print(val)
                    print(val['payload'])
                    print(scope.glitch.repeat, scope.glitch.ext_offset)
                    print("🐙", end="")
                    break
                else:
                    gc.add("normal")
                    
cw.set_all_log_levels(cw.logging.WARNING)                    


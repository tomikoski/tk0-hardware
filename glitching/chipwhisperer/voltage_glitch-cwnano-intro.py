import chipwhisperer as cw
import time
import warnings
from datetime import datetime
import struct
import matplotlib.pylab as plt
import chipwhisperer.common.results.glitch as glitch

SCOPETYPE = 'CWNANO'
PLATFORM = 'CWNANO'
SS_VER = 'SS_VER_2_1'
#SS_VER = 'SS_VER_1_1'


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
target.baud = 38400*7.5/7.37
def reboot_flush():
    scope.io.nrst = False
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()

cw.set_all_log_levels(cw.logging.CRITICAL)
####CODE BLOCK####################################################

import chipwhisperer.common.results.glitch as glitch
gc = glitch.GlitchController(groups=["success", "reset", "normal"], parameters=["repeat", "ext_offset"])
#gc.display_stats()
fig = plt.figure()

from importlib import reload
import chipwhisperer.common.results.glitch as glitch
from tqdm.notebook import trange
import struct

g_step = 1

gc.set_global_step(g_step)
gc.set_range("repeat", 1, 7)
gc.set_range("ext_offset", 1, 200)
scope.glitch.repeat = 0

reboot_flush()
sample_size = 1
for glitch_setting in gc.glitch_values():
    scope.glitch.repeat = glitch_setting[0]
    scope.glitch.ext_offset = glitch_setting[1]
    successes = 0
    resets = 0
    for i in range(5):
        target.flush()

        scope.arm()

        #Do glitch loop
        target.write("g\n")

        ret = scope.capture()

        val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10)#For loop check

        if ret:
            print('Timeout - no trigger')
            gc.add("reset", (scope.glitch.repeat, scope.glitch.ext_offset))
            plt.plot(scope.glitch.ext_offset, scope.glitch.repeat, 'xr', alpha=1)
            fig.canvas.draw()
            resets += 1

            #Device is slow to boot?
            reboot_flush()

        else:
            if val['valid'] is False:
                reboot_flush()
                gc.add("reset", (scope.glitch.repeat, scope.glitch.ext_offset))
                plt.plot(scope.glitch.ext_offset, scope.glitch.repeat, 'xr', alpha=1)
                fig.canvas.draw()
                resets += 1
            else:
                gcnt = struct.unpack("<I", val['payload'])[0]

                if gcnt != 2500: #for loop check
                    gc.add("success", (scope.glitch.repeat, scope.glitch.ext_offset))
                    print(gcnt)
                    plt.plot(scope.glitch.ext_offset, scope.glitch.repeat, '+g', alpha=1)
                    fig.canvas.draw()
                    successes += 1
                else:
                    gc.add("normal", (scope.glitch.repeat, scope.glitch.ext_offset))
    if successes > 0:
        print("successes = {}, resets = {}, repeat = {}, ext_offset = {}".format(successes, resets, scope.glitch.repeat, scope.glitch.ext_offset))
print("Done glitching")


##################################################################
cw.set_all_log_levels(cw.logging.WARNING)
scope.dis()
target.dis()


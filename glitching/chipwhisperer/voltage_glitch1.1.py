import time
import warnings
import chipwhisperer as cw
from importlib import reload
import chipwhisperer.common.results.glitch as glitch
from tqdm.notebook import trange
import struct
import sys

SCOPETYPE = 'OPENADC'
PLATFORM = 'CWNANO'
#SS_VER = 'SS_VER_2_1' #REMOVE DUE SERIAL2 read errors
SS_VER = 'SS_VER_1_1'
MAX_SUCCESSES = 1

def reset_target(scope):
    if PLATFORM == "CW303" or PLATFORM == "CWLITEXMEGA":
        scope.io.pdic = 'low'
        time.sleep(0.1)
        scope.io.pdic = 'high_z' #XMEGA doesn't like pdic driven high
        time.sleep(0.1) #xmega needs more startup time
    elif "neorv32" in PLATFORM.lower():
        raise IOError("Default iCE40 neorv32 build does not have external reset - reprogram device to reset")
    elif PLATFORM == "CW308_SAM4S" or PLATFORM == "CWHUSKY":
        scope.io.nrst = 'low'
        time.sleep(0.25)
        scope.io.nrst = 'high_z'
        time.sleep(0.25)
    else:  
        scope.io.nrst = 'low'
        time.sleep(0.05)
        scope.io.nrst = 'high_z'
        time.sleep(0.05)


# graphics
gc = glitch.GlitchController(groups=["success", "reset", "normal"], parameters=["width", "offset", "ext_offset"])
#gc.display_stats()
#gc.glitch_plot(plotdots={"success":"+g", "reset":"xr", "normal":None})


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

warnings.filterwarnings("ignore")
#disable logging
cw.set_all_log_levels(cw.logging.CRITICAL)

target.baud = 38400
time.sleep(0.1)

def reboot_flush():
#    print(f"IO STATE: {scope.io.pdic}") #get IO state
#    print(f"IO NRST:  {scope.io.nrst}") #get nRST state
    print("Reboot!!")
    scope.io.nrst = False
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()

#PLATFORM="CWNANO"

scope.io.glitch_hp = True
scope.io.glitch_lp = True
scope.glitch.clk_src = "clkgen" # set glitch input clock
scope.glitch.output = "glitch_only" # glitch_out = clk ^ glitch
scope.glitch.trigger_src = "ext_single" # glitch only after scope.arm() called

g_step = 0.4
if PLATFORM=="CWLITEXMEGA":
    gc.set_range("width", 45.7, 47.8)
    gc.set_range("offset", 2.8, 10)
    gc.set_range("ext_offset", 2, 4)
    scope.glitch.repeat = 10
elif PLATFORM == "CWLITEARM":
    #should also work for the bootloader memory dump
    gc.set_range("width", 34.7, 36)
    gc.set_range("offset", -41, -30)
    gc.set_range("ext_offset", 6, 6)
    scope.glitch.repeat = 7
elif PLATFORM == "CW308_STM32F3":
    #these specific settings seem to work well for some reason
    #also works for the bootloader memory dump
    gc.set_range("ext_offset", 9, 12)
    gc.set_range("width", 47.6, 49.6)
    gc.set_range("offset", -19, -21.5)
    scope.glitch.repeat = 5
#TOMI
elif PLATFORM == "CWNANO":
    scope.vglitch_setup(glitcht=None, default_setup=True) # repeat = 1 ext_offset = 0
    gc.set_range("ext_offset", 9, 12)
    gc.set_range("width", 47.6, 49.6)
    gc.set_range("offset", -19, -21.5)
    gc.set_global_step(0.4)
    #gc.set_range("width", 34.7, 36)
    #gc.set_range("offset", -41, -30)
    #gc.set_range("ext_offset", 6, 6)
    #scope.glitch.repeat = 7
   
if(len(sys.argv) > 1):
    print("Override REPEAT...")
    scope.glitch.repeat = int(sys.argv[1])
 
print(f"REPEAT: {scope.glitch.repeat}")
    

scope.adc.timeout = 0.5

reboot_flush()
total_successes = 0
successes = 0
resets = 0
for glitch_setting in gc.glitch_values():
    scope.glitch.offset = glitch_setting[1]
    scope.glitch.width = glitch_setting[0]
    scope.glitch.ext_offset = glitch_setting[2]

    # break out
    total_successes += successes
    successes = 0
    resets = 0
    if total_successes > MAX_SUCCESSES:
       break

    print(f"WIDTH: {scope.glitch.width}, OFFSET: {scope.glitch.offset}, EXT_OFFSET: {scope.glitch.ext_offset}")
    target.flush()
    scope.arm()

    #Do glitch loop
    target.simpleserial_write("g", bytearray([]))

    ret = scope.capture()

    if ret:
        #print('Timeout - no trigger')
        gc.add("reset")
        resets += 1

        #Device is slow to boot?
        reboot_flush()

    else:
        val = target.simpleserial_read_witherrors('r', 4, glitch_timeout=10, timeout=50)#For loop check
        if val['valid'] is False:
            gc.add("reset")
            reboot_flush()
            resets += 1
            #print(val)
        else:
            gcnt = struct.unpack("<I", val['payload'])[0]

            if gcnt != 2500: #for loop check
                gc.add("success")
                print((scope.glitch.width, scope.glitch.offset, scope.glitch.ext_offset))
                successes += 1
            else:
                gc.add("normal")
    if (successes > 0):
        print("successes = {}, resets = {}, offset = {}, width = {}, ext_offset = {}".format(successes, resets, scope.glitch.offset, scope.glitch.width, scope.glitch.ext_offset))
        total_successes += successes
print("Done glitching")
print("successes = {}, resets = {}, offset = {}, width = {}, ext_offset = {}".format(successes, resets, scope.glitch.offset, scope.glitch.width, scope.glitch.ext_offset))

#enable logging
cw.set_all_log_levels(cw.logging.WARNING)
import chipwhisperer as cw
import matplotlib.pylab as plt
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
    time.sleep(0.05)
    scope.io.nrst = "high_z"
    time.sleep(0.05)
    #Flush garbage too
    target.flush()


gc = glitch.GlitchController(groups=["success", "reset", "normal"], parameters=["repeat", "ext_offset"])
#gc.display_stats()
fig = plt.figure()

cw.set_all_log_levels(cw.logging.CRITICAL)

#ORIG
#g_step = 1
#gc.set_global_step(g_step)
#gc.set_range("repeat", 1, 7)
#gc.set_range("ext_offset", 1, 30)
#scope.glitch.repeat = 0

#ORIG
#REPEAT_MIN=1
#REPEAT_MAX=7
#EXT_OFFSET_MIN=1
#EXT_OFFSET_MAX=30

#FULL SCALE
REPEAT_MIN=1
REPEAT_MAX=7
EXT_OFFSET_MIN=1
EXT_OFFSET_MAX=30

g_step = 1
gc.set_global_step(g_step)
gc.set_range("repeat", REPEAT_MIN, REPEAT_MAX)
gc.set_range("ext_offset", EXT_OFFSET_MIN, EXT_OFFSET_MAX)
scope.glitch.repeat = 0

# sane defaults: https://chipwhisperer.readthedocs.io/en/latest/scope-api.html#chipwhisperer-nano-scope
scope.vglitch_setup(glitcht=None, default_setup=True)

reboot_flush()
broken = False

print(scope)
print("baud = {}".format(target.baud))
print("offset: [{}-{}], repeat: [{}-{}]".format(EXT_OFFSET_MIN,EXT_OFFSET_MAX,REPEAT_MIN,REPEAT_MAX))

for glitch_settings in gc.glitch_values():
    scope.glitch.repeat = glitch_settings[0]
    scope.glitch.ext_offset = glitch_settings[1]
    if broken:
        break
    for i in range(50):
        #print("ext_offset {}, repeat {}".format(scope.glitch.ext_offset,scope.glitch.repeat)) # would show "progress"
        scope.arm()
        
        #target.simpleserial_write('p', bytearray([ord('t'),ord('o'),ord('u'),ord('c'),ord('h')])) #SIMPLESERIAL1 PASS
        target.simpleserial_write('p', bytearray([0]*5)) #SIMPLESERIAL1
        #target.simpleserial_write(0x1, bytearray([0]*5)) #SIMPLESERIAL2
        
        ret = scope.capture()
        
        if ret:
            print('Timeout - no trigger')
            gc.add("reset")
            #Device is slow to boot?
            reboot_flush()

        else:
            val = target.simpleserial_read_witherrors('r', 1, glitch_timeout=10) #For loop check
            #print(val) 
            if val['valid'] is False:
                gc.add("reset")
                reboot_flush()
            else:
                #SIMPLESERIAL1 => would print if not success: "{'valid': True, 'payload': bytearray(b'\x00'), 'full_response': 'r00\n', 'rv': 0}"
                #SIMPLESERIAL2 => would print if not success: {'valid': True, 'payload': CWbytearray(b'00'), 'full_response': CWbytearray(b'00 72 01 00 99 00'), 'rv': bytearray(b'\x00')}
                #print(val) 

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

# cleanup
scope.dis()
target.dis()                   
cw.set_all_log_levels(cw.logging.WARNING)                    


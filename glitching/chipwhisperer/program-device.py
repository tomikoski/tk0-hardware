import chipwhisperer as cw
import sys
import os

scope = cw.scope()
#cw.program_target(scope, cw.programmers.STM32FProgrammer, "./git/chipwhisperer/hardware/victims/firmware/simpleserial-base/simpleserial-base-CWNANO.hex")
#cw.program_target(scope, cw.programmers.STM32FProgrammer, "./git/chipwhisperer/hardware/victims/firmware/simpleserial-glitch/simpleserial-glitch-CWNANO.hex")
print(os.system("ls -ltr " + sys.argv[1]))
cw.program_target(scope, cw.programmers.STM32FProgrammer, sys.argv[1])
scope.dis()

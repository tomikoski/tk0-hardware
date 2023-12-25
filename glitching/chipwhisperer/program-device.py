import chipwhisperer as cw
import os

scope = cw.scope()
HOME = os.path.expanduser('~')

#cw.program_target(scope, cw.programmers.STM32FProgrammer, HOME + "/git/chipwhisperer/hardware/victims/firmware/simpleserial-base/simpleserial-base-CWNANO.hex")
cw.program_target(scope, cw.programmers.STM32FProgrammer, HOME + "/git/chipwhisperer/hardware/victims/firmware/simpleserial-glitch/simpleserial-glitch-CWNANO.hex")

scope.dis()

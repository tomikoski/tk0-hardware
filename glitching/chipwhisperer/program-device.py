import chipwhisperer as cw
scope = cw.scope()

cw.program_target(scope, cw.programmers.STM32FProgrammer, "$HOME/git/chipwhisperer/hardware/victims/firmware/simpleserial-base/simpleserial-base-CWNANO.hex")

scope.dis()

import chipwhisperer as cw
import time

# Setup a connection with the CW board
# and fetch the scope for using this board.
scope = cw.scope()

# The default settings are fine for now.
#scope.default_setup()

# Fetch the target from the scope
# This should be automatically connected
#target = cw.target(scope)
target = cw.target(scope, cw.targets.SimpleSerial) #cw.targets.SimpleSerial can be omitted

scope.arm()

msg = bytearray([0]*16) #simpleserial uses bytearrays
target.simpleserial_write('p', msg)

a = 0
while(a < 10):
  t = scope.get_last_trace()
  print(t)
  time.sleep(1)
  a+=1

scope.dis()
target.dis()


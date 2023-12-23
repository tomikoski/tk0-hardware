import chipwhisperer as cw

# Setup a connection with the CW board
# and fetch the scope for using this board.
scope = cw.scope()

# The default settings are fine for now.
#scope.default_setup()

# Fetch the target from the scope
# This should be automatically connected
#target = cw.target(scope)
target = cw.target(scope, cw.targets.SimpleSerial) #cw.targets.SimpleSerial can be omitted

msg = bytearray([0x00]*16) #simpleserial uses bytearrays
target.simpleserial_write('p', msg)
print(target.simpleserial_read('r', 16))

msg = bytearray([0x01]*16) #simpleserial uses bytearrays
target.simpleserial_write('k', msg)
print(target.simpleserial_wait_ack()) #should return 0

# NOT WORKING?!
#target.write('p' + '0'*16) #fill in the rest here
#print(target.simpleserial_read('r', 16))

scope.dis()
target.dis()


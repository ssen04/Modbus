# Reading Temperature and RH from Probe connected to Indigo500 Transmitter
import struct
import datetime
from pyModbusTCP.client import ModbusClient

# Constants
IP = '172.30.31.33'
PORT = 502
UNIT_ID = 241

# Specify the time in hours till which measurement would continue
end = datetime.datetime.now() + datetime.timedelta(hours=48)


# Converts the data from two registers to a 32-bit float
# Takes the holding register data and the index of the register as inputs
# Returns 32-bit float
def data_from_register(registers, i):
    return struct.unpack('!f', bytes.fromhex('{0:04x}'.format(registers[i]) + '{0:04x}'.format(registers[i - 1])))[0]


# TCP auto connect on first modbus request
print("Connecting to probe ... ")
c = ModbusClient(host=IP, port=PORT, unit_id=UNIT_ID, auto_open=True)
print("Connected to probe!")
# Printing the device specs
print(c, "\n")

while datetime.datetime.now() < end:
    regs = c.read_holding_registers(0, 10)
    # Print the registers read
    print("Registers read : ", regs)
    if regs:
        rh = data_from_register(regs, 1)  # get the RH
        t = data_from_register(regs, 3)  # get the Temperature
        dp = data_from_register(regs, 9)  # get the Dew Point
        with open("datalog.csv", "a") as f:
            line = f"RH: {rh}, Temperature: {t}, Dew Point {dp}\n"
            print(line)
            f.write(line)
    else:
        print("Read error")


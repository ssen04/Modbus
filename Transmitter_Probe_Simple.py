import struct

from pyModbusTCP.client import ModbusClient


def data_from_register(registers, i):
    return struct.unpack('!f', bytes.fromhex('{0:04x}'.format(registers[i]) + '{0:04x}'.format(registers[i - 1])))[0]


# TCP auto connect on first modbus request
c = ModbusClient(host="192.168.5.20", port=502, unit_id=241, auto_open=True)
print("Connected to port")

print(c)

while (True):
    regs = c.read_holding_registers(0, 10)

    print("Registers read")
    if regs:
        print(regs)
        rh = data_from_register(regs, 1)
        t = data_from_register(regs, 3)
        dp = data_from_register(regs, 9)
        line = f"RH: {rh}, Temperature: {t}, Dew Point {dp}\n"
        print(line)

    else:
        print("read error")

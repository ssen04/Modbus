from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import time
import datetime

RATE = 1  # The poll rate in seconds (default 1)
LENGTH = 48  # The length of time in hours to data log (default 9999999)
FILE = 'datalog.csv'  # The filename to store the data (default data.csv)
PORT = 'COM7'  # Communication port of the probe
ADDRESS = 240  # The address of the probe (default 240)

# Modbus connection
probe = ModbusClient(method='rtu', port=PORT, timeout=1, baudrate=9600, stopbits=1, parity='N')

end = datetime.datetime.now() + datetime.timedelta(hours=LENGTH)

print("End date and time: ", end)


# Converts the data from two registers to a 32-bit float
# Takes the holding register data and the index of the register as inputs
# Returns 32-bit float
def data_from_register(registers, i):
    return struct.unpack('!f', bytes.fromhex('{0:04x}'.format(registers[i]) + '{0:04x}'.format(registers[i - 1])))[0]


# Reads the holding registers of the probe and returns the values as 32-bit float
# Returns True, Relative Humidity, Temperature and Dew Point if read successfully
# Returns False, None, None, None if not
def holding_registers_data():
    try:
        registers = probe.read_holding_registers(address=0, count=10, unit=ADDRESS).registers

    except Exception as e:
        print(e)
        return False, None, None, None
    try:
        rh = data_from_register(registers, 1)
        t = data_from_register(registers, 3)
        dp = data_from_register(registers, 9)

    except Exception as e:
        print(e)
        return False, None, None, None

    return True, rh, t, dp


# Logging the data

# Reads relative humidity, temperature and dew point from holding_registers_data() and writes the values to a csv file with the date and time
def data_logger():
    probe.connect()
    successful, rh, t, dp = holding_registers_data()
    if (successful):
        dt = datetime.datetime.now()

        try:
            with open(FILE, "a") as f:
                line = f"Date and Time: {dt}, RH: {rh}, Temperature: {t}, Dew Point {dp}\n"
                print(line)
                f.write(line)
        except Exception as e:
            print(e)
        probe.close()
        time.sleep(RATE)

    else:
        probe.close()
        time.sleep(0.5)


def main():
    while datetime.datetime.now() < end:
        data_logger()


if __name__ == "__main__":
    main()

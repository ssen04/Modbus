from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import time
import datetime
import argparse

# Parameters
parser = argparse.ArgumentParser(
    description="Modbus data logger"
)

parser.add_argument('port', help="The COM port where the probe is attached")
parser.add_argument('-f', '--file', help="The file name to store the data (default data.csv)", default="data.csv")
parser.add_argument('-a', '--address', help="The address of the probe (default 240)", default=240, type=int)
parser.add_argument('-r', "--rate", help="The poll rate in seconds (default 1)", default=1, type=float)
parser.add_argument('-l', '--length', help="The length of time in hours to data log (default 9999999)", type=float, default=9999999)

args = parser.parse_args()
print(args)

# Modbus connection
probe = ModbusClient(method='rtu', port=args.port, timeout=1, baudrate=9600, stopbits=1, parity='N')

end = datetime.datetime.now() + datetime.timedelta(hours=args.length)

print("End date and time: ", end)


# Converts the data from two registers to a 32-bit float
# Takes the holding register data and the index of the register as inputs
# Returns 32-bit float
def data_from_register(registers, i):
    return struct.unpack('!f', bytes.fromhex('{0:04x}'.format(registers[i]) + '{0:04x}'.format(registers[i - 1])))[0]


# Reads the holding registers of the probe and returns the values as 32-bit float
# Returns True, Relative Humidity, Temperature and Dew Point if read sucessfully
# Returns False, None, None, None if not
def holding_registers_data():
    try:

        registers = probe.read_holding_registers(address=0, count=10, unit=args.address).registers


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
            with open(args.file, "a") as f:
                line = f"{dt},{rh},{t},{dp}\n"
                print(line)
                f.write(line)
        except Exception as e:
            print(e)
        probe.close()
        time.sleep(args.rate)

    else:
        probe.close()
        time.sleep(0.5)


def main():
    while datetime.datetime.now() < end:
        data_logger()


if __name__ == "__main__":
    main()

import serial
import re
import time
import datetime

port = 'COM7'
wt_conn = serial.Serial(port)


# Temperature, pressure, humidity

def wt_tph_setup():
    wt_s = serial.Serial(port)
    wt_s.write(b"0TU,R=1101000011010000,I=60\r\n")  # Query for temperature, pressure and humidity. R=acquire air temperature, pressure and humidity,I=update interval
    line = wt_conn.readline().decode()
    return (line)


# Uncomment to check all settings
print(wt_tph_setup())


# Data acquisition

def wt_connection():
    wt_conn = serial.Serial(port)
    wt_conn.write(b"0R0\r\n")  # Query to acquire all wanted data
    line = wt_conn.readline().decode()
    data = re.findall("[0-9]+\\.[0-9]+|[0-9]+", line)
    return (data)


# Check data acquisition
while True:
    dt = [datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")]
    wt = wt_connection()
    wt_data = dt + [wt[2], wt[3], wt[4], wt[5], wt[6], wt[7], wt[8], wt[9]]
    print(wt_data)
    time.sleep(60)

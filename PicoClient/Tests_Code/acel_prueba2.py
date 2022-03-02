import machine
import utime
import ustruct
import sys

###############################################################################
# Constants

# I2C address
ADXL343_ADDR = 0x68

# Registers
REG_DEVID = 0x3B
REG_POWER_CTL = 0x2D
REG_DATAX0 = 0x32

# Other constants
DEVID = 0xE5
SENSITIVITY_2G = 1.0 / 256  # (g/LSB)
EARTH_GRAVITY = 9.80665     # Earth's gravity in [m/s^2]

###############################################################################
# Settings

# Initialize I2C with pins
i2c = machine.I2C(0,
                  scl=machine.Pin(17),
                  sda=machine.Pin(16),
                  freq=400000)

###############################################################################
# Functions

def reg_write(i2c, addr, reg, data):
    """
    Write bytes to the specified register.
    """
    
    # Construct message
    msg = bytearray()
    msg.append(data)
    
    # Write out message to register
    i2c.writeto_mem(addr, reg, msg)
    utime.sleep_ms(100)
    
def reg_read(i2c, addr, reg, nbytes=1):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """
    
    # Check to make sure caller is asking for 1 or more bytes
    if nbytes < 1:
        return bytearray()
    
    # Request data from specified register(s) over I2C
    data = i2c.readfrom_mem(addr, reg, nbytes)
    
    return data

###############################################################################
# Main

# Read device ID to make sure that we can communicate with the ADXL343
utime.sleep_ms(100)
data = reg_read(i2c, ADXL343_ADDR, REG_DEVID)
if (data != bytearray((DEVID,))):
    print("ERROR: Could not communicate with ADXL343")
    sys.exit()
    
# Read Power Control register
data = reg_read(i2c, ADXL343_ADDR, REG_POWER_CTL)
print(data)

# Tell ADXL343 to start taking measurements by setting Measure bit to high
data = int.from_bytes(data, "big") | (1 << 3)
reg_write(i2c, ADXL343_ADDR, REG_POWER_CTL, data)

# Test: read Power Control register back to make sure Measure bit was set
data = reg_read(i2c, ADXL343_ADDR, REG_POWER_CTL)
print(data)

# Wait before taking measurements
utime.sleep(2.0)

# Run forever
while True:
    
    # Read X, Y, and Z values from registers (16 bits each)
    data = reg_read(i2c, ADXL343_ADDR, REG_DATAX0, 6)

    # Convert 2 bytes (little-endian) into 16-bit integer (signed)
    acc_x = ustruct.unpack_from("<h", data, 0)[0]
    acc_y = ustruct.unpack_from("<h", data, 2)[0]
    acc_z = ustruct.unpack_from("<h", data, 4)[0]

    # Convert measurements to [m/s^2]
    acc_x = acc_x * SENSITIVITY_2G * EARTH_GRAVITY
    acc_y = acc_y * SENSITIVITY_2G * EARTH_GRAVITY
    acc_z = acc_z * SENSITIVITY_2G * EARTH_GRAVITY

    # Print results
    print("X:", "{:.2f}".format(acc_x), \
          "| Y:", "{:.2f}".format(acc_y), \
          "| Z:", "{:.2f}".format(acc_z))
    
    utime.sleep(0.1)
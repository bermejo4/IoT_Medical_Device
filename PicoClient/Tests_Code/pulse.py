
import utime
from machine import Pin, ADC, Signal
import uos
#import utime
import rp2
from rp2 import PIO, asm_pio
#from machine import Pin
from time import sleep
import onewire
from ds18x20 import DS18X20
import binascii
import struct
import math
import utime
from machine import Pin, I2C


class MPU6050Data:

    def __init__(self):
        self.Gx=0
        self.Gy=0
        self.Gz=0
        self.Temperature=0
        self.Gyrox=0
        self.Gyroy=0
        self.Gyroz=0

class MPU6050:

    AccelerationFactor= 2.0/32768.0;   #assuming +/- 16G
    GyroFactor=500.0 / 32768.0;         #assuming 500 degree / sec

    # Temperature in degrees C = (TEMP_OUT Register Value as a signed quantity)/340 + 36.53
    TemperatureGain = 1.0 / 340.0
    TemperatureOffset = 36.53

    #converted from Jeff Rowberg code https://github.com/jrowberg/i2cdevlib/blob/master/Arduino/MPU6050/MPU6050.h


    #register definition

    MPU6050_RA_XG_OFFS_TC = 0x00 # [7] PWR_MODE, [6:1] XG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_YG_OFFS_TC = 0x01 # [7] PWR_MODE, [6:1] YG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_ZG_OFFS_TC = 0x02 # [7] PWR_MODE, [6:1] ZG_OFFS_TC, [0] OTP_BNK_VLD
    MPU6050_RA_X_FINE_GAIN = 0x03 # [7:0] X_FINE_GAIN
    MPU6050_RA_Y_FINE_GAIN = 0x04 # [7:0] Y_FINE_GAIN
    MPU6050_RA_Z_FINE_GAIN = 0x05  # [7:0] Z_FINE_GAIN
    MPU6050_RA_XA_OFFS_H = 0x06  # [15:0] XA_OFFS
    MPU6050_RA_XA_OFFS_L_TC = 0x07
    MPU6050_RA_YA_OFFS_H = 0x08  #[15:0] YA_OFFS
    MPU6050_RA_YA_OFFS_L_TC = 0x09
    MPU6050_RA_ZA_OFFS_H = 0x0A  #[15:0] ZA_OFFS
    MPU6050_RA_ZA_OFFS_L_TC = 0x0B
    MPU6050_RA_XG_OFFS_USRH = 0x13  #[15:0] XG_OFFS_USR
    MPU6050_RA_XG_OFFS_USRL = 0x14
    MPU6050_RA_YG_OFFS_USRH = 0x15  #[15:0] YG_OFFS_USR
    MPU6050_RA_YG_OFFS_USRL = 0x16
    MPU6050_RA_ZG_OFFS_USRH = 0x17  #[15:0] ZG_OFFS_USR
    MPU6050_RA_ZG_OFFS_USRL = 0x18
    MPU6050_RA_SMPLRT_DIV = 0x19
    MPU6050_RA_CONFIG = 0x1A
    MPU6050_RA_GYRO_CONFIG = 0x1B
    MPU6050_RA_ACCEL_CONFIG = 0x1C
    MPU6050_RA_FF_THR = 0x1D
    MPU6050_RA_FF_DUR = 0x1E
    MPU6050_RA_MOT_THR = 0x1F
    MPU6050_RA_MOT_DUR = 0x20
    MPU6050_RA_ZRMOT_THR = 0x21
    MPU6050_RA_ZRMOT_DUR = 0x22
    MPU6050_RA_FIFO_EN = 0x23
    MPU6050_RA_I2C_MST_CTRL = 0x24
    MPU6050_RA_I2C_SLV0_ADDR = 0x25
    MPU6050_RA_I2C_SLV0_REG = 0x26
    MPU6050_RA_I2C_SLV0_CTRL = 0x27
    MPU6050_RA_I2C_SLV1_ADDR = 0x28
    MPU6050_RA_I2C_SLV1_REG = 0x29
    MPU6050_RA_I2C_SLV1_CTRL = 0x2A
    MPU6050_RA_I2C_SLV2_ADDR = 0x2B
    MPU6050_RA_I2C_SLV2_REG = 0x2C
    MPU6050_RA_I2C_SLV2_CTRL = 0x2D
    MPU6050_RA_I2C_SLV3_ADDR = 0x2E
    MPU6050_RA_I2C_SLV3_REG = 0x2F
    MPU6050_RA_I2C_SLV3_CTRL = 0x30
    MPU6050_RA_I2C_SLV4_ADDR = 0x31
    MPU6050_RA_I2C_SLV4_REG = 0x32
    MPU6050_RA_I2C_SLV4_DO = 0x33
    MPU6050_RA_I2C_SLV4_CTRL = 0x34
    MPU6050_RA_I2C_SLV4_DI = 0x35
    MPU6050_RA_I2C_MST_STATUS = 0x36
    MPU6050_RA_INT_PIN_CFG = 0x37
    MPU6050_RA_INT_ENABLE = 0x38
    MPU6050_RA_DMP_INT_STATUS = 0x39
    MPU6050_RA_INT_STATUS = 0x3A
    MPU6050_RA_ACCEL_XOUT_H = 0x3B
    MPU6050_RA_ACCEL_XOUT_L = 0x3C
    MPU6050_RA_ACCEL_YOUT_H = 0x3D
    MPU6050_RA_ACCEL_YOUT_L = 0x3E
    MPU6050_RA_ACCEL_ZOUT_H = 0x3F
    MPU6050_RA_ACCEL_ZOUT_L = 0x40
    MPU6050_RA_TEMP_OUT_H = 0x41
    MPU6050_RA_TEMP_OUT_L = 0x42
    MPU6050_RA_GYRO_XOUT_H = 0x43
    MPU6050_RA_GYRO_XOUT_L = 0x44
    MPU6050_RA_GYRO_YOUT_H = 0x45
    MPU6050_RA_GYRO_YOUT_L = 0x46
    MPU6050_RA_GYRO_ZOUT_H = 0x47
    MPU6050_RA_GYRO_ZOUT_L = 0x48
    MPU6050_RA_EXT_SENS_DATA_00 = 0x49
    MPU6050_RA_EXT_SENS_DATA_01 = 0x4A
    MPU6050_RA_EXT_SENS_DATA_02 = 0x4B
    MPU6050_RA_EXT_SENS_DATA_03 = 0x4C
    MPU6050_RA_EXT_SENS_DATA_04 = 0x4D
    MPU6050_RA_EXT_SENS_DATA_05 = 0x4E
    MPU6050_RA_EXT_SENS_DATA_06 = 0x4F
    MPU6050_RA_EXT_SENS_DATA_07 = 0x50
    MPU6050_RA_EXT_SENS_DATA_08 = 0x51
    MPU6050_RA_EXT_SENS_DATA_09 = 0x52
    MPU6050_RA_EXT_SENS_DATA_10 = 0x53
    MPU6050_RA_EXT_SENS_DATA_11 = 0x54
    MPU6050_RA_EXT_SENS_DATA_12 = 0x55
    MPU6050_RA_EXT_SENS_DATA_13 = 0x56
    MPU6050_RA_EXT_SENS_DATA_14 = 0x57
    MPU6050_RA_EXT_SENS_DATA_15 = 0x58
    MPU6050_RA_EXT_SENS_DATA_16 = 0x59
    MPU6050_RA_EXT_SENS_DATA_17 = 0x5A
    MPU6050_RA_EXT_SENS_DATA_18 = 0x5B
    MPU6050_RA_EXT_SENS_DATA_19 = 0x5C
    MPU6050_RA_EXT_SENS_DATA_20 = 0x5D
    MPU6050_RA_EXT_SENS_DATA_21 = 0x5E
    MPU6050_RA_EXT_SENS_DATA_22 = 0x5F
    MPU6050_RA_EXT_SENS_DATA_23 = 0x60
    MPU6050_RA_MOT_DETECT_STATUS = 0x61
    MPU6050_RA_I2C_SLV0_DO = 0x63
    MPU6050_RA_I2C_SLV1_DO = 0x64
    MPU6050_RA_I2C_SLV2_DO = 0x65
    MPU6050_RA_I2C_SLV3_DO = 0x66
    MPU6050_RA_I2C_MST_DELAY_CTRL = 0x67
    MPU6050_RA_SIGNAL_PATH_RESET = 0x68
    MPU6050_RA_MOT_DETECT_CTRL = 0x69
    MPU6050_RA_USER_CTRL = 0x6A
    MPU6050_RA_PWR_MGMT_1 = 0x6B
    MPU6050_RA_PWR_MGMT_2 = 0x6C
    MPU6050_RA_BANK_SEL = 0x6D
    MPU6050_RA_MEM_START_ADDR = 0x6E
    MPU6050_RA_MEM_R_W = 0x6F
    MPU6050_RA_DMP_CFG_1 = 0x70
    MPU6050_RA_DMP_CFG_2 = 0x71
    MPU6050_RA_FIFO_COUNTH = 0x72
    MPU6050_RA_FIFO_COUNTL = 0x73
    MPU6050_RA_FIFO_R_W = 0x74
    MPU6050_RA_WHO_AM_I = 0x75     

    ZeroRegister = [
        MPU6050_RA_FF_THR, #Freefall threshold of |0mg|  LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FF_THR, 0x00);
        MPU6050_RA_FF_DUR, #Freefall duration limit of 0   LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FF_DUR, 0x00);
        MPU6050_RA_MOT_THR, #Motion threshold of 0mg     LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_MOT_THR, 0x00);
        MPU6050_RA_MOT_DUR, #Motion duration of 0s    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_MOT_DUR, 0x00);
        MPU6050_RA_ZRMOT_THR, #Zero motion threshold    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_ZRMOT_THR, 0x00);
        MPU6050_RA_ZRMOT_DUR, #Zero motion duration threshold    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_ZRMOT_DUR, 0x00);
        MPU6050_RA_FIFO_EN, #Disable sensor output to FIFO buffer    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FIFO_EN, 0x00);
        MPU6050_RA_I2C_MST_CTRL, #AUX I2C setup    //Sets AUX I2C to single master control, plus other config    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_MST_CTRL, 0x00);
        MPU6050_RA_I2C_SLV0_ADDR, #Setup AUX I2C slaves    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_ADDR, 0x00);
        MPU6050_RA_I2C_SLV0_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_REG, 0x00);
        MPU6050_RA_I2C_SLV0_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_CTRL, 0x00);
        MPU6050_RA_I2C_SLV1_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_ADDR, 0x00);
        MPU6050_RA_I2C_SLV1_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_REG, 0x00);
        MPU6050_RA_I2C_SLV1_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_CTRL, 0x00);
        MPU6050_RA_I2C_SLV2_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_ADDR, 0x00);
        MPU6050_RA_I2C_SLV2_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_REG, 0x00);
        MPU6050_RA_I2C_SLV2_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_CTRL, 0x00);
        MPU6050_RA_I2C_SLV3_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_ADDR, 0x00);
        MPU6050_RA_I2C_SLV3_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_REG, 0x00);
        MPU6050_RA_I2C_SLV3_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_CTRL, 0x00);
        MPU6050_RA_I2C_SLV4_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_ADDR, 0x00);
        MPU6050_RA_I2C_SLV4_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_REG, 0x00);
        MPU6050_RA_I2C_SLV4_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_DO, 0x00);
        MPU6050_RA_I2C_SLV4_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_CTRL, 0x00);
        MPU6050_RA_I2C_SLV4_DI, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_DI, 0x00);
        MPU6050_RA_INT_PIN_CFG, #MPU6050_RA_I2C_MST_STATUS //Read-only    //Setup INT pin and AUX I2C pass through    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_INT_PIN_CFG, 0x00);
        MPU6050_RA_INT_ENABLE, #Enable data ready interrupt      LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_INT_ENABLE, 0x00);
        MPU6050_RA_I2C_SLV0_DO, #Slave out, dont care    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_DO, 0x00);
        MPU6050_RA_I2C_SLV1_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_DO, 0x00);
        MPU6050_RA_I2C_SLV2_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_DO, 0x00);
        MPU6050_RA_I2C_SLV3_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_DO, 0x00);
        MPU6050_RA_I2C_MST_DELAY_CTRL, #More slave config      LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_MST_DELAY_CTRL, 0x00);
        MPU6050_RA_SIGNAL_PATH_RESET, #Reset sensor signal paths    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_SIGNAL_PATH_RESET, 0x00);
        MPU6050_RA_MOT_DETECT_CTRL, #Motion detection control    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_MOT_DETECT_CTRL, 0x00);
        MPU6050_RA_USER_CTRL, #Disables FIFO, AUX I2C, FIFO and I2C reset bits to 0    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_USER_CTRL, 0x00);
        MPU6050_RA_CONFIG, #Disable FSync, 256Hz DLPF    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_CONFIG, 0x00);
        MPU6050_RA_FF_THR, #Freefall threshold of |0mg|    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FF_THR, 0x00);
        MPU6050_RA_FF_DUR, #Freefall duration limit of 0    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FF_DUR, 0x00);
        MPU6050_RA_MOT_THR, #Motion threshold of 0mg    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_MOT_THR, 0x00);
        MPU6050_RA_MOT_DUR, #Motion duration of 0s    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_MOT_DUR, 0x00);
        MPU6050_RA_ZRMOT_THR, #Zero motion threshold    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_ZRMOT_THR, 0x00);
        MPU6050_RA_ZRMOT_DUR, #Zero motion duration threshold    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_ZRMOT_DUR, 0x00);
        MPU6050_RA_FIFO_EN, #Disable sensor output to FIFO buffer    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FIFO_EN, 0x00);
        MPU6050_RA_I2C_MST_CTRL, #AUX I2C setup    //Sets AUX I2C to single master control, plus other config    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_MST_CTRL, 0x00);
        MPU6050_RA_I2C_SLV0_ADDR, #Setup AUX I2C slaves    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_ADDR, 0x00);
        MPU6050_RA_I2C_SLV0_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_REG, 0x00);
        MPU6050_RA_I2C_SLV0_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_CTRL, 0x00);
        MPU6050_RA_I2C_SLV1_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_ADDR, 0x00);
        MPU6050_RA_I2C_SLV1_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_REG, 0x00);
        MPU6050_RA_I2C_SLV1_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_CTRL, 0x00);
        MPU6050_RA_I2C_SLV2_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_ADDR, 0x00);
        MPU6050_RA_I2C_SLV2_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_REG, 0x00);
        MPU6050_RA_I2C_SLV2_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_CTRL, 0x00);
        MPU6050_RA_I2C_SLV3_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_ADDR, 0x00);
        MPU6050_RA_I2C_SLV3_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_REG, 0x00);
        MPU6050_RA_I2C_SLV3_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_CTRL, 0x00);
        MPU6050_RA_I2C_SLV4_ADDR, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_ADDR, 0x00);
        MPU6050_RA_I2C_SLV4_REG, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_REG, 0x00);
        MPU6050_RA_I2C_SLV4_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_DO, 0x00);
        MPU6050_RA_I2C_SLV4_CTRL, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_CTRL, 0x00);
        MPU6050_RA_I2C_SLV4_DI, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV4_DI, 0x00);
        MPU6050_RA_I2C_SLV0_DO, #Slave out, dont care    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV0_DO, 0x00);
        MPU6050_RA_I2C_SLV1_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV1_DO, 0x00);
        MPU6050_RA_I2C_SLV2_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV2_DO, 0x00);
        MPU6050_RA_I2C_SLV3_DO, #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_SLV3_DO, 0x00);
        MPU6050_RA_I2C_MST_DELAY_CTRL, #More slave config    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_I2C_MST_DELAY_CTRL, 0x00);
        MPU6050_RA_SIGNAL_PATH_RESET, #Reset sensor signal paths    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_SIGNAL_PATH_RESET, 0x00);
        MPU6050_RA_MOT_DETECT_CTRL, #Motion detection control    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_MOT_DETECT_CTRL, 0x00);
        MPU6050_RA_USER_CTRL, #Disables FIFO, AUX I2C, FIFO and I2C reset bits to 0    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_USER_CTRL, 0x00);
        MPU6050_RA_INT_PIN_CFG, #MPU6050_RA_I2C_MST_STATUS //Read-only    //Setup INT pin and AUX I2C pass through    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_INT_PIN_CFG, 0x00);
        MPU6050_RA_INT_ENABLE, #Enable data ready interrupt    LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_INT_ENABLE, 0x00);
        MPU6050_RA_FIFO_R_W ] #LDByteWriteI2C(MPU6050_ADDRESS, MPU6050_RA_FIFO_R_W, 0x00);


    def reg_write(self,reg_addr,value):
        self.i2c.writeto_mem(self.MPU6050_ADDRESS,reg_addr,value)

    def reg_writeByte(self,reg_addr,value):
        self.reg_write(reg_addr,bytes((value,)))

    def reg_read(self,reg_addr, count):
        return self.i2c.readfrom_mem(self.MPU6050_ADDRESS,reg_addr,count)

    def __init__(self, bus=1, address=0x68, scl=Pin(15), sda=Pin(14), freq=400000):
        self.i2c = I2C(bus,scl=scl,sda=sda,freq=freq)
        self.MPU6050_ADDRESS = address
        self.setSampleRate(100)
        self.setGResolution(2)
        self.setGyroResolution(250)
        # Disable gyro self tests, scale of 500 degrees/s
        self.reg_writeByte(self.MPU6050_RA_GYRO_CONFIG, 0b00001000)

        for loop in self.ZeroRegister:
            self.reg_writeByte(loop,0)

        # Sets clock source to gyro reference w/ PLL
        self.reg_writeByte(self.MPU6050_RA_PWR_MGMT_1, 0b00000010)

        #Controls frequency of wakeups in accel low power mode plus the sensor standby modes
        self.reg_writeByte(self.MPU6050_RA_PWR_MGMT_2, 0x00)

        self.reg_writeByte(self.MPU6050_RA_INT_ENABLE, 0x01)
        self.readStatus()
        self.fifoCount =0

    def readDataFromFifo(self,nCount=None):
        # first check how many bytes in temporary fifo counter
        if self.fifoCount == 0 :
            self.fifoCount = self.readFifoCount()

        #max block transfer in i2c is 32 bytes including the address
        # accelerometer, gyro and temperature  data=> 7 short  = 14 bytes  => 31 bytes / 14 = 2
        # then it will be 28
        if nCount is None:
            if (self.fifoCount > 28) :
                nCount = 28
            else:
                nCount = self.fifoCount
        GData = self.reg_read(self.MPU6050_RA_FIFO_R_W, nCount)
        self.fifoCount = self.fifoCount - nCount
        return GData

    def readData(self):
        #read accelerometers , temperature and gyro
        GData = self.reg_read(self.MPU6050_RA_ACCEL_XOUT_H,14)
        #convert list of 14 values bytes into MPU6050Data struct in engineering units
        return self.convertData(GData)

    def convertData(self,ListData):
        ShortData = struct.unpack(">hhhhhhh", bytearray(ListData))
        #lets create the Data Class
        AccData = MPU6050Data()

        # first 3 short value are Accelerometer

        AccData.Gx = ShortData[0] * self.AccelerationFactor
        AccData.Gy = ShortData[1] * self.AccelerationFactor
        AccData.Gz = ShortData[2] * self.AccelerationFactor

        #temperature
        AccData.Temperature = ShortData[3] * self.TemperatureGain + self.TemperatureOffset

        #and the 3 last ar'e the gyro data

        AccData.Gyrox = ShortData[4] * self.GyroFactor
        AccData.Gyroy = ShortData[5] * self.GyroFactor
        AccData.Gyroz = ShortData[6] * self.GyroFactor

        return AccData

    def setGyroResolution(self, value):
        #use dictionary to get correct G resolution 2,4,8 or 16G
        self.reg_writeByte(self.MPU6050_RA_GYRO_CONFIG,{250 : 0 , 500 : 8 , 1000 : 16 , 2000 : 24}[value])
        self.GyroFactor= value/32768.0;


    def setGResolution(self, value):
        #use dictionary to get correct G resolution 2,4,8 or 16G
        self.reg_writeByte(self.MPU6050_RA_ACCEL_CONFIG,{2 : 0 , 4 : 8 , 8 : 16 , 16 : 24}[value])
        self.AccelerationFactor= value/32768.0;


    def setSampleRate(self, Rate):
        SampleReg =  int(( 8000 / Rate) -1)
        self.SampleRate = 8000.0 / (SampleReg + 1.0)
        self.reg_writeByte(self.MPU6050_RA_SMPLRT_DIV,SampleReg)


    def readStatus(self):
        return  self.reg_read(self.MPU6050_RA_INT_STATUS,1
                          )

    def readFifoCount(self):
        GData=self.reg_read(self.MPU6050_RA_FIFO_COUNTH,2)
        self.fifoCount = (GData[0] * 256 + GData[1])
        return self.fifoCount

    def readFifo(self, ByteCount):
        GData = self.reg_read(self.MPU6050_RA_FIFO_R_W ,ByteCount)
        return GData

    def resetFifo(self):
        self.reg_writeByte(self.MPU6050_RA_USER_CTRL,0b00000000)
        pass
        self.reg_writeByte(self.MPU6050_RA_USER_CTRL,0b00000100)
        pass
        self.reg_writeByte(self.MPU6050_RA_USER_CTRL,0b01000000)

    def enableFifo(self,flag):
        self.reg_writeByte(self.MPU6050_RA_FIFO_EN,0)
        if flag:
            self.resetFifo()
            self.reg_writeByte(self.MPU6050_RA_FIFO_EN,0b11111000)
            print('enable fifo',self.reg_read(self.MPU6050_RA_FIFO_EN,1))



UseFifo = True


def sendCMD_waitResp(cmd, uart=machine.UART(0, baudrate=115200), timeout=2000):
    print("CMD: " + cmd)
    uart.write(cmd)
    waitResp(uart, timeout)
    print()
    
def waitResp(uart=machine.UART(0, baudrate=115200), timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
        
# send CMD to uart,
# wait and show response without return
def sendCMD_waitAndShow(cmd, uart=machine.UART(0, baudrate=115200)):
    print("CMD: " + cmd)
    uart.write(cmd)
    while True:
        print(uart.readline())
        
def espSend(text="test", uart=machine.UART(0, baudrate=115200)):
    sendCMD_waitResp('AT+CIPSEND=' + str(len(text)) + '\r\n')
    sendCMD_waitResp(text)


        
def pulse_sensor():
    #pulse_sensor = Pin(26, Pin.IN, Pin.PULL_UP)        # Pulse Sensor PURPLE WIRE connected to ANALOG PIN 0
    #LED_on_board = machine.Pin(25, machine.Pin.OUT)
    #signal=machine.ADC(pulse_sensor) # holds the incoming raw data. Signal value can range from 0-1024
    #signal.atten(machine.ADC.ATTN_11DB)
    pulse_sensor=machine.ADC(2)
    conversion_factor = 3.3 / (65535)
    
    
    while True:
      signal_value = pulse_sensor.read_u16()*conversion_factor
    
      print(signal_value)
      utime.sleep(0.05)
      

def temperature2():
    ow = onewire.OneWire(Pin(13)) #Prepara GPIO4 para usar con OneWire
    sensor = DS18X20(ow) #define un sensor en ese pin
    direcciones = sensor.scan()  #Lee el ID del sensor conectado
    id=direcciones[0]
    #Pasa el ID a formato de texto e imprime
    idHex = binascii.hexlify(bytearray(id))
    print ("ID=",idHex)
    #Lee e imprime la temperatura cada 1 segundo
    while (True):
        sensor.convert_temp ()
        sleep (1)
        temperatura = sensor.read_temp (id)
        print (temperatura)

def temperature():
    ds_pin = machine.Pin(16)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
    roms = ds_sensor.scan()
    print('Found DS devices: ', roms)
    while True:
        ds_sensor.convert_temp()
        utime.sleep_ms(750)
        for rom in roms:
            print(rom)
            print(ds_sensor.read_temp(rom))
        utime.sleep(1)
        
        
def temperature_mcu():
    sensortemp = machine.ADC(4)
    factorconversion = 3.3 / 65365
    while True:
     # VARIABLE CON VALOR EN BRUTO DE LA TEMPERATURA
     rawValue = sensortemp.read_u16() * factorconversion
     temperatura_mcu = 27 - (rawValue - 0.706) / 0.001721
     print(temperatura_mcu)
     utime.sleep(1)
        
def ad8232():
    ecg_pin_output=machine.ADC(0)
    lo_plus=machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_UP).value()
    lo_minus=machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP).value()
    
    while True:
        #print('lo+: '+str(lo_plus))
        #if lo_plus==1 or lo_minus==1:
           # print("!")
       # else:
        signal_value_ecg = ecg_pin_output.read_u16()
        if signal_value_ecg>64000 and signal_value_ecg<65000:
            if signal_value_ecg>64500 and signal_value_ecg<65000:
                print(signal_value_ecg)
                utime.sleep(0.04)
            else:
                print(signal_value_ecg)
                utime.sleep(0.04)

def acelerometer():
    mpu = MPU6050()
    mpu.enableFifo(UseFifo)
    mpu.setSampleRate(40)
    mpu.setGyroResolution(250)
    mpu.setGResolution(2)
    while True:
        if UseFifo:
            byteCount = mpu.readFifoCount()
            if byteCount>= 14:
                g = mpu.convertData(mpu.readDataFromFifo(14))
            else:
                continue
        else:
            g=mpu.readData()
            utime.sleep_ms(25)
        print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}".format(g.Gx,g.Gy,g.Gz))
    
                
class pico_data:
    def __init__(self, temp=None, temp_mcu=None, pulse_sig=None, cord_x=None, cord_y=None, cord_z=None):
        self.temp = temp
        self.temp_mcu = temp_mcu
        self.pulse_sig=pulse_sig
        self.cord_x=cord_x
        self.cord_y=cord_y
        self.cord_z=cord_z
        
    def JSON_transform(self):
        data_string="{"\
                     +"\"Temp\":\""+str(self.temp)+"\""\
                     +",\"TempMcu\":\""+str(self.temp_mcu)+"\""\
                     +",\"PulseSig\":\""+str(self.pulse_sig)+"\""\
                     +",\"Acel_x\":\""+str(self.cord_x)+"\""\
                     +",\"Acel_y\":\""+str(self.cord_y)+"\""\
                     +",\"Acel_z\":\""+str(self.cord_z)+"\""\
                     +"}"
        return data_string
    
def data_collector():
    #INICIALIZACIÓN DEL OBJETO pico
    pico=pico_data()
    #--------------------------------------------------
    #SENSOR TEMPERATURE
    ow = onewire.OneWire(Pin(13)) #Prepara GPIO4 para usar con OneWire
    sensor = DS18X20(ow) #define un sensor en ese pin
    direcciones = sensor.scan()  #Lee el ID del sensor conectado
    id=direcciones[0]
    #Pasa el ID a formato de texto e imprime
    idHex = binascii.hexlify(bytearray(id))
    print ("ID=",idHex)
    #Lee e imprime la temperatura cada 1 segundo
    #while (True):
    sensor.convert_temp ()
        #sleep (1)
    temperatura = sensor.read_temp (id)
        #print (temperatura)
    pico.temp=temperatura
    #--------------------------------------------------
    #MCU TEMPERATURE
    sensortemp = machine.ADC(4)
    factorconversion = 3.3 / 65365
    rawValue = sensortemp.read_u16() * factorconversion
    temperatura_mcu = 27 - (rawValue - 0.706) / 0.001721
    pico.temp_mcu=temperatura_mcu
    #----------------------------------------------------
    #PULSE SIGNAL
    pulse_sensor=machine.ADC(2)
    conversion_factor = 3.3 / (65535)
    #while True:
    signal_value = pulse_sensor.read_u16()*conversion_factor
    pico.pulse_sig=signal_value
      #print(signal_value)
      #utime.sleep(0.05)
    #----------------------------------------------------
    #ACELEROMETER
    mpu = MPU6050()
    mpu.enableFifo(UseFifo)
    mpu.setSampleRate(40)
    mpu.setGyroResolution(250)
    mpu.setGResolution(2)
    while True:
        if UseFifo:
            byteCount = mpu.readFifoCount()
            if byteCount>= 14:
                g = mpu.convertData(mpu.readDataFromFifo(14))
            else:
                continue
        else:
            g=mpu.readData()
            #utime.sleep_ms(25)
        pico.cord_x=g.Gx
        pico.cord_y=g.Gy
        pico.cord_z=g.Gz
        #print("X:{:.2f}  Y:{:.2f}  Z:{:.2f}".format(g.Gx,g.Gy,g.Gz))
        break
    
    #-----------------------------------------   
    #print(pico.temp)
    #print(pico.temp_mcu)
    print(pico.JSON_transform())
    return pico.JSON_transform()
    


    
        
if __name__ == "__main__":
#    from machine import Pin
#     from DHT22 import DHT22
#    import utime
    #dht_data = Pin(15,Pin.IN,Pin.PULL_UP)
    #dht_sensor=DHT22(dht_data,Pin(14,Pin.OUT),dht11=True)
    FREQUENCY_SEND=2000#Hz -> 5ms
    #--------------
    #pulse_sensor()
    #--------------
    #temperature2()
    #--------------
    #ad8232()
    #--------------
    #temperature_mcu()
    #--------------
    #acelerometer()
    #--------------
    print(data_collector())
    
    server_ip="192.168.184.227"
    server_port=9999

    print()
    print("Machine: \t" + uos.uname()[4])
    print("MicroPython: \t" + uos.uname()[3])

    #indicate program started visually
    led_onboard = machine.Pin(25, machine.Pin.OUT)
    led_onboard.value(0)     # onboard LED OFF/ON for 0.5/1.0 sec
    utime.sleep(0.5)
    led_onboard.value(1)
    utime.sleep(1.0)
    led_onboard.value(0)

    uart0 = machine.UART(0, baudrate=115200)
    print(uart0)
    
    sendCMD_waitResp('AT\r\n')          #Test AT startup
    sendCMD_waitResp('AT+CWLAP\r\n', timeout=10000) #List available APs
    sendCMD_waitResp('AT+CWJAP="Rivendel","jeronimo"\r\n', timeout=5000) #Connect to AP
    sendCMD_waitResp('AT+CIFSR\r\n')    #Obtain the Local IP Address
    #sendCMD_waitResp('AT+CIPSTART="TCP","192.168.12.147",9999\r\n')
    sendCMD_waitResp('AT+CIPSTART="TCP","' +
                 server_ip +
                 '",' +
                 str(server_port) +
                 '\r\n')
    espSend()
    
#------------NO TOCAR------------------    

#-----------------------------------------------------        
    while True:
        string_to_send=""
        string_to_send=str(data_collector())
        #utime.sleep_ms(5)
        #utime.sleep_ms(int((1/FREQUENCY_SEND)*1000))
        #print('Enter something:')
        #msg = input()
        #sendCMD_waitResp('AT+CIPSTART="TCP","192.168.12.147",9999\r\n')
        sendCMD_waitResp('AT+CIPSTART="TCP","' +
                     server_ip +
                     '",' +
                     str(server_port) +
                     '\r\n')
        print("enviando:"+string_to_send)
        espSend(string_to_send)

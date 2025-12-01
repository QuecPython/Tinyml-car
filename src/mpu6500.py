import ustruct
import utime
from machine import I2C

_GYRO_CONFIG    = 0x1b
_ACCEL_CONFIG   = 0x1c
_ACCEL_CONFIG2  = 0x1d
_ACCEL_XOUT_H   = 0x3b
_ACCEL_XOUT_L   = 0x3c
_ACCEL_YOUT_H   = 0x3d
_ACCEL_YOUT_L   = 0x3e
_ACCEL_ZOUT_H   = 0x3f
_ACCEL_ZOUT_L   = 0x40
_TEMP_OUT_H     = 0x41
_TEMP_OUT_L     = 0x42
_GYRO_XOUT_H    = 0x43
_GYRO_XOUT_L    = 0x44
_GYRO_YOUT_H    = 0x45
_GYRO_YOUT_L    = 0x46
_GYRO_ZOUT_H    = 0x47
_GYRO_ZOUT_L    = 0x48
_WHO_AM_I       = 0x75

#_ACCEL_FS_MASK     = 0b00011000
ACCEL_FS_SEL_2G     = 0b00000000
ACCEL_FS_SEL_4G     = 0b00001000
ACCEL_FS_SEL_8G     = 0b00010000
ACCEL_FS_SEL_16G    = 0b00011000

_ACCEL_SO_2G    = 16384 # 1 / 16384 ie. 0.061 mg / digit
_ACCEL_SO_4G    = 8192 # 1 / 8192 ie. 0.122 mg / digit
_ACCEL_SO_8G    = 4096 # 1 / 4096 ie. 0.244 mg / digit
_ACCEL_SO_16G   = 2048 # 1 / 2048 ie. 0.488 mg / digit

#_GYRO_FS_MASK = 0b00011000)
GYRO_FS_SEL_250DPS  = 0b00000000
GYRO_FS_SEL_500DPS  = 0b00001000
GYRO_FS_SEL_1000DPS = 0b00010000
GYRO_FS_SEL_2000DPS = 0b00011000

_GYRO_SO_250DPS  = 131
_GYRO_SO_500DPS  = 62.5
_GYRO_SO_1000DPS = 32.8
_GYRO_SO_2000DPS = 16.4

_TEMP_SO     = 333.87
_TEMP_OFFSET = 21

SF_G     = 1
SF_M_S2  = 9.80665 # 1 g = 9.80665 m/s2 ie. standard gravity
SF_DEG_S = 1
SF_RAD_S = 0.017453292519943 # 1 deg/s is 0.017453292519943 rad/s

# MPU6500 的 I2C 地址
MPU6500_ADDRESS = 0x68
I2C_NO = I2C(I2C.I2C1, I2C.STANDARD_MODE)

class I2C_dev(object):
    def __init__(self, i2c, addr):
        self.i2c = i2c
        self.i2c_addr = addr

    def write_data(self, reg, data):
        '''
        i2c write data
        '''
        self.i2c.write(self.i2c_addr, 
                       bytearray(reg), len(reg),
                       bytearray(data), len(data))
        
    def read_data(self, reg, length):
        '''
        i2c read data
        '''
        r_data = [0x00 for i in range(length)]
        r_data = bytearray(r_data)
        self.i2c.read(self.i2c_addr, 
                       bytearray(reg), len(reg),
                       r_data, length,
                       0)
        return list(r_data)


class MPU6500:
    """Class which provides interface to MPU6500 6-axis motion tracking device."""
    def __init__(
        self, i2c,
        accel_fs=ACCEL_FS_SEL_2G, gyro_fs=GYRO_FS_SEL_250DPS,
        accel_sf=SF_M_S2, gyro_sf=SF_RAD_S,
        gyro_offset=[0, 0, 0]
        ):
        
        self.i2c = I2C_dev(i2c, MPU6500_ADDRESS)

        # 0x70 = standalone MPU6500, 0x71 = MPU6250 SIP
        # if self.whoami not in [0x71, 0x70]:
        #     raise RuntimeError("MPU6500 not found in I2C bus.")

        self._accel_so = self._accel_fs(accel_fs)
        self._gyro_so = self._gyro_fs(gyro_fs)
        self._accel_sf = accel_sf
        self._gyro_sf = gyro_sf
        self._gyro_offset = gyro_offset


    def acceleration(self):
        """
        Acceleration measured by the sensor. By default will return a
        3-tuple of X, Y, Z axis acceleration values in m/s^2 as floats. Will
        return values in g if constructor was provided `accel_sf=SF_M_S2`
        parameter.
        """
        so = self._accel_so
        sf = self._accel_sf

        data = self.i2c.read_data([_ACCEL_XOUT_H], 6)

        ax = (data[0] << 8) | data[1]
        ay = (data[2] << 8) | data[3]
        az = (data[4] << 8) | data[5]


        if ax > 32767:
            ax = ax - 65536
        if ay > 32767:
            ay = ay - 65536
        if az > 32767:
            az = az - 65536

        
        return [ax / so * sf, ay / so * sf, az / so * sf]


    def gyro(self):
        """
        X, Y, Z radians per second as floats.
        """
        so = self._gyro_so
        sf = self._gyro_sf
        ox, oy, oz = self._gyro_offset

        data = self.i2c.read_data([_GYRO_XOUT_H], 6)

        gx = (data[0] << 8) | data[1]
        gy = (data[2] << 8) | data[3]
        gz = (data[4] << 8) | data[5]

        if gx > 32767:
            gx = gx - 65536
        if gy > 32767:
            gy = gy - 65536
        if gz > 32767:
            gz = gz - 65536

        return [gx / so * sf, gy / so * sf, gz / so * sf]

    @property
    def whoami(self):
        """ Value of the whoami register. """
        return self.i2c.read_data([_WHO_AM_I], 1)

    def gyro_calibrate(self, count=256, delay=0):
        ox, oy, oz = (0.0, 0.0, 0.0)
        self._gyro_offset = [0.0, 0.0, 0.0]
        n = float(count)

        while count:
            utime.sleep_ms(delay)
            gyro = self.gyro()
            ox += gyro[0]
            oy += gyro[1]
            oz += gyro[2]
            count -= 1

        self._gyro_offset = [ox / n, oy / n, oz / n]
        return self._gyro_offset
    
    def acc_calibrate(self, count=256, delay=0):
        acc_x, acc_y, acc_z = (0.0, 0.0, 0.0)
        acc_offset = [0.0, 0.0, 0.0]
        n = float(count)

        while count:
            utime.sleep_ms(delay)
            acc = self.acceleration()
            acc_x += acc[0]
            acc_y += acc[1]
            acc_z += acc[2]
            count -= 1

        acc_offset = [acc_x / n, acc_y / n, acc_z / n]
        return acc_offset

    def _accel_fs(self, value):
        self.i2c.write_data([_ACCEL_CONFIG], [value])

        # Return the sensitivity divider
        if ACCEL_FS_SEL_2G == value:
            return _ACCEL_SO_2G
        elif ACCEL_FS_SEL_4G == value:
            return _ACCEL_SO_4G
        elif ACCEL_FS_SEL_8G == value:
            return _ACCEL_SO_8G
        elif ACCEL_FS_SEL_16G == value:
            return _ACCEL_SO_16G

    def _gyro_fs(self, value):
        self.i2c.write_data([_GYRO_CONFIG], [value])

        # Return the sensitivity divider
        if GYRO_FS_SEL_250DPS == value:
            return _GYRO_SO_250DPS
        elif GYRO_FS_SEL_500DPS == value:
            return _GYRO_SO_500DPS
        elif GYRO_FS_SEL_1000DPS == value:
            return _GYRO_SO_1000DPS
        elif GYRO_FS_SEL_2000DPS == value:
            return _GYRO_SO_2000DPS

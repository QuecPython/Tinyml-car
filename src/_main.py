try:
    from tinyml import TinyML
    from mpu6500 import MPU6500, I2C_NO
except ImportError:
    from usr.tinyml import TinyML
    from usr.mpu6500 import MPU6500, I2C_NO

import utime
from machine import Timer

tinyml = TinyML(50, 5)

mpu6500 = MPU6500(I2C_NO)

def read_sensor(timer):
    timestamp = utime.ticks_ms()
    acc = mpu6500.acceleration()
    gyro = mpu6500.gyro()

    # print('{} acc_x: {}, acc_y: {}, acc_z: {}, gyro_x: {}, gyro_y: {}, gyro_z: {}\n \n'.format(timestamp, acc[0], acc[1], acc[2], gyro[0], gyro[1], gyro[2]))
    # utime.sleep(2)
    tinyml.collect([acc[0], acc[1], acc[2], gyro[1], gyro[2]])

def check_score(timer):
    score = tinyml.score()
    #print("Score:", score)
    if score:
        print("***************************^-^***************************score:", score)

if __name__ == '__main__':
    # Timer za čitanje senzora (20ms = 50Hz - usklađeno sa TinyML)
    sensor_timer = Timer(0)
    sensor_timer.start(period=20, mode=Timer.PERIODIC, callback=read_sensor)
    
    # Timer za proveru score-a (50ms = 20Hz)
    score_timer = Timer(1)
    score_timer.start(period=50, mode=Timer.PERIODIC, callback=check_score)
    
    print("TinyML system started with Timer-based approach")
    print("Sensor reading: 50Hz (20ms), Score checking: 20Hz (50ms)")
    print("Buffer capacity: 250 samples (1 second @ 50Hz)")
    print("Debounce: 3 consecutive results in 600ms (optimized for circular gestures)")


import time
import board
import adafruit_mpu6050


# Establishes an i2c connection between raspberry pico and raspberry zero
i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

# Once connection is set up and our devices are communicating I can print these>
while True:

        print()
        print("Acceleration: X: %.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
        print("Temperature: %.2f Degrees Celsius" % mpu.temperature)
        print("Gyro: X: %.2f Y: %.2f Z: %.2f rad/s" %( mpu.gyro))
        print()
        time.sleep(1)

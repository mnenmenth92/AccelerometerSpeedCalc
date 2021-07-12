import time
from lsm303d import LSM303D

lsm = LSM303D(0x1e)  # Change to 0x1e if you have soldered the address jumper
alpha = 0.8
x = y = z = 0


while True:
    xyz = lsm.accelerometer()

    x = alpha * x + (1 - alpha) * xyz[0]
    y = alpha * y + (1 - alpha) * xyz[1]
    z = alpha * z + (1 - alpha) * xyz[2]

    xl = xyz[0] - x
    yl = xyz[1] - y
    zl = xyz[2] - z


    print(("{:+06.2f}g : {:+06.2f}g : {:+06.2f}g").format(xl, yl, zl))




    time.sleep(1.0/50)

import time
from lsm303d import LSM303D
import math
from threading import Thread, Event

lsm = LSM303D(0x1e)  # Change to 0x1e if you have soldered the address jumper
alpha = 0.8
x = y = z = 0
velocity = 0
vx = vy = vz = 0

index = 0
while True:
    t1 = time.time()
    sleep_time = 0.001
    xyz = lsm.accelerometer()

    x = alpha * x + (1 - alpha) * xyz[0]
    y = alpha * y + (1 - alpha) * xyz[1]
    z = alpha * z + (1 - alpha) * xyz[2]

    if index > 10:  # remove few first accelerations

        xl = xyz[0] - x
        yl = xyz[1] - y
        zl = xyz[2] - z
        # print(("{:+06.2f}g : {:+06.2f}g : {:+06.2f}g").format(xl, yl, zl))
        vx += (xl * sleep_time)  # sleep time is in seconds
        vy += (yl * sleep_time)  # sleep time is in seconds
        vz += (zl * sleep_time)  # sleep time is in seconds




    index += 1
    time.sleep(sleep_time)
    t2 = time.time()

    print('vx: {:+06.2f} vy: {:+06.2f}  vz: {:+06.2f},   time = {}'.format(vx, vy, vz,t2 - t1))


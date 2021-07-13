from config import VelocityCalcConfig
import time
from lsm303d import LSM303D
from threading import Thread

class VelocityCalc:

    def __init__(self):
        self.lsm = LSM303D(0x1e)
        self.raw_acc = [0, 0, 0]  # raw accelerations
        self.acc = [0, 0, 0]  # accelerations
        self.velocity =[0, 0, 0]
        self.config = VelocityCalcConfig
        self.alpha = self.config.high_pass_filter_coef
        self.runs = True
        self.loop_time = 0



    def get_velocity(self):
        """
        get accelerations data, remove constant g with high pass filter, calculate velocity
        :return:
        """
        while self.runs:
            calc_time_offset = 0.0001  # calculations time coefficient
            time1 = time.time()  # loop started

            xyz = self.lsm.accelerometer()  # gather accelerometer data

            # high pass filter on acceleration to remove constant g
            self.raw_acc[0] = self.alpha * self.raw_acc[0] + (1 - self.alpha) * xyz[0]
            self.raw_acc[1] = self.alpha * self.raw_acc[1] + (1 - self.alpha) * xyz[1]
            self.raw_acc[2] = self.alpha * self.raw_acc[2] + (1 - self.alpha) * xyz[2]
            self.acc[0] = xyz[0] - self.raw_acc[0]
            self.acc[1] = xyz[1] - self.raw_acc[1]
            self.acc[2] = xyz[2] - self.raw_acc[2]
            # velocity calculation
            self.velocity[0] += (self.acc[0] * self.config.loop_time)
            self.velocity[1] += (self.acc[1] * self.config.loop_time)
            self.velocity[2] += (self.acc[2] * self.config.loop_time)


            time2 = time.time() - time1  # time taken by data acquisition and calculations
            time.sleep(self.config.loop_time - time2 - calc_time_offset)  # delay time that left after calculations
            self.loop_time = time.time() - time1  # calc loop time

    def run_acc_data_thread(self):
        acc_thread = Thread(target=self.get_velocity)
        acc_thread.start()

    def support_loop(self):

        time.sleep(self.config.init_delay)  # wait for high pass filter to adapt
        self.velocity = [0, 0, 0]  # reset calculated velocities
        while self.runs:

            # print(("{:+06.2f}g : {:+06.2f}g : {:+06.2f}g,  time: {}").format(
            #     self.acc[0],
            #     self.acc[1],
            #     self.acc[2],
            #     self.loop_time
            # ))
            print(("{:+06.2f}m/s : {:+06.2f}m/s : {:+06.2f}m/s,  time: {}").format(
                self.velocity[0],
                self.velocity[1],
                self.velocity[2],
                self.loop_time
            ))

            time.sleep(self.config.loop_time)


    def run_support_thread(self):
        acc_thread = Thread(target=self.support_loop)
        acc_thread.start()





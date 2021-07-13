from velocity_calc import VelocityCalc
import time

vel_calc = VelocityCalc()
vel_calc.run_acc_data_thread()
vel_calc.run_support_thread()
time.sleep(100)
vel_calc.runs = False
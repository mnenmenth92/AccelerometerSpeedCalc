class VelocityCalcConfig:
    high_pass_filter_coef = 0.8  # high pass filter coefficient default value
    loop_time = 0.01
    init_delay = 0.2  # initial time after which calculated velocity is reset due to high pass filter adaptation
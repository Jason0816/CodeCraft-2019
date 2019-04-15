# -*- coding: UTF-8 -*-
class global_var:
    WEIGHT = 0.003
    RATIO_SPEED = 2
    RATIO_CHANNEL = 2
    INTERVAL = 295
    DELAY = 5
    START_TIME = 49
    NORMAL = [1.007, 1.006, 1.005, 1.004, 1.003, 1.002, 1.001, 1, 0.999, 0.998, 0.997, 0.996, 0.995, 0.994, 0.993]


def get_weight():
    """ 获取权值
        返回值: WEIGHT
    """ 
    return global_var.WEIGHT

def get_ratio_speed():
    """ 获取速度比例
        返回值: RATIO_SPEED
    """ 
    return global_var.RATIO_SPEED

def get_ratio_channel():
    """ 获取车道比例
        返回值: RATIO_CHANNEL
    """ 
    return global_var.RATIO_CHANNEL

def get_interval():
    """ 获取车辆计数
        返回值: INTERVAL
    """ 
    return global_var.INTERVAL

def get_delay():
    """ 获取间隔
        返回值: DELAY
    """ 
    return global_var.DELAY

def get_start_time():
    """ 获取最初车辆出发时间
        返回值: WEIGHT
    """ 
    return global_var.START_TIME

def get_normal(i):
    """ 获取车速匹配系数
        返回值: NORMAL[i]
    """ 
    return global_var.NORMAL[i]

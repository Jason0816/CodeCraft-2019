# -*- coding: utf-8 -*-

# ==============================================================
#                文件读取
# ==============================================================
def data_process(string):
    """ 删除数据两侧括号，并利用','对字符串进行切片处理
        string: 传入的待处理str
        返回值: str string
    """
    # 删除数据两侧括号
    string = string.replace('(', '')
    string = string.replace(')', '')
    # 利用','对字符串进行切片处理，返回类型为list
    string = string.split(",")
    return string

def read_cars(car_path):
    """ 读取车辆信息
        car_path: car.txt路径
        返回值: dict cars{}
    """
    cars = {}
    # 以只读模式打开文件
    with open(car_path, 'r') as f:
        # 跳过文件中的第一行注释
        f.readline()
        datas = f.readlines()
        for data in datas:
            # 数据处理
            data = data_process(data)
            # 按照ID索引添加信息到datas
            # 数据内容依次为：id, from, to, speed, planTime
            cars[int(data[0])] = {'from': int(data[1]), 'to': int(data[2]), \
                                  'speed': int(data[3]), 'time': int(data[4]), \
                                  'priority': int(data[5]), 'preset': int(data[6]), \
                                  'state': -1, 's1': -1, 'direction': 'unknown', 'next_cross': -1, 'should_judge': 1
                                 }
    return cars

def read_roads(road_path):
    """ 读取道路信息
        road_path: roads.txt路径
        返回值: dict roads{}
    """
    roads = {}
    with open(road_path, 'r') as f:
        f.readline()
        datas = f.readlines()
        for data in datas:
            data = data_process(data)
            # 数据内容依次为：id, length, speed, channel, from, to, isDuplex
            roads[int(data[0])] = {'length': int(data[1]), 'speed': int(data[2]), \
                                   'channel': int(data[3]), 'from': int(data[4]), \
                                   'to': int(data[5]), 'isDuplex': bool(int(data[6]))
                                  }         
    return roads

def read_cross(cross_path):
    """ 读取路口信息
        cross_path: cross.txt路径
        返回值: dict cross{}
    """
    cross = {}
    with open(cross_path, 'r') as f:
        f.readline()
        datas = f.readlines()
        for data in datas:
            data = data_process(data)
            # 数据内容依次为：id, road0, road1, road2, road3,
            cross[int(data[0])] = {0: int(data[1]), 1: int(data[2]), 2: int(data[3]), 3: int(data[4])}
    return cross

def read_preset_answer(preset_answer_path):
    """ 读取预置车辆信息
        presetAnswer_path: presetAnswer.txt路径
        返回值: dict presetAnswer{}
    """
    preset_answer = {}
    with open(preset_answer_path, 'r') as f:
        f.readline()
        datas = f.readlines()
        for data in datas:
            path = []
            data = data_process(data)
            for tmp in data:
                path.append(int(tmp))
            path.pop(0)
            path.pop(0)
            # 数据内容依次为：id, road0, road1, road2, road3,
            preset_answer[int(data[0])] = {'time': int(data[1]), 'path': path}
    return preset_answer

def answer2str(answer_time, graph):
    """ 将answer转化为最终的字符串形式

    """
    answer_list = []
    for ans in answer_time:
        path_str = ""
        for i in range(0, len(ans['path']) - 1):
            temp = str(graph[ans['path'][i]][ans['path'][i+1]][1]) + ','
            path_str += temp
            # 去末尾逗号
            path = path_str[:-1]
        answer = '(' + str(ans['car_id']) + ',' + str(ans['time']) + ',' + path + ')'
        answer_list.append(answer)
    return answer_list


def output_answer(answer_path, answer_str):
    """ 将结果写入到answer.txt
        answer_path: answer.txt路径
        answer_list: 结果集 answer_list[], 内部元素为str
    """
    with open(answer_path, 'w+') as f:
        f.write("#(carId,StartTime,RoadId...)" + "\n")
        for line in answer_str:
            f.write(line + "\n")


# ==============================================================
#         用以主函数调用
# ==============================================================
def read_input(car_path, road_path, cross_path, preset_answer_path):
    """ 读取car.txt, road.txt, cross.txt
        car_path: cat.txt路径
        road_path: road.txt路径
        cross_path: cross.txt路径
        返回值: dict cars{}, roads{}, cross{}
    """
    cars = read_cars(car_path)
    roads = read_roads(road_path)
    cross = read_cross(cross_path)
    preset_answer = read_preset_answer(preset_answer_path)
    return cars, roads, cross, preset_answer
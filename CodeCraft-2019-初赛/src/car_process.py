# -*- coding: utf-8 -*-
import config
from file_io import answer2str

# ==============================================================
#                构建地图
# ==============================================================
def get_speed(cars):
    """ 获取车辆的速度
        cars: 车辆信息{}
        返回值: set() car_speed
    """
    tmp = []
    for key in cars:
        tmp.append(cars[key]['speed'])
    car_speeds = set(tmp)
    return car_speeds

def calculate_weight(roads, roads_id, is_pass, car_speed):
    """ 计算道路初始权值
        weight =  length / (speed + channel)
        roads: 道路信息roads{}
        road_id: 道路ID int road_id
        is_pass: 是否通行 bool is_pass
        返回值: float weight
    """
    RATIO_SPEED = config.get_ratio_speed()
    RATIO_CHANNEL = config.get_ratio_channel()
    NORMAL = config.get_normal(roads[roads_id]['speed'] - car_speed)
    if roads[roads_id]['isDuplex'] == True:
        # 道路为双向，则双向通行
        weight = roads[roads_id]['length'] / (RATIO_SPEED * min(roads[roads_id]['speed'], car_speed) \
                 + RATIO_CHANNEL * roads[roads_id]['channel']) / 10 / NORMAL
    else:
        # 道路为单行，通过is_pass判断是通行
        if is_pass == 1:
            weight = roads[roads_id]['length'] / (RATIO_SPEED * min(roads[roads_id]['speed'], car_speed) \
                     + RATIO_CHANNEL * roads[roads_id]['channel']) /10 / NORMAL
        else:
            weight = 99999
    return weight

def build_graph(roads, cross, car_speed):
    """ 构建地图
        roads: 道路信息 roads{}
        cross: 路口信息 cross{}
        返回值: dict graph{}
    """
    # 定义graph
    graph = {}
    #new_cross = {}
    # 初始化格式为map = {key: {}}
    for key in cross:
        graph[key] = {}
    # 构建地图
    # 得到一个节点到所有与之相连节点的权值
    # eg. cross[1][0] = 5000 --> roads[5000][3 or 4] = 2 --> 1: {2: 10}
    for key in cross:
        for i in range(0,4):
            road_id = cross[key][i]
            if road_id == -1:
                continue
            if roads[road_id]['from'] == key:
                # from --> to
                next_cross = roads[road_id]['to']
                is_pass = 1
            else:
                # to --> from
                next_cross = roads[road_id]['from']
                is_pass = 0
            # 这里需要添加权重计算函数，(speed * channel / length) * is_pass * other
            weight = calculate_weight(roads, road_id, is_pass, car_speed)
            graph[key][next_cross] = [weight, road_id]
    return graph

def update_graph(path, graph):
    """ 通过路径更新地图
        path: 车辆行驶路径 path[]
        graph: 地图信息 graph{}
    """
    WEIGHT = config.get_weight()
    for i in range(0, len(path) - 1):
        graph[path[i]][path[i+1]][0] = graph[path[i]][path[i+1]][0] + WEIGHT
    return

def get_cost(roads, path, graph, car_speed):
    cost = 0
    for i in range(0, len(path) - 1):
        length = roads[graph[path[i]][path[i+1]][1]]['length']
        road_speed = roads[graph[path[i]][path[i+1]][1]]['speed']
        cost += length / min(car_speed, road_speed)
    return cost

def get_start(cars):
    """ 获取车辆的所有出发点
        cars: 车辆信息 cars{}
        返回值: set() start
    """
    tmp = []
    for key in cars:
        tmp.append(cars[key]['from'])
    start = set(tmp)
    return start

def Dijkstra(start, graph):
    """ 迪杰斯特拉算法
        start: 起点 int start
        graph: 地图 graph{}
        返回值: dict path_graph{}
               dict path_dict{}
    """
    INF = 999999  # INF
    length = len(graph)
    path_graph = {k:INF for k in graph.keys()}
    already_traversal = set()
    path_graph[start] = 0
    min_node = start#初始化最小权值点
    already_traversal.add(min_node)#把找到的最小节点添加进去
    path_parent = {k:start for k in graph.keys()}
    path_dict = {}
    while(len(already_traversal) <= length):
        p = min_node
        key = min_node
        #path_dict = {}
        if p != start:
            path = []
            path.append(p)
            while (path_parent[p] != start):#找该节点的父节点添加到path，直到父节点是start
                path.append(path_parent[p])
                p = path_parent[p]
                value = p
            path.append(start)
            path.reverse()#反序
            path_dict[key] = path
        if(len(already_traversal) == length):
            break
        for k in path_graph.keys():#更新距离
            if k not in already_traversal:
                if  k in graph[min_node].keys() and (path_graph[min_node]+graph[min_node][k][0]) < path_graph[k]:
                    path_graph[k] = path_graph[min_node]+graph[min_node][k][0]
                    path_parent[k] = min_node
        min_value = INF
        for k in path_graph.keys():#找最小节点
            if k not in already_traversal:
                if path_graph[k] < min_value:
                    min_node = k
                    min_value = path_graph[k]
        already_traversal.add(min_node)#把找到最小节点添加进去
    return path_graph, path_dict          

# ==============================================================
#                待修正
# ==============================================================

def get_answer(cars,roads, cross, starts, car_speeds):
    """ 通过出发点和终点匹配每辆车的路径
        cars: 车辆信息 cars{}
        starts: 出发点集合 set() starts
        graph: 地图信息 graph{}
        返回值: list sorted_answer[]
               dict graph{}
    """
    answer = []
    graph = {}
    for car_speed in car_speeds:
        graph = build_graph(roads, cross, car_speed)
        # 根据answer更新地图
        for ans in answer:
            update_graph(ans['path'], graph)

        for start in starts:
            path_graph, path_dict = Dijkstra(start, graph)
            for key in cars:
                if cars[key]['speed'] == car_speed and cars[key]['from'] == start:
                    for i in path_dict.keys():
                        if cars[key]['to'] == i:
                            cost = get_cost(roads, path_dict[i], graph, car_speed)
                            line = {'car_id': key, 'time': cars[key]['time'], 'path': path_dict[i], 'cost': cost, 'speed': car_speed}
                            # 在此处修改权值
                            update_graph(line['path'], graph)
                            answer.append(line)
                            break
    # 对车辆进行多级排序，先按照cost，再按照time
    sorted_answer =  sorted(answer, key = lambda s: (s['cost'], s['time']))
    return sorted_answer, graph

# ==============================================================
#                确定车辆出发时间
# ==============================================================

def schedule(sorted_answer):
    """ 修改车辆出发时间
        sorted_answer: 车辆规划信息 sorted_answer{}
        返回值: list answer_list[]
    """
    cnt = 0
    answer_time = sorted_answer
    interval = config.get_interval()
    delay = config.get_delay()
    i = config.get_start_time()
    for answer in answer_time:  
        if answer['time'] > i:
            continue
        answer['time'] = i
        cnt = cnt + 1
        if cnt % interval == 0:
            i = i + delay
    return answer_time

# ==============================================================
#         用以主函数调用
# ==============================================================

def process(cars, roads, cross):
    """ 计算获取answer结果集
        cars: 车辆信息
        roads: 道路信息
        cross: 路口信息
    """
    # 获取出发点
    starts = get_start(cars)
    car_speeds = get_speed(cars)
    # 获取按时间排序后的结果集以及地图
    sorted_answer, graph = get_answer(cars,roads, cross, starts, car_speeds)
    # 对结果集的时间进行修改
    answer_time = schedule(sorted_answer)
    # 将结果集转化为字符串，便于写入
    answer_str = answer2str(answer_time, graph)
    return answer_str

    
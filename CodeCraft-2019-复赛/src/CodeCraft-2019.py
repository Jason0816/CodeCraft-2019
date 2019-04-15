# -*- coding: utf-8 -*-
import sys
from file_io import read_input, output_answer
from car_process import process, road_to_cross

# ==============================================================
#         主函数
# ==============================================================
def main():
    if len(sys.argv) != 6:
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    preset_answer_path = sys.argv[4]
    answer_path = sys.argv[5]

# to read input file
    cars, roads, cross, preset_answer = read_input(car_path, road_path, cross_path, preset_answer_path)
# process
    answer = process(cars, roads, cross, preset_answer)
    # print(answer)
# to write output file
    output_answer(answer_path, answer)

if __name__ == "__main__":
    main()


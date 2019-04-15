# -*- coding: utf-8 -*-
import sys
from file_io import read_input, output_answer
from car_process import process

# ==============================================================
#         主函数
# ==============================================================
def main():
    if len(sys.argv) != 5:
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]
# to read input file
    cars, roads, cross = read_input(car_path, road_path, cross_path)
# process
    answer = process(cars, roads, cross)
    # print(answer)
# to write output file
    output_answer(answer_path, answer)

if __name__ == "__main__":
    main()


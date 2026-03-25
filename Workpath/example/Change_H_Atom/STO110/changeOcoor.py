# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 09:28:02 2024

@author: chen
"""

import numpy as np

# 生成坐标序列
def generate_coordinates(x0, y0, z0, x_change=None, y_change=None, z_change=None):
    if x_change is not None:
        x_change = np.atleast_2d(x_change)
        for i in x_change:
            x_step, x_delta = i[0], i[1]
        x_range = np.arange(x0 - x_delta, x0 + x_delta + x_step, x_step)
    else:
        x_range = [x0]

    if y_change is not None:
        y_change = np.atleast_2d(y_change)
        for i in y_change:
            y_step, y_delta = i[0], i[1]
        y_range = np.arange(y0 - y_delta, y0 + y_delta + y_step, y_step)
    else:
        y_range = [y0]

    if z_change is not None:
        z_change = np.atleast_2d(z_change)
        for i in z_change:
            z_step, z_delta = i[0], i[1]
        z_range = np.arange(z0 - z_delta, z0 + z_delta + z_step, z_step)
    else:
        z_range = [z0]

    # 生成坐标组合
    coordinates = [(round(float(x), 5), round(float(y), 5), round(float(z), 5))
                   for x in x_range for y in y_range for z in z_range]
    return coordinates

# 替换并保存文件
def replace_and_save_files(coordinates1, coordinates2, input_file, output_prefix):
    idx = 1
    num_digits = len(str(len(coordinates1) * len(coordinates2)+1))
    print(num_digits)
    
    for x1, y1, z1 in coordinates1:
        for x2, y2, z2 in coordinates2:
            # 替换内容，使用两组坐标
            new_line_18 = f" O    {x1:.6f}  {y1:.6f}  {z1:.6f}  1.000000  0.013000  0.100000  0.100000  0.100000"  #修改cel文件中第18行的数据
            new_line_20 = f" O    {x2:.6f}  {y2:.6f}  {z2:.6f}  1.000000  0.013000  0.100000  0.100000  0.100000"  #
            new_line_11 = f" O    {(x1+0.5):.6f}  {(y1+0.5):.6f}  {(z1-0.5):.6f}  1.000000  0.013000  0.100000  0.100000  0.100000" #
            new_line_12 = f" O    {(x1+0.5):.6f}  {(y1):.6f}   {z1:.6f}  1.000000  0.013000  0.100000  0.100000  0.100000" #
            new_line_17 = f" O    {x1:.6f}  {(y1+0.5):.6f}  {(z1-0.5):.6f}  1.000000  0.013000  0.100000  0.100000  0.100000" #
            new_line_13 = f" O    {(x2+0.5):.6f}  {(y2+0.5):.6f}  {(z2+0.5):.6f}  1.000000  0.013000  0.100000  0.100000  0.100000" #
            new_line_14 = f" O    {(x2+0.5):.6f}  {y2:.6f}  {z2:.6f}  1.000000  0.013000  0.100000  0.100000  0.100000" #
            new_line_19 = f" O    {x2:.6f}  {(y2+0.5):.6f} {(z2+0.5):.6f}  1.000000  0.013000  0.100000  0.100000  0.100000" #
            

            
            output_filename = f"./cel/{output_prefix}_{idx:0{num_digits}d}.cel"
            idx += 1
            
            replace_single_line_in_file(input_file, 18, new_line_18, output_filename)
            replace_single_line_in_file(output_filename, 20, new_line_20, output_filename)
            replace_single_line_in_file(output_filename, 11, new_line_11, output_filename)
            replace_single_line_in_file(output_filename, 12, new_line_12, output_filename)
            replace_single_line_in_file(output_filename, 17, new_line_17, output_filename)
            replace_single_line_in_file(output_filename, 13, new_line_13, output_filename)
            replace_single_line_in_file(output_filename, 14, new_line_14, output_filename)
            replace_single_line_in_file(output_filename, 19, new_line_19, output_filename)
            
            print(f"Saved: {output_filename}")


def replace_single_line_in_file(file_path, line_number, new_line, new_path):
    # 打开文件并读取所有行
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # 替换指定行的内容
    if line_number <= len(lines):
        lines[line_number - 1] = new_line + '\n'
    else:
        print("行号超出文件总行数！")

    # 将修改后的行写回文件
    with open(new_path, 'w') as file:
        file.writelines(lines)


# 主程序：根据两个原始坐标生成坐标并替换文件
def process_coordinates_for_two_points(coords1, coords2, input_file):
    x0_1, y0_1, z0_1 = coords1
    x0_2, y0_2, z0_2 = coords2

    # 自定义范围和步长（可以根据需要调整）
    x_change = [[0.01, 0.02]]  # [步长, 范围]
    y_change = [[0.01, 0.02]]
    z_change = [[0.01, 0.02]]

    # 生成两组坐标
    coordinates1 = generate_coordinates(x0_1, y0_1, z0_1, x_change, y_change,z_change)
    coordinates2 = generate_coordinates(x0_2, y0_2, z0_2, x_change, y_change,z_change)

    # 替换并保存文件
    replace_and_save_files(coordinates1, coordinates2, input_file, "STO_110_Output")


 




# 示例输入
input_file = 'STOR-3C110H071.cel'
coords1 = (0.234100,  0.244800,  0.750000)
coords2 = (0.224100,  0.259800,  0.250000)

# 执行程序
process_coordinates_for_two_points(coords1, coords2, input_file)

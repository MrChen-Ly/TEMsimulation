# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:19:05 2024

@author: chen
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def extract_line_profile(image, start, end):
    """
    提取图像从起点到终点的line profile
    :param image: 图像数据（numpy数组）
    :param start: 起点坐标 (x0, y0)
    :param end: 终点坐标 (x1, y1)
    :return: Line profile 数据
    """
    # 使用直线插值获取所有点坐标
    x0, y0 = start
    x1, y1 = end
    num_points = int(np.hypot(x1 - x0, y1 - y0))  # 计算点数
    x_coords = np.linspace(x0, x1, num_points).astype(np.int32)
    y_coords = np.linspace(y0, y1, num_points).astype(np.int32)

    # 获取线上的像素值
    line_profile = image[y_coords, x_coords]
    return line_profile


def process_folder(folder_path, start, end, output_plot_path):
    """
    遍历文件夹中的所有图像文件，生成叠加折线图
    :param folder_path: 文件夹路径
    :param start: 起点坐标 (x0, y0)
    :param end: 终点坐标 (x1, y1)
    :param output_plot_path: 输出折线图路径
    """
    plt.figure(figsize=(10, 6))  # 创建绘图窗口
    plt.title("Line Profiles from All Images")
    plt.xlabel("Distance Along Line")
    plt.ylabel("Pixel Intensity")
    
    # 遍历文件夹中的所有图像文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
            # 读取图像
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                print(f"无法读取图像文件: {filename}")
                continue

            # 提取line profile
            line_profile = extract_line_profile(image, start, end)

            # 绘制折线图
            plt.plot(line_profile, label=filename)

    # 添加图例
    plt.legend(loc="upper right", fontsize='small', bbox_to_anchor=(1.3, 1))
    plt.tight_layout(rect=[0, 0, 0.8, 1])  # 为图例预留空间

    # 保存结果
    plt.savefig(output_plot_path)
    plt.show()
    print(f"折线图已保存到: {output_plot_path}")


# 示例使用
if __name__ == "__main__":
    folder_path = "./image_result"  # 图像文件夹路径
    start_point = (15, 154)  # 起点坐标
    end_point = (49, 122)  # 终点坐标
    output_plot_path = "./line_profiles.png"  # 输出折线图路径

    process_folder(folder_path, start_point, end_point, output_plot_path)

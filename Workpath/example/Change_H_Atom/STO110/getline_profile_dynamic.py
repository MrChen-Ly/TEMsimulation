# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:59:50 2024

@author: chen
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import mplcursors

def extract_line_profile(image, start, end):
    """
    提取图像从起点到终点的line profile
    :param image: 图像数据（numpy数组）
    :param start: 起点坐标 (x0, y0)
    :param end: 终点坐标 (x1, y1)
    :return: Line profile 数据
    """
    x0, y0 = start
    x1, y1 = end
    num_points = int(np.hypot(x1 - x0, y1 - y0))  # 计算点数
    x_coords = np.linspace(x0, x1, num_points).astype(np.int32)
    y_coords = np.linspace(y0, y1, num_points).astype(np.int32)
    line_profile = image[y_coords, x_coords]
    return line_profile

def process_folder(folder_path, start, end):
    """
    遍历文件夹中的所有图像文件，生成交互式折线图
    :param folder_path: 文件夹路径
    :param start: 起点坐标 (x0, y0)
    :param end: 终点坐标 (x1, y1)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.title("Line Profiles from All Images")
    plt.xlabel("Distance Along Line")
    plt.ylabel("Pixel Intensity")

    # 数据存储
    profiles = []
    labels = []

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

            # 绘制折线图并保存句柄
            line, = ax.plot(line_profile, label=filename)
            profiles.append(line)
            labels.append(filename)

    # 添加图例并支持交互
    legend = ax.legend(loc="upper right", fontsize='small', bbox_to_anchor=(1.3, 1))
    legend.set_draggable(True)

    # 启用mplcursors交互功能
    cursor = mplcursors.cursor(profiles, hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(labels[profiles.index(sel.artist)]))



    plt.tight_layout(rect=[0, 0, 0.8, 1])  # 为图例和按钮预留空间
    plt.show()

# 示例使用
if __name__ == "__main__":
    folder_path = "./image_result"  # 图像文件夹路径
    start_point = (15, 154)  # 起点坐标
    end_point = (49, 122)  
    process_folder(folder_path, start_point, end_point)
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 12:03:28 2024

@author: chen
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:39:01 2024

@author: chen
"""
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from scipy.optimize import curve_fit

# 高斯函数
def gaussian_2d(x, y, x0, y0, sigma_x, sigma_y, amplitude, offset):
    return offset + amplitude * np.exp(
        -((x - x0)**2 / (2 * sigma_x**2) + (y - y0)**2 / (2 * sigma_y**2))
    )

# 高斯拟合
def fit_gaussian_2d(data, center, radius):
    y, x = np.indices(data.shape)
    x0, y0 = center
    mask = (x - x0)**2 + (y - y0)**2 <= radius**2
    x_masked = x[mask]
    y_masked = y[mask]
    data_masked = data[mask]
    
    initial_guess = (x0, y0, 1, 1, np.max(data_masked), np.min(data_masked))
    popt, _ = curve_fit(lambda xy, x0, y0, sigma_x, sigma_y, amplitude, offset: 
                           gaussian_2d(xy[0], xy[1], x0, y0, sigma_x, sigma_y, amplitude, offset),
                           (x_masked, y_masked), data_masked, p0=initial_guess,maxfev=10000 )
        
    return popt
def circular_region_integral(array, center, radius):
    x_center, y_center = center
    y, x = np.ogrid[:array.shape[0], :array.shape[1]]
    mask = (x - x_center)**2 + (y - y_center)**2 <= radius**2
    return np.sum(array[mask])#sum
# 计算积分面积
def intensityscore(simulated_image,center,r):
    # 读取HRTEM图像

    # 图像预处理：高斯模糊去噪
    array = filters.gaussian(simulated_image, sigma=1)
    
    # 指定圆心和半径
    
    radius = r

    # 对指定圆形区域进行高斯拟合
    popt = fit_gaussian_2d(array, center, radius)
    x0, y0, sigma_x, sigma_y, amplitude, offset = popt
    #print(f"高斯分布拟合中心: ({x0}, {y0})")

    # 调整后的中心点
    adjusted_center = (x0, y0)
    xo=(x0-38.711)*0.0042636*1000
    yo=(y0-80.540)*0.0042636*1000
    # 计算调整后中心点的圆形区域的积分强度
    integral_intensity = circular_region_integral(array, adjusted_center, radius)#/np.mean(array)
    print(f'{x0}, {y0}', integral_intensity,'')
    return integral_intensity,xo,yo
# 读取图片
def read_binary_file(file_path, height, width):
    image_data = np.fromfile(file_path, dtype=np.float32)
    return image_data.reshape((height, width))

# 绘制热图
def plot_heatmap(coordinates, values, title="Heatmap",labelname="Distance (pm)"):
    x_coords = sorted(set(coord[0] for coord in coordinates))
    y_coords = sorted(set(coord[1] for coord in coordinates))
    heatmap = np.zeros((len(y_coords), len(x_coords)))
    
    coord_to_value = {coord: value for coord, value in zip(coordinates, values)}
    for i, y in enumerate(y_coords):
        for j, x in enumerate(x_coords):
            heatmap[i, j] = coord_to_value.get((x, y), np.nan)
    
    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap, cmap='coolwarm', origin='lower', 
               extent=[min(x_coords), max(x_coords), min(y_coords), max(y_coords)])
    plt.colorbar(label=labelname)
    plt.title(title)
    plt.xlabel("X Coordinate ")
    plt.ylabel("Y Coordinate ")
    plt.show()

# 主程序
def process_images(data_folder, coordinates, image_shape, center, radius):
    for i in range(12):
        #image = read_binary_file(file_path, *image_shape)#.dat
        image = cv2.imread(r"E:\RunTemp\Drprobe\img\SrTiO_change_Hcoor\STO110\image_result\Up_roi_single.jpg", cv2.IMREAD_GRAYSCALE)
        integral_area,xo,yo =intensityscore(image, center[i], radius)
        
# 示例参数
data_folder = "./image_result"  # 图片存储文件夹
image_shape = (200, 200)  # 图片的宽和高
center = [(55.559174,16.414219),
(53.379089,114.04405),
(58.580101,201.12642),
(60.582756,291.35684),
(119.10729,16.787672),
(121.74889,109.50634),
(121.74067,198.90376),
(120.92617,285.9017),
(183.05359,20.917124),
(183.16995,110.69762),
(184.14612,192.18076),
(184.95213,290.04474)
] # 圆心位置
radius = 7  # 半径
x_delta=0.08
x_step=0.02
x_range = np.arange(0.297500 - x_delta, 0.297500 + x_delta + x_step, x_step)
y_range = np.arange(0.461300 - x_delta, 0.461300 + x_delta + x_step, x_step)
coordinates = [(round(float(x), 5), round(float(y), 5))
                   for x in x_range for y in y_range]

# 运行程序
process_images(data_folder, coordinates, image_shape, center, radius)

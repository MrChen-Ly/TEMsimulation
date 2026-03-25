import itertools
import math
import subprocess
import tifffile as tiff
import numpy as np
import os
import tkinter as tk
from tkinter import ttk
from tkinter import  filedialog, simpledialog

global workingDir, slcname,heightval,widthval
# Define global variables
slcname = ""
heightval = 0
widthval = 0
workingDir = ""





def batch_export_to_tiff(input_folder, output_folder, height, width):
    # 获取选中的文件夹中的所有二进制文件
    file_paths = [os.path.join(input_folder, filename) for filename in os.listdir(input_folder) if filename.endswith('.dat')]
    
    for file_path in file_paths:         
        # 导出为tif文件
        export_to_tiff(file_path, height, width, output_folder)
def runbatfile(batch_file_path):
    import subprocess
    try:
        # 使用subprocess.run运行批处理文件，并显示cmd窗口
        result = subprocess.run(batch_file_path, shell=True, check=True,  stdout=subprocess.PIPE, text=True)
        
        # 输出批处理文件的结果
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"运行批处理文件时发生错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")

def replace_lines(file_path, start_line, end_line, new_content,newpath):
    with open(file_path, 'r') as file:
        lines = file.readlines()   
    if start_line <= len(lines) :
        lines[start_line-1:end_line-1] = new_content 
    with open(newpath, 'w') as file:
        file.writelines(lines)
def replace_single_line_in_file(file_path, line_number, new_line,new_path):
    # 打开文件并读取所有行
    with open(file_path, 'r') as file:
        lines = file.readlines()  
    # 替换指定行的内容
    if line_number <= len(lines):
        lines[line_number-1] = new_line + '\n'
        #print('%d:%s' %(line_number - 1,new_line))
    else:
        print("行号超出文件总行数！")

    # 将修改后的行写回文件
    with open(new_path, 'w') as file:
        file.writelines(lines)
    file.close()
def polar_to_cartesian(r, theta):
    # 将角度转换为弧度
    theta_rad = math.radians(theta)
    # 计算笛卡尔坐标值
    x =round(r * math.cos(theta_rad),6)
    y = round(r * math.sin(theta_rad),6)
    return x, y
# 模拟函数
def read_binary_file(file_path, height, width):
    # 从二进制文件读取数据
    image_data = np.fromfile(file_path, dtype=np.float32)
    # 将一维数组转换为二维数组
    image_shape = (height, width)
    image_data = image_data.reshape(image_shape)
    
    # 如果图像尺寸大于512x512，则仅选择512x512的部分
    if height > 512:
        start_row = (height - 512) // 2
        end_row = start_row + 512
        if width > 512:
            start_col = (width - 512) // 2
            end_col = start_col + 512
            image_data = image_data[start_row:end_row, start_col:end_col]
        else:
            image_data = image_data[start_row:end_row, :]
    else:
        if width > 512:
            start_col = (width - 512) // 2
            end_col = start_col + 512
            image_data = image_data[:, start_col:end_col]
    
    return image_data

def export_to_tiff(file_path, height, width, output_folder):
    # 读取二进制文件
    image_data = read_binary_file(file_path, height, width)
    # 构造输出文件路径
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = os.path.join(output_folder, f"{file_name}.tif")
    
    # 保存为tif文件
    tiff.imsave(output_path, image_data)
    #print(f"导出成功: {output_path}")

def runwav(Tilt, Tilta, Cs, Df, Tk, A1, A1a, A2, A2a, B2, B2a, Sod):
    
    # 构建命令字符串
    cmd_command = f'cd /d {workingDir} && wavimg -prm prm\\wavimg_{slcname}.prm /nli' 
    print(f'cd /d {workingDir} && wavimg -prm prm\\wavimg_{slcname}.prm /nli' )
    # 在cmd中运行命令
    output = subprocess.check_output(cmd_command, shell=True, encoding="utf-8")
    print(output) 
    file_path =f'img\\dat\\%s_Tilt_{Tilt}_Tilta_{Tilta}_Cs_{Cs}_Df_{Df}_Tk_{Tk}_A1_{A1}_A1a_{A1a}_A2_{A2}_A2a_{A2a}_B2_{B2}_B2a_{B2a}_Sod_{Sod}_map.dat'% (slcname) # 新的行内容
    export_to_tiff(workingDir+file_path,heightval, widthval,workingDir+'img\\tif')
# 模拟函数
def sim_function(workingDir,slcname,Tilt, Tilta, Cs, Df, Tk, A1, A1a, A2, A2a, B2, B2a, Sod,no):
    # 在这里编写你的函数逻辑
    #Thickness
    TkV=round(Tk/(0.09758))
    
    #print(TkV)
    file_path = workingDir+'prm\\wavimg_%s.prm'%slcname  # 替换目标文件路径
    line_number = 1 # 要替换的行号
    new_line = '\'wav\\%s_sl%03d.wav\'' %(slcname,TkV) # 新的行内容
    newpath= workingDir+'prm\\wavimg_%s.prm' %slcname
    replace_single_line_in_file(file_path, line_number, new_line, newpath)
    #14
    file_path = workingDir+'prm\\wavimg_%s.prm'%slcname  # 替换目标文件路径
    line_number = 14 # 要替换的行号
    new_line = '1,%f' %Sod # 新的行内容
    newpath= workingDir+'prm\\wavimg_%s.prm' %slcname
    replace_single_line_in_file(file_path, line_number, new_line, newpath)
    #ab
    A1x,A1y=polar_to_cartesian(A1,A1a)
    A2x,A2y=polar_to_cartesian(A2,A2a)
    B2x,B2y=polar_to_cartesian(B2,B2a)
    Cs=Cs*1000
    file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
    line_number = 18  # 要替换的行号
    new_line = '10\n'+'0.0 0.0 0.0 0.0\n'+'1, %0.1f'%Df+', 0.\n'+'2, %0.1f,%0.1f 0.\n'%(A1x,A1y)+'3, %0.1f, %0.1f 0.0\n' %(B2x,B2y)+'4, %0.1f, %0.1f 0.0\n'%(A2x,A2y) +'5, %0.1f, 0.\n'%Cs+'6.0 0.0 0.0 0.0\n'+'7.0 0.0 0.0 0.0\n'+'8.0 0.0 0.0 0.0\n'+'9.0 0.0 0.0 0.0\n' # 新的行内容
    newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
    endline= 29
    replace_lines(file_path, line_number, endline,new_line, newpath)
    file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
    line_number = 6  # 要替换的行号
    new_line =f'img\\dat\\%s_{no}.dat'% (slcname) # 新的行内容
    newpath= workingDir+'prm\\wavimg_%s_%d.prm' % (slcname,no)  #新地址
    replace_single_line_in_file(file_path, line_number, new_line, newpath)
     
    
    #runwav(Tilt, Tilta, Cs, Df, Tk, A1, A1a, A2, A2a, B2, B2a, Sod)
#tilt替换函数
def msachange(workingDir,slcname,tilt,tilta):
    tilt=tilt*(0.18/math.pi)
    tiltx,tilty=polar_to_cartesian(tilt,tilta)
    file_path = workingDir+'prm\\msa_%s.prm'%slcname  # 替换目标文件路径
    line_number = 13  # 要替换的行号
    new_line =  '%f' %tiltx # 新的行内容
    newpath=workingDir+'prm\\msa_%s.prm'%slcname
    replace_single_line_in_file(file_path, line_number, new_line,newpath)
    
    file_path=workingDir+'prm\\msa_%s.prm'%slcname
    line_number = 14  # 要替换的行号
    new_line =  '%f' %tilty  # 新的行内容
    replace_single_line_in_file(file_path, line_number, new_line,newpath)
def runmsa(workingDir,slcname):
    # 替换%s的值
    prm_file = f'{slcname}'
    
    # 构建命令字符串
    cmd_command = f'cd /d {workingDir} && msa -prm prm\\msa_{prm_file}.prm -out wav\\{prm_file} /ctem'
    # 在cmd中运行命令
    output = subprocess.check_output(cmd_command, shell=True, encoding="utf-8")
    print(output)    
   
def create_folder(folder_path):
    """
    确认并新建指定文件夹

    参数：
    folder_path (str): 要创建的文件夹路径

    返回：
    bool: 如果成功创建了文件夹，则返回True；如果文件夹已存在或创建失败，则返回False。
    """
    # 检查文件夹是否已存在
    if os.path.exists(folder_path):
        print(f"文件夹 '{folder_path}' 已存在。")
        return False

    try:
        # 创建文件夹
        os.makedirs(folder_path)
        print(f"文件夹 '{folder_path}' 创建成功。")
        return True
    except OSError as e:
        print(f"创建文件夹 '{folder_path}' 失败：{e}")
        return False    
def copy_text_file(source_file, destination_file):
    """
    将源文本文件复制到目标文件路径。

    参数：
    source_file (str): 源文件的路径。
    destination_file (str): 目标文件的路径。

    返回：
    bool: 如果成功复制文件，则返回True；否则返回False。
    """
    try:
        with open(source_file, 'r') as source:
            with open(destination_file, 'w') as destination:
                for line in source:
                    destination.write(line)
        print(f"文本文件 '{source_file}' 已成功复制到 '{destination_file}'。")
        return True
    except Exception as e:
        print(f"复制文本文件 '{source_file}' 到 '{destination_file}' 失败：{e}")
        return False
def clear_folder(folder_path):
    """
    清空指定文件夹中的所有文件和子文件夹。

    参数：
    folder_path (str): 要清空的文件夹路径。

    返回：
    无。
    """
    try:
        # 遍历文件夹中的所有文件和子文件夹
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            # 如果是文件则删除
            if os.path.isfile(file_path):
                os.remove(file_path)
            # 如果是文件夹则递归调用清空文件夹函数
            elif os.path.isdir(file_path):
                clear_folder(file_path)
        print(f"文件夹 '{folder_path}' 已成功清空。")
    except Exception as e:
        print(f"清空文件夹 '{folder_path}' 失败：{e}")
def rangetodata(data_st, data_end, data_step):
     data = []
     num = round((data_end - data_st) / data_step)
     num=num+1
     for i in range(num):
         val = data_st + data_step * i
         data.append(val)  # Append a new list containing val
     return data
def get_parameter_ranges():
    # Define global variables for parameter ranges
     Cs_range = [-15.0, -14.5, -14.0, -13.5, -13.0, -12.5, -12.0, -11.5, -11.0, -10.5, -10.0, -9.5, -9.0, -8.5, -8.0, -7.5, -7.0, -6.5, -6.0, -5.5, -5.0, -4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.0]
     Df_range = [0.0, 2.0, 4.0, 6.0, 8.0]
     Tk_range = [2.0, 4.0, 6.0]
     Tilt_range = [0.0]
     Tilta_range = [0.0]
     A1_range = [0.0]
     A1a_range = [0.0]
     A2_range = [0.0]
     A2a_range = [0.0]
     B2_range = [0.0]
     B2a_range = [0.0]
     Sod_range = [3.0]
 
     folder_path = 'H:\\DrProbe\\SrTiO'#filedialog.askdirectory(title="select a folder path")
     if folder_path:
         new_folder_name = simpledialog.askstring("input", "inputcif name：", initialvalue="NewFolder")
         x =180#simpledialog.askstring("input", "x：")
         y =90# simpledialog.askstring("input", "y：")
     else:
         exit(0)
     print(folder_path)
     print(new_folder_name)
     
     
     slcname= new_folder_name
     workingDir =folder_path+'/'
     
     heightval=int(y)
     widthval=int(x)

     # Cs range
     cs_start = float(cs_start_entry.get())
     cs_end = float(cs_end_entry.get())
     cs_step = float(cs_step_entry.get())
     Cs_range = rangetodata(cs_start, cs_end , cs_step)
     
     # Df range
     df_start = float(df_start_entry.get())
     df_end = float(df_end_entry.get())
     df_step = float(df_step_entry.get())
     Df_range = rangetodata(df_start, df_end, df_step)
     
     # Tk range
     tk_start = float(tk_start_entry.get())
     tk_end = float(tk_end_entry.get())
     tk_step = float(tk_step_entry.get())
     Tk_range = rangetodata(tk_start, tk_end , tk_step)
     
     # Tilt range
     tilt_start = float(tilt_start_entry.get())
     tilt_end = float(tilt_end_entry.get())
     tilt_step = float(tilt_step_entry.get())
     Tilt_range = rangetodata(tilt_start, tilt_end , tilt_step)
     
     # Tilta range
     Tilta_range =rangetodata(float(tilta_start_entry.get()), float(tilta_end_entry.get()) , float(tilta_step_entry.get()))
     
     # A1 range
     a1_start = float(a1_start_entry.get())
     a1_end = float(a1_end_entry.get())
     a1_step = float(a1_step_entry.get())
     A1_range = rangetodata(a1_start, a1_end, a1_step)
     
     # A1a range
     A1a_range = rangetodata(float(a1a_start_entry.get()), float(a1a_end_entry.get()) , float(a1a_step_entry.get()))
     
     # A2 range
     a2_start = float(a2_start_entry.get())
     a2_end = float(a2_end_entry.get())
     a2_step = float(a2_step_entry.get())
     A2_range = rangetodata(a2_start, a2_end , a2_step)
     
     # A2a range
     A2a_range = rangetodata(float(a2a_start_entry.get()),float(a2a_end_entry.get()) , float(a2a_step_entry.get()))
     
     # B2 range
     b2_start = float(b2_start_entry.get())
     b2_end = float(b2_end_entry.get())
     b2_step = float(b2_step_entry.get())
     B2_range = rangetodata(b2_start, b2_end , b2_step)
     
     # B2a range
     B2a_range = rangetodata(float(b2a_start_entry.get()), float(b2a_end_entry.get()) , float(b2a_step_entry.get()))
     
     # Sod range
     Sod_range = rangetodata(float(sod_start_entry.get()), float(sod_end_entry.get()), float(b2a_step_entry.get()))


     print("Cs_range:", Cs_range)
     print("Df_range:", Df_range)
     print("Tk_range:", Tk_range)
     print("Tilt_range:", Tilt_range)
     print("Tilta_range:", Tilta_range)
     print("A1_range:", A1_range)
     print("A1a_range:", A1a_range)
     print("A2_range:", A2_range)
     print("A2a_range:", A2a_range)
     print("B2_range:", B2_range)
     print("B2a_range:", B2a_range)
     print("Sod_range:", Sod_range)
     
      # 统计参数范围的数量
     Cs_count = len(Cs_range)
     Df_count = len(Df_range)
     Tk_count = len(Tk_range)
     Tilt_count = len(Tilt_range)
     Tilta_count = len(Tilta_range)
     A1_count = len(A1_range)
     A1a_count = len(A1a_range)
     A2_count = len(A2_range)
     A2a_count = len(A2a_range)
     B2_count = len(B2_range)
     B2a_count = len(B2a_range)
     Sod_count = len(Sod_range)

      # 计算所有参数范围的总和
     total_count = (
          len(Cs_range) * len(Df_range) * len(Tk_range) * len(Tilt_range)*
          len(Tilta_range) * len(A1_range) * len(A1a_range) * len(A2_range) *
          len(A2a_range) * len(B2_range) *len(B2a_range) * len(Sod_range)
      )

      # 打印总和
     print("所有参数范围的总和:", total_count)
     
     # 使用嵌套循环执行函数操作
     for tilt_combination in itertools.product(Tilt_range, Tilta_range):
         tilt, tilta = tilt_combination
         #print(tilt, tilta)
         msachange(workingDir,slcname,tilt,tilta)#执行替换函数替换msa文件中的tilt参数
         runmsa(workingDir,slcname)
         #新建一个bat文件
         for Cs_value in Cs_range:
             for Df_value in Df_range:
                 no=0
                 
                 for combination in itertools.product([Cs_value], [Df_value], Tk_range, A1_range, A1a_range, A2_range, A2a_range, B2_range, B2a_range, Sod_range):
                     #start_time = time.time()
                     print([Df_value])
                     print(combination)
                     sim_function(workingDir,slcname,tilt, tilta, *combination,no)
                     no=no+1
                     #end_time = time.time()
                     #execution_time = end_time - start_time
                     #print(f"代码执行时间: {execution_time} 秒")
                 #添加wavimg指令行并运行bat文件
                 string=workingDir[0:len(workingDir)-1]
                 runPrmFileBat = open(workingDir + 'img\\runPrm.bat', 'w')
                 runPrmFileBat.write(r'cd %s'%string)
                 
                 for i in range (no):
                     runPrmFileBat.write('\nwavimg -prm prm\\wavimg_%s_%d.prm /nli'% (slcname,i))
                 runPrmFileBat.close()
                 runbatfile(workingDir + 'img\\runPrm.bat')
                 # 使用 filedialog 选择文件夹
                 input_folder = 'H:\\DrProbe\\SrTiO\\img\\dat'#filedialog.askdirectory(title="dat save path")
                 output_folder =os.path.join('H:\\DrProbe\\SrTiO\\img','%s_tkloop\\Cs_%s\\df_%s'%(slcname,Cs_value,Df_value)) #filedialog.askdirectory(title="tif save path")
                 create_folder(output_folder)
                 # 调用函数
                 batch_export_to_tiff(input_folder, output_folder,heightval, widthval)
                 source_file = "H:\\DrProbe\\SrTiO\\prm\\wavimg_%s_0.prm"%slcname
                 destination_file = os.path.join(output_folder,"wavimg_%s_0.prm"%slcname)
                 copy_text_file(source_file, destination_file)
                 clear_folder('H:\\DrProbe\\SrTiO\\img\\dat')

root = tk.Tk()   # 
root.title("Parameter Ranges")

 # Cs range
cs_label = ttk.Label(root, text="Cs Range:")
cs_label.grid(row=0, column=0, sticky="w")
cs_start_entry = ttk.Entry(root, width=5)
cs_start_entry.grid(row=0, column=1)
cs_end_entry = ttk.Entry(root, width=5)
cs_end_entry.grid(row=0, column=2)
cs_step_entry = ttk.Entry(root, width=5)
cs_step_entry.grid(row=0, column=3)

 # Df range
df_label = ttk.Label(root, text="Df Range:")
df_label.grid(row=1, column=0, sticky="w")
df_start_entry = ttk.Entry(root, width=5)
df_start_entry.grid(row=1, column=1)
df_end_entry = ttk.Entry(root, width=5)
df_end_entry.grid(row=1, column=2)
df_step_entry = ttk.Entry(root, width=5)
df_step_entry.grid(row=1, column=3)

 # Tk range
tk_label = ttk.Label(root, text="Tk Range:")
tk_label.grid(row=2, column=0, sticky="w")
tk_start_entry = ttk.Entry(root, width=5)
tk_start_entry.grid(row=2, column=1)
tk_end_entry = ttk.Entry(root, width=5)
tk_end_entry.grid(row=2, column=2)
tk_step_entry = ttk.Entry(root, width=5)
tk_step_entry.grid(row=2, column=3)

 # Tilt range
tilt_label = ttk.Label(root, text="Tilt Range:")
tilt_label.grid(row=3, column=0, sticky="w")
tilt_start_entry = ttk.Entry(root, width=5)
tilt_start_entry.grid(row=3, column=1)
tilt_end_entry = ttk.Entry(root, width=5)
tilt_end_entry.grid(row=3, column=2)
tilt_step_entry = ttk.Entry(root, width=5)
tilt_step_entry.grid(row=3, column=3)
 # Tilta range
tilta_label = ttk.Label(root, text="Tilta Range:")
tilta_label.grid(row=4, column=0, sticky="w")
tilta_start_entry = ttk.Entry(root, width=5)
tilta_start_entry.grid(row=4, column=1)
tilta_end_entry = ttk.Entry(root, width=5)
tilta_end_entry.grid(row=4, column=2)
tilta_step_entry = ttk.Entry(root, width=5)
tilta_step_entry.grid(row=4, column=3)

 # A1 range
a1_label = ttk.Label(root, text="A1 Range:")
a1_label.grid(row=5, column=0, sticky="w")
a1_start_entry = ttk.Entry(root, width=5)
a1_start_entry.grid(row=5, column=1)
a1_end_entry = ttk.Entry(root, width=5)
a1_end_entry.grid(row=5, column=2)
a1_step_entry = ttk.Entry(root, width=5)
a1_step_entry.grid(row=5, column=3)
 # A1a range
a1a_label = ttk.Label(root, text="A1a Range:")
a1a_label.grid(row=6, column=0, sticky="w")
a1a_start_entry = ttk.Entry(root, width=5)
a1a_start_entry.grid(row=6, column=1)
a1a_end_entry = ttk.Entry(root, width=5)
a1a_end_entry.grid(row=6, column=2)
a1a_step_entry = ttk.Entry(root, width=5)
a1a_step_entry.grid(row=6, column=3)
 # A2 range
a2_label = ttk.Label(root, text="A2 Range:")
a2_label.grid(row=7, column=0, sticky="w")
a2_start_entry = ttk.Entry(root, width=5)
a2_start_entry.grid(row=7, column=1)
a2_end_entry = ttk.Entry(root, width=5)
a2_end_entry.grid(row=7, column=2)
a2_step_entry = ttk.Entry(root, width=5)
a2_step_entry.grid(row=7, column=3)
 # A2a range
a2a_label = ttk.Label(root, text="A2a Range:")
a2a_label.grid(row=8, column=0, sticky="w")
a2a_start_entry = ttk.Entry(root, width=5)
a2a_start_entry.grid(row=8, column=1)
a2a_end_entry = ttk.Entry(root, width=5)
a2a_end_entry.grid(row=8, column=2)
a2a_step_entry = ttk.Entry(root, width=5)
a2a_step_entry.grid(row=8, column=3)
 # B2 range
b2_label = ttk.Label(root, text="B2 Range:")
b2_label.grid(row=9, column=0, sticky="w")
b2_start_entry = ttk.Entry(root, width=5)
b2_start_entry.grid(row=9, column=1)
b2_end_entry = ttk.Entry(root, width=5)
b2_end_entry.grid(row=9, column=2)
b2_step_entry = ttk.Entry(root, width=5)
b2_step_entry.grid(row=9, column=3)
 # B2a range
b2a_label = ttk.Label(root, text="B2a Range:")
b2a_label.grid(row=10, column=0, sticky="w")
b2a_start_entry = ttk.Entry(root, width=5)
b2a_start_entry.grid(row=10, column=1)
b2a_end_entry = ttk.Entry(root, width=5)
b2a_end_entry.grid(row=10, column=2)
b2a_step_entry = ttk.Entry(root, width=5)
b2a_step_entry.grid(row=10, column=3)
 # Sod range
sod_label = ttk.Label(root, text="Sod Range:")
sod_label.grid(row=11, column=0, sticky="w")
sod_start_entry = ttk.Entry(root, width=5)
sod_start_entry.grid(row=11, column=1)
sod_end_entry = ttk.Entry(root, width=5)
sod_end_entry.grid(row=11, column=2)
sod_step_entry = ttk.Entry(root, width=5)
sod_step_entry.grid(row=11, column=3)
# Button to get parameter ranges
get_ranges_button = ttk.Button(root, text="Get Parameter Ranges", command=get_parameter_ranges)
get_ranges_button.grid(row=12, column=0, columnspan=4, pady=10)

root.mainloop()
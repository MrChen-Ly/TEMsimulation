# -*- coding: utf-8 -*-
"""version——3
Created on Mon Jan 12 15:50:47 2026

@author: Linyuan chen
"""

#add Accelerating Voltage control


# -*- coding: utf-8 -*-
"""version——2
Created on Thu Jan  4 17:32:22 2024

@author: Linyuan chen
"""

# -*- coding: utf-8 -*-

"""version——1
Created on Mon Dec 25 19:24:15 2023

@author: Linyuan chen
"""
## 增加图像的回传和打开
from tkinter import *

def run_tem_simulation(work_path, CIF_NAME, CIF_path,colortype):   
    import numpy as np
    import math
    import os
    import tifffile as tiff
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    from tkinter import Toplevel
    from matplotlib.colors import LinearSegmentedColormap
    from tkinter import filedialog 
    
    # 获取环境变量 WORK_PATH 的值
    #work_path = os.environ.get('WORK_PATH', '')
    #CIF_path = os.environ.get('CIF_PATH', '')
    
    def read_binary_file(file_path, height, width):
        # 从二进制文件读取数据
        image_data = np.fromfile(file_path, dtype=np.float32)
        
        # 将一维数组转换为二维数组
        image_shape = (height, width)
        image_data = image_data.reshape(image_shape)
        
        return image_data
    def create_custom_cmap():
       if (colortype==1):
            # 定义自定义的颜色映射
           #colors = [(1, 0, 0), (1, 1, 1), (0, 0, 1)]  # 红-白-蓝 
           colors = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)]  # 黑-蓝-绿-红-黄-白
           cmap_name = 'custom_gradient'
       else:
           cmap_name = 'custom_graymap'
           colors = [(0,0,0),(1,1,1)]
       return LinearSegmentedColormap.from_list(cmap_name, colors)
    
    def open_plot_window(image_data):
        # Create a sub-window
        plot_window = Toplevel()
        plot_window.title("Matplotlib Plot")
        
        # Create a NumPy 2D array (example data)
        array_data =  image_data
        
        # Use Matplotlib to plot the image
        fig, ax = plt.subplots()
        cax = ax.matshow(array_data,cmap=create_custom_cmap())
        fig.colorbar(cax)
        
        # Embed Matplotlib figure into Tkinter sub-window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas_widget.config(width=800, height=800)
        # Add Navigation Toolbar (optional but useful for zooming)
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        canvas_widget.config(scrollregion=canvas_widget.bbox("all"))
    
        def zoom_in():
            ax.set_xlim(ax.get_xlim()[0] * 1.1, ax.get_xlim()[1] * 1.1)
            ax.set_ylim(ax.get_ylim()[0] * 1.1, ax.get_ylim()[1] * 1.1)
            canvas.draw()
    
        def zoom_out():
            ax.set_xlim(ax.get_xlim()[0] / 1.1, ax.get_xlim()[1] / 1.1)
            ax.set_ylim(ax.get_ylim()[0] / 1.1, ax.get_ylim()[1] / 1.1)
            canvas.draw()
    
        # Add Zoom In and Zoom Out buttons
        button_zoom_in = Button(plot_window, text="Zoom In", command=zoom_in)
        button_zoom_in.pack(side="left")
    
        button_zoom_out = Button(plot_window, text="Zoom Out", command=zoom_out)
        button_zoom_out.pack(side="left")
    
        # Start the Tkinter event loop for the sub-window
        plot_window.mainloop()
    
    '''
    User
    def open_plot_window(image_data):
        # Create a sub-window
        plot_window = Toplevel()
        plot_window.title("Matplotlib Plot")
    
        # Create a NumPy 2D array (example data)
        array_data =  image_data
    
        # Use Matplotlib to plot the image
        fig, ax = plt.subplots()
        cax = ax.matshow(array_data, cmap='viridis')
        fig.colorbar(cax)
    
        # Embed Matplotlib figure into Tkinter sub-window
        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
        canvas_widget.config(width=1080, height=1080)
        # Start the Tkinter event loop for the sub-window
        plot_window.mainloop()
    '''
    def export_to_window(file_path, height, width, output_folder):
        # 读取二进制文件
        image_data = read_binary_file(file_path, height, width)
        #在子界面中显示
        open_plot_window(image_data)
    def export_to_tiff(file_path, height, width, output_folder):
        # 读取二进制文件
        image_data = read_binary_file(file_path, height, width)
        # 构造输出文件路径
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(output_folder, f"{file_name}.tif")
        
        # 保存为tif文件
        tiff.imsave(output_path, image_data)
        print(f"导出成功: {output_path}")
    
    def batch_export_to_tiff(input_folder, output_folder,height,width):
        # 获取选中的多个文件
        file_paths = filedialog.askopenfilenames(title="选择多个二进制文件", filetypes=[("Data files", "*.dat"), ("All files", "*.*")])
    
        for file_path in file_paths:
            # 提取文件名、高度和宽度等信息（请根据实际情况修改）
            file_name = os.path.splitext(os.path.basename(file_path))[0]           
            # 导出为tif文件
            export_to_tiff(file_path, height, width, output_folder)
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
    
    def replace_lines(file_path, start_line, end_line, new_content,newpath):
        with open(file_path, 'r') as file:
            lines = file.readlines()   
        if start_line <= len(lines) :
            lines[start_line-1:end_line-1] = new_content 
        with open(newpath, 'w') as file:
            file.writelines(lines)
    
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
    #_________________________________________________________________________  
    def submit():
        values = []
        for entry in entries:
            value = entry.get()
            values.append(value)
        print("Input Values:", values)
    #_________________________________________________________________________________
        num=9
        global workingDir, typef,xp,yp
        workingDir = values[0] #文件存储路径
        docname=values[1] #img文件夹下的子文件夹名
        tiltlist=[]
        nua=1
        cifname=values[2]  #cif文件名
        celname=values[3]  #cel文件名
        typef=int(values[4])
        celname2=celname+'1'
        global slcname, tkmin,tkminnm
        slcname=celname   
        a=float(values[5])*0.1 #晶胞参数a
        b=float(values[6])*0.1#晶胞参数b
        c=float(values[7])*0.1   #晶胞参数c
        rpx=int(values[8])     #单胞扩充数x方向
        rpy=int(values[9])     #单胞扩充数y方向
        a=a*rpx
        b=b*rpy
        slice1=int(values[10])  #切片数
        think=200  #厚度数
        xa=round(a/(float(values[32])),0)*2
        yb=round(b/(float(values[32])),0)*2
        zc=slice1
        na=a/xa
        nb=b/yb
        dfmin=float(values[11])   #焦距的最小值
        dfmax=float(values[13])    #焦距的最大值
        dfcont=round((dfmax-dfmin)/float(values[12])+1,0)   #焦距的变化数    
        tkmin=float(values[14])   #厚度nm     
        tkmax=float(values[16])   #厚度nm
        tkcont=round((tkmax-tkmin)/float(values[15])+1,0)  #厚度变化数
        tkmin=round(tkmin/(c/slice1),0)
        tkmax=round(tkmax/(c/slice1),0)
        xp=round(xa*0.5*dfcont,0)
        yp=round(yb*0.5*tkcont,0)
        defocus=dfmin   #nm
        think=tkmax
        A1x=float(values[17].split(',')[0])*math.cos(float(values[17].split(',')[1])/180*(math.pi))       #nm
        A1y=float(values[17].split(',')[0])*math.sin(float(values[17].split(',')[1])/180*(math.pi)) 
        comax=float(values[18].split(',')[0])*math.cos(float(values[18].split(',')[1])/180*(math.pi)) 
        comay=float(values[18].split(',')[0])*math.sin(float(values[18].split(',')[1])/180*(math.pi)) #nm
        A2x=float(values[19].split(',')[0])*math.cos(float(values[19].split(',')[1])/180*(math.pi))
        A2y=float(values[19].split(',')[0])*math.sin(float(values[19].split(',')[1])/180*(math.pi)) #nm
        CS=float(values[20])   #nm
        Oapx=float(values[21]) #mrad
        vibx=float(values[22])   #vibration
        viby=float(values[23])  #vibration 
        fs=float(values[29]) #focus-spread
        sc=float(values[30]) #semi-convergence
        fr=float(values[31]) #frame rotation
        Voltage=float(values[33])# Accelerating Voltage
        
        #tilt change
        if (typef==3):
            defocus=0.0
                
        file_path = workingDir+ 'prm\\msa_strd.prm' # 替换目标文件路径
        line_number = 27  # 要替换的行号
        new_line =  '\'slc\\%s\''  % slcname # 新的行内容
        newpath=workingDir+'prm\\msa_%s.prm'%slcname 
        replace_single_line_in_file(file_path, line_number, new_line,newpath)

        file_path = workingDir+'prm\\msa_%s.prm'%slcname  # 替换目标文件路径
        line_number = 6  # 要替换的行号
        lambda_nm = 1.226 / np.sqrt(Voltage * 1000 * (1 + 0.978e-6 * Voltage * 1000))
        new_line =  '%d'  % Voltage # 新的行内容
        newpath=workingDir+'prm\\msa_%s.prm'%slcname 
        replace_single_line_in_file(file_path, line_number, new_line,newpath)    
    
        if (typef==1):
            file_path = workingDir+'prm\\wavimg_1.prm'  # 替换目标文件路径
            line_number = 1 # 要替换的行号
            new_line = '\'wav\\%s_sl%03d.wav\''% (slcname,tkmin) # 新的行内容
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number, new_line, newpath)
            xp=round(xa*0.5,0)
            yp=round(yb*0.5,0)
        else:
            file_path = workingDir+'prm\\wavimg_%d.prm'%typef  # 替换目标文件路径
            line_number = 1 # 要替换的行号
            new_line = '\'wav\\%s_sl.wav\''% (slcname) # 新的行内容
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number, new_line, newpath)
    
        file_path = workingDir+'prm\\wavimg_%s.prm' % (slcname)  # 替换目标文件路径
        line_number = 2 # 要替换的行号
        new_line = '%d,%d' %(xa,yb)# 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath)
    
        file_path = workingDir+'prm\\wavimg_%s.prm' % (slcname)  # 替换目标文件路径
        line_number = 3 # 要替换的行号
        new_line = '%0.9f,%0.9f' %(na,nb)# 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath)  
        
        file_path = workingDir+'prm\\wavimg_%s.prm' % (slcname)  # 替换目标文件路径
        line_number = 4 # 要替换的行号
        new_line = '%d.' %(Voltage)# 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath)    
        
    
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 6  # 要替换的行号
        new_line = '\'img\\%s\\%s_map.dat\''% (docname,slcname) # 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath) 
    
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 7  # 要替换的行号
        new_line = '%d,%d'% (xp,yp) # 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath)
        
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 10  # 要替换的行号
        new_line = '%.6f'% (float(values[32])) # 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath)
        
        #Cs changed
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 17  # 要替换的行号
        new_line = '2,%.3f,%.3f,0.0'%(vibx,viby)
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number,new_line, newpath)
    
    
    
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 12  # 要替换的行号
        new_line = '%0.1f'%(fr)
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number,new_line, newpath)
    
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 14  # 要替换的行号
        new_line = '1, %0.1f'%(fs)
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number,new_line, newpath)
    
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 15  # 要替换的行号
        new_line = '1, %0.1f'%(sc)
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number,new_line, newpath)
        
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 18  # 要替换的行号
        new_line = '10\n'+'0.0 0.0 0.0 0.0\n'+'1, %0.1f'%defocus+', 0.\n'+'2, %0.1f,%0.1f 0.\n'%(A1x,A1y)+'3, %0.1f, %0.1f 0.0\n' %(comax,comay)+'4, %0.1f, %0.1f 0.0\n'%(A2x,A2y) +'5, %0.1f, 0.\n'%CS+'6.0 0.0 0.0 0.0\n'+'7.0 0.0 0.0 0.0\n'+'8.0 0.0 0.0 0.0\n'+'9.0 0.0 0.0 0.0\n'+'%0.1f ,0.03 \n'%Oapx # 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        endline= 30
        replace_lines(file_path, line_number, endline,new_line, newpath)
    
        #loop change
        if(typef==3):
            file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
            line_number = 35  # 要替换的行号
            new_line = '%0.1f,%0.1f,%d'%(dfmin,dfmax,dfcont)
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number,new_line, newpath)
            file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
            line_number = 40  # 要替换的行号
            new_line = '%d,%d,%d'%(tkmin,tkmax,tkcont)
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number,new_line, newpath)
        elif(typef==2):
            file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
            line_number = 35  # 要替换的行号
            new_line = '%d,%d,%d'%(tkmin,tkmax,tkcont)
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number,new_line, newpath)
            xp=round(xa*0.5,0)
            yp=yp
            file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
            line_number = 7  # 要替换的行号
            new_line = '%d,%d'% (xp,yp) # 新的行内容
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number, new_line, newpath) 
            
        else:
            file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
            line_number = 6  # 要替换的行号
            tkminnm=tkmin*(c/slice1)
            new_line = '\'img\\%s\\%s_TK_%s.dat\''% (docname,slcname,tkminnm) # 新的行内容
            newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
            replace_single_line_in_file(file_path, line_number, new_line, newpath) 
        '''Cs changed
        
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 18  # 要替换的行号
        new_line = '2\n'+'1,6,0.\n'+'5,-11000.0,0.' # 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        endline= 20
        replace_lines(file_path, line_number, endline,new_line, newpath)
        '''
        
        file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
        line_number = 16  # 要替换的行号
        
        new_line = '%d, 1., \'prm\MTF-US2k-300.mtf\' '% (int(values[26])) # 新的行内容
        newpath= workingDir+'prm\\wavimg_%s.prm' % (slcname)
        replace_single_line_in_file(file_path, line_number, new_line, newpath) 
        repeat=''
        for i in range(slice1):
            repeat=repeat+'%d' %i+'\n'
    
        num_rows=int(think/slice1)+1
        repeated_text = (repeat) * num_rows
        repeated_text = '%d' %slice1+'\n'+'1\n'+'1\n'+'1\n'+'%d' %think+'\n'+repeated_text 
    
    
        file_path = workingDir+'prm\\msa_%s.prm' %slcname
        start_line = 28
        end_line = 150
        new_content = '%s'% repeated_text
        newpath=workingDir+'prm\\msa_%s.prm' %slcname
        replace_lines(file_path, start_line, end_line, new_content,newpath)
    
        ##清空cel
        import os
        import shutil
        
        def check_and_create_folder(folder_path):
            # 检查文件夹是否存在
            if os.path.exists(folder_path):
                # 如果存在，清空文件夹
                try:
                    shutil.rmtree(folder_path)
                    os.makedirs(folder_path)  # 重新创建空文件夹
                    print(f"文件夹 '{folder_path}' 已清空并重新创建。")
                except Exception as e:
                    print(f"清空文件夹 '{folder_path}' 时发生错误: {e}")
            else:
                # 如果不存在，创建文件夹
                try:
                    os.makedirs(folder_path)
                    print(f"文件夹 '{folder_path}' 已创建。")
                except Exception as e:
                    print(f"创建文件夹 '{folder_path}' 时发生错误: {e}")    
        #tilt change
        #_______________________________________________________________________________________
        global tiltlength
        tiltlength=float(values[27])*0.18/(math.pi)
        
        tiltx=float(values[27])*0.18/(math.pi)*math.cos(float(values[28])/180*(math.pi))
        tilty=float(values[27])*0.18/(math.pi)*math.sin(float(values[28])/180*(math.pi))  
        file_path = workingDir+'prm\\msa_%s.prm'%slcname  # 替换目标文件路径
        line_number = 13  # 要替换的行号
        new_line =  '%f' %tiltx # 新的行内容
        newpath=workingDir+'prm\\msa_%s.prm'%slcname 
        replace_single_line_in_file(file_path, line_number, new_line,newpath)
        
        file_path=workingDir+'prm\\msa_%s.prm'%slcname 
        line_number = 14  # 要替换的行号
        new_line =  '%f' %tilty  # 新的行内容
        replace_single_line_in_file(file_path, line_number, new_line,newpath)
       #_______________________________________________________________________________________
        Atom_string = values[24]
        result = Atom_string.split(',')
        Dw_string = values[25]
        DW = Dw_string.split(',')
        DW=[round(float(num) * 0.01,8) for num in DW]
        print(DW)
        result_string=''
        for i,Atom_text in enumerate(result):
            result_string=result_string+' -B %2s,'%(Atom_text)+str(DW[i])#调整了相关数据结构。
        string=workingDir[0:len(workingDir)-1]
        string2=workingDir[0:2]
        check_and_create_folder(workingDir+'cel')
        runPrmFileBat = open(workingDir + 'img\\runPrm.bat', 'w')
        runPrmFileBat.write(r'cd %s'%string)
    
        runPrmFileBat.write('\n%s'%string2)
        tz=1/(slice1*2)
        #runPrmFileBat.write('\nBuildcell BuildCell --spacegroup=1 --lattice=3.810000,3.810000,3.810000,90.0,90.0,90.0 ---atom=H，0.000000，0.000000，0.500000，1.00，0.5 --atom=H，0.500000，0.000000，0.000000，1.00，0.5 --atom=H，0.000000，1.000000，0.500000，1.0 ，0.500000 --atom=H，0.500000，0.000000，1.000000，1.0 ，0.500000 --atom=H，0.500000，1.000000，0.000000，1.0 ，0.500000 --atom=H，0.000000，0.500000，0.000000，1.0 ，0.500000 --atom=H，0.500000，1.000000，1.000000，1.0 ，0.500000 --atom=H，0.000000，0.500000，1.000000，1.0，0.500000 --atom=Al，0.000000，1.000000，0.000000，1.0，0.500000 --atom=Al，0.000000，0.000000，1.000000，1.0，0.500000 --atom=Al，0.000000，0.000000，0.000000，1.0，0.500000 --atom=Al，0.000000，1.000000，1.000000，1.0，0.500000 --atom=La，0.500000，0.500000，0.500000，1.0 0.500000  --output=cel\%s.cel'%(celname))
        runPrmFileBat.write('\nBuildcell --cif=cif\\%s.cif --output=cel\\%s.cel'%(cifname,celname))
        runPrmFileBat.write('\ncellmuncher -f cel\\%s.cel -o cel\\%s.cel %s  --cif --override' %(celname,celname2,result_string))
       #runPrmFileBat.write('\nCellMuncher -f cel\\%s.cel -o cel\\%s2.cel -T x,0.25 -T y,0.25 -T z,%0.2f'%(celname2,celname2,tz))
       #runPrmFileBat.write('\nCellMuncher -f cel\\%s.cel -o cel\\%s3.cel --periodic=x --periodic=y --periodic=z --cif'%(celname2,celname2))
       #runPrmFileBat.write('\nCellMuncher -f cel\\%s3.cel -o cel\\%s4.cel --remove-close-atoms=0.2 --cif'%(celname2,celname2))
        runPrmFileBat.write('\nCellMuncher -f cel\\%s.cel -o cel\\%s5.cel --repeat=x,%d --repeat=y,%d --cif'%(celname2,celname2,rpx,rpy))
        runPrmFileBat.write('\ncelslc -cel cel\\%s5.cel -slc slc\\%s -nx %d -ny %d -nz %d -ht %d. -abs -dwf' %(celname2,slcname,xa,yb,zc,Voltage))
           
        runPrmFileBat.write('\nmd img\\%s' % docname)
    
    
        runPrmFileBat.write('\nmsa -prm prm\\msa_%s.prm -out wav\\%s /ctem'% (slcname,slcname))
        runPrmFileBat.write('\nwavimg -prm prm\\wavimg_%s.prm /nli' % (slcname))
                
                
        runPrmFileBat.close()
        
        print("像素点大小：%dX%d " %(xp,yp))
        print("runPrm储存至：%simg"%workingDir)
    
        # 批处理文件的路径
        batch_file_path = workingDir + 'img\\runPrm.bat'  # 替换为实际的批处理文件路径
        runbatfile(batch_file_path)
        if (typef==1):
            export_to_tiff(workingDir+r'img\%s\%s_TK_%s.dat'% (docname,slcname,tkminnm),int(yp),int(xp),workingDir+'img\\%s'% (docname))
        else:
            export_to_tiff(workingDir+'img\\%s\\%s_map.dat'% (docname,slcname),int(yp),int(xp),workingDir+'img\\%s'% (docname))
            
        if (typef==1):
            export_to_window(workingDir+r'img\%s\%s_TK_%s.dat'% (docname,slcname,tkminnm),int(yp),int(xp),workingDir+'img\\%s'% (docname))
        else:
            export_to_window(workingDir+'img\\%s\\%s_map.dat'% (docname,slcname),int(yp),int(xp),workingDir+'img\\%s'% (docname))
           
    def abberationScan(length, anglebg,angleInteral,angleend):
    	global numl, abberList
    	numl=int((angleend-anglebg)/angleInteral)
    
        #if 360 % angleInteral == 0:
    		#numl = (360 // angleInteral)
    	#else:
    		#numl = (360 // angleInteral) + 1
    	
    	abberList = []
    	for i in range(numl):
    		abberList.append([])
    		angle = angleInteral * i+anglebg
    		abberX = round(math.cos(angle/180*(math.pi)) * length, 4)
    		abberY = round(math.sin(angle/180*(math.pi)) * length, 4)
    		abberList[i].append(length)
    		abberList[i].append(abberX)
    		abberList[i].append(abberY)
    		abberList[i].append(angle)
    
            
    def lengthScan(alength, Interal, alengthend, angle):
        global numl,abberList
        numl= int((alengthend-alength)/Interal)
        abberList = []
        for i in range(numl):
            abberList.append([])
            length= alength+i*Interal
            #print(length)
            abberX = round(math.cos(angle/180*(math.pi)) * length, 4)
            abberY = round(math.sin(angle/180*(math.pi)) * length, 4)
            abberList[i].append(length)
            abberList[i].append(abberX)
            abberList[i].append(abberY)
            abberList[i].append(angle)
        
    def tiltloop():
        
        tiltbg=float(tilt_entry1.get())
        tiltic=float(tilt_entry2.get())
        tilted=float(tilt_entry3.get())
        abberationScan(tiltlength,tiltbg,tiltic,tilted)
        current_path=workingDir+'img'
        folder_path= os.path.join(current_path,'tiltloop')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        with open(workingDir+'img\\tiltloop\\recordingtxt.txt','w') as file:
            file.write("length abberX abberY angle\n")
            for item in abberList:
                file.write(f"{item}\n" )
        for i in range(numl):
            file_path = workingDir+'prm\\msa_%s.prm'%slcname  # 替换目标文件路径
            line_number = 13  # 要替换的行号
            new_line =  '%f' %abberList[i][1] # 新的行内容
            newpath=workingDir+'prm\\msa_%s_tilt_%s.prm'%(slcname,i) 
            replace_single_line_in_file(file_path, line_number, new_line,newpath)
            
            file_path=workingDir+'prm\\msa_%s_tilt_%s.prm'%(slcname,i) 
            line_number = 14  # 要替换的行号
            new_line =  '%f' %abberList[i][2]  # 新的行内容
            replace_single_line_in_file(file_path, line_number, new_line,newpath)
            print("\n tilt : %f, %f"%(abberList[i][1],abberList[i][2]))
            
            file_path = workingDir+'prm\\wavimg_%s.prm'%slcname  # 替换目标文件路径 newpath=workingDir+'prm\\msa_tilt_x%d_y%d.prm' % (tiltx,tilty)
            line_number = 1 # 要替换的行号
            
            if (typef==1):
                new_line = '\'wav\\%s_tilt_%s_sl%03d.wav\''% (slcname,i,tkmin) # 新的行内容
            else:
                new_line = '\'wav\\%s_tilt_%s_sl.wav\''% (slcname,i) # 新的行内容
            
            
            newpath= workingDir+'prm\\wavimg_%s_tilt_%s.prm' % (slcname,i)
            replace_single_line_in_file(file_path, line_number, new_line, newpath)    
            file_path=workingDir+'prm\\wavimg_%s_tilt_%s.prm' % (slcname,i)
            line_number = 6  # 要替换的行号
            new_line = '\'img\\tiltloop\\mapping_%s_tilt_%s.dat\''% (slcname,i) # 新的行内容
            replace_single_line_in_file(file_path, line_number, new_line, newpath) 
    
        runPrmFileBat = open(workingDir + 'img\\tiltloop\\TiltrunPrm.bat', 'w')
        string=workingDir[0:len(workingDir)-1]
        string2=workingDir[0:2]
        runPrmFileBat.write(r'cd %s'%string)
        runPrmFileBat.write('\n%s'%string2)
        for j in  range(numl):
        	runPrmFileBat.write('\nmsa -prm prm\\msa_%s_tilt_%s.prm -out wav\\%s_tilt_%s /ctem'% (slcname,j,slcname,j))
        	runPrmFileBat.write('\nwavimg -prm prm\\wavimg_%s_tilt_%s.prm /nli' % (slcname,j))
        runPrmFileBat.close()
        batch_file_path = (workingDir + 'img\\tiltloop\\TiltrunPrm.bat')  # 替换为实际的批处理文件路径
        runbatfile(batch_file_path)	
        batch_export_to_tiff((workingDir + 'img\\tiltloop'),(workingDir + 'img\\tiltloop'),int(yp),int(xp))            
        
    def open_child_window():
        def do_A1loop(looptype):
            A1Length=float(childentry.get().split(',')[0])
            A1Angle=float(childentry2.get().split(',')[0])
            Interal=float(childentry.get().split(',')[1])
            A1Lengthend=float(childentry.get().split(',')[2])
            print(A1Length,A1Lengthend,Interal,A1Angle)
            selected_options=''
            selected_type=0
            val=int(childentry4.get())
            if val==1:
                selected_options='A1'
                selected_type=21
            if val==2:
                selected_options='A2'
                selected_type=23
            if val==3:
                selected_options='B2'
                selected_type=22
            if val==4:
                selected_options='def'
                selected_type=20
            if (selected_type==0):
                print("bad")
                return
                
            if (looptype==1):
                lengthScan(A1Length, Interal,A1Lengthend,A1Angle)
            else:
                angleInteral=int(childentry2.get().split(',')[1])
                angleend=int(childentry2.get().split(',')[2])
                abberationScan(A1Length, A1Angle, angleInteral,angleend)
            #改变wavimg文件中的A1和img文件的名字并将wavimg文件重命名
            current_path=workingDir+'img'
            folder_path= os.path.join(current_path,'%sloop'%selected_options)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            with open(workingDir+'img\\%sloop\\recordingtxt.txt'%selected_options,'w') as file:
                file.write("length abberX abberY angle\n")
                for item in abberList:
                    file.write(f"{item}\n" )
            #3 write prm files at all angles
            for i in range(numl):
                file_path=workingDir+'prm\\wavimg_%s.prm' % (slcname)
                line_number = selected_type  # 要替换的行号
                new_line = '%d,'%(selected_type-19)+str(abberList[i][1])+', ' + str(abberList[i][2]) # 新的行内容
                newpath= workingDir+'prm\\wavimg_%s_%s_No_%s.prm' % (slcname,selected_options,i)
                replace_single_line_in_file(file_path, line_number, new_line, newpath) 
                
                file_path= workingDir+'prm\\wavimg_%s_%s_No_%s.prm' % (slcname,selected_options,i)
                line_number = 6  # 要替换的行号
                new_line = '\'img\\%sloop\\%s_%s_No_%s.dat\''% (selected_options,slcname,selected_options,i)# 新的行内容
                newpath= workingDir+'prm\\wavimg_%s_%s_No_%s.prm' % (slcname,selected_options,i)
                replace_single_line_in_file(file_path, line_number, new_line, newpath) 
            
                
                
            #4 write a bat file to run prm files one by one with WAVIMG
            runPrmFileBat = open(workingDir + 'img\\%sloop\\%srunLoop.bat'%(selected_options,selected_options), 'w')
            string=workingDir[0:len(workingDir)-1]
            string2=workingDir[0:2]
            runPrmFileBat.write(r'cd %s'%string)
            runPrmFileBat.write('\n%s'%string2)
            for i in range(numl):
            	runPrmFileBat.write('\nwavimg -prm prm\\wavimg_%s_%s_No_%s.prm /nli' % (slcname,selected_options,i))#% (i * abAngleInteral))
            runPrmFileBat.close()
            # 批处理文件的路径
            batch_file_path = workingDir + 'img\\%sloop\\%srunLoop.bat'%(selected_options,selected_options)  # 替换为实际的批处理文件路径
            runbatfile(batch_file_path)
            
            batch_export_to_tiff((workingDir + 'img\\tiltloop'),(workingDir + 'img\\%sloop'%(selected_options)),int(yp),int(xp)) 
            
        def on_child_button_click(number):
            A1Length=float(childentry.get())
            if(number==1):
                print("子窗口按钮1被点击: %f" %A1Length)
            else:
                print("子窗口按钮2被点击")
        child_window = Toplevel(root)
        child_window.title("Ab loop")
        child_window.geometry("200x300")
        child_label = Label(child_window, text="change")
        child_label.pack()
        child_button = Button(child_window, text=" Length", command=lambda:do_A1loop(1))
        child_button.pack()
        child_button2 = Button(child_window, text=" Angle", command=lambda:do_A1loop(2))
        child_button2.pack()
        child_window.protocol("WM_DELETE_WINDOW", lambda: child_window_destroy(child_window))
        childlabel = Label(child_window, text=" Length bg,in,ed(nm)")
        childlabel.pack()
        childentry=Entry(child_window,width=15)
        childentry.pack()
        childlabe2 = Label(child_window, text=" Angle (deg),in(deg),end(deg)")
        childlabe2.pack()
        childentry2=Entry(child_window,width=15)
        childentry2.pack()
        child_labe3 = Label(child_window, text="selecte a loop type：")
        child_labe3.pack(pady=10)
        childlabel4 = Label(child_window, text="1 for A1\n 2 for A2\n 3 for B2")
        childlabel4.pack(pady=10)
        childentry4=Entry(child_window,width=15)
        childentry4.pack()
        '''
        var1 = BooleanVar()
        checkbutton1 = Checkbutton(child_window, text="A1", variable=var1)
        checkbutton1.pack()
    
    
        var2 = BooleanVar()
        checkbutton2 = Checkbutton(child_window, text="A2", variable=var2)
        checkbutton2.pack()
    
    
        var3 = BooleanVar()
        checkbutton3 = Checkbutton(child_window, text="B2", variable=var3)
        checkbutton3.pack()
        
        '''
    def child_window_destroy(child_window):
        child_window.destroy()  
    root = Tk()
    
    root.title("TEM simulation GUI for Dr.Probe 3.0.0")
    labels = ["Workpath", "sub_workfolde", "cif_name", "doc_name for save", "worktype", "a(A)", "b(A)", "c(A)", "repeat alone x ", "repeat alone y","slicenumber", "defocus (nm)", "defocus_increace (nm)", "defocus_end (nm)", "thickness (nm)", "thickness_increace (nm)", "thickness_end (nm)", "A1 (nm), angle(Deg)", "coma (nm), anlge(Deg)", "A2 (nm), anlge(Deg)", "Cs (nm)", "Oapx (mrad)", "Vibrationx (nm)", "Vibrationy (nm)","Atoms","Dw(A^2)"," with MTF（Radio） ","Tilt angle (mrad)","Rotation angle (Deg)","focus-spread(nm)","semi-convergence(mrad)","Frame rotation(Deg)","sample rate(nm/pixel)","Accelerating Voltage"]
    Values1 = [ (work_path+"\\"),CIF_NAME,CIF_NAME,CIF_NAME,"2", "7.64"  ,"7.64" , "7.64" ,"3","3" ,"4", "4.5","1.0","6.5" ,"5.5","1.0","8.5","1.0,74.0","20.0,260.0","20.0,300.0","-10000.0","250.0","0.025","0.025","La,Al,O,H","0.5,0.5,1.10803","1","2.0","90.0","2.8","0.24","135","0.008690","300"]
    
    entries = []
    
    frame1 = Frame(root)
    frame1.pack(side=LEFT, padx=10)
    frame2 = Frame(root)
    frame2.pack(side=LEFT, padx=10)
    for i, label_text in enumerate(labels):
        if i < 17:
            frame = frame1
        else:
            frame = frame2
    
        label = Label(frame, text=label_text)
        label.pack()
    
        entry = Entry(frame)
        Value=Values1[i]
        entry.insert(0, Value)  # 预设填入的值
        entry.pack()
        entries.append(entry)
    
    submit_button = Button(root, text="Submit", command=submit)
    submit_button.place(x=250,y=10) 
    # 创建按钮，并绑定打开子窗口的函数
    open_button = Button(root, text=" loop", command=open_child_window,width=15)
    open_button.pack(pady=60)
    
    tilt_button = Button(root, text=" loop", command=tiltloop,width=15)
    tilt_button.place(x=325,y=550)
    tilt_labe1 = Label(root, text="beg")
    tilt_labe1.place(x=325,y=485)
    tilt_entry1=Entry(root,width=3)
    tilt_entry1.place(x=325,y=510)
    tilt_labe2 = Label(root, text="inc")
    tilt_labe2.place(x=365,y=485)
    tilt_entry2=Entry(root,width=3)
    tilt_entry2.place(x=360,y=510)
    tilt_labe3 = Label(root, text="end")
    tilt_labe3.place(x=400,y=485)
    tilt_entry3=Entry(root,width=3)
    tilt_entry3.place(x=400,y=510)

    # 启动主循环
    root.mainloop()
    
    

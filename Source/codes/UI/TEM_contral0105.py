# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 21:54:12 2023

@author: chen
"""
import tkinter as tk
from tkinter import Menu, filedialog, simpledialog
import os
import shutil
import subprocess
from threading import Thread
from TEMsimulation5 import run_tem_simulation  # 导入 TEM 模拟的运行函数

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('TEM simulation GUI for Dr.Probe 3.0.0')
        self.root.geometry("500x200+1100+150")
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.text_box = tk.Text(self.root, wrap='word', height=10, width=400)
        self.text_box.pack(padx=10, pady=10)

        self.work_path = None
        self.cif_file_path = None
        self.colortype=1
        self.interface()

    def interface(self):
        self.menubar.add_cascade(label="文件", menu=self.file_menu())
        self.menubar.add_cascade(label="查看", menu=self.about_menu())
        self.menubar.add_cascade(label="运行",  command=self.run_in_thread)  # 添加"运行"菜单
       
    def run_in_thread(self):
        # 启动新线程运行子进程
        thread = Thread(target=self.run_subprocess)
        thread.start()

    def run_subprocess(self):
        if self.cif_file_path and self.work_path:
            env = os.environ.copy()
            env['WORK_PATH'] = self.work_path
            
            env['CIF_NAME'] = os.path.splitext(os.path.basename(self.cif_file_path))[0]
            run_tem_simulation(self.work_path, env['CIF_NAME'],self.cif_file_path,self.colortype) 
            
            # 可以选择在这里添加一些与运行 TEM 模拟相关的处理，如果有必要
        else:
            print("工作路径为空，无法运行 TEMsimulation2.0.1.py")

    def file_menu(self):
        fmenu = Menu(self.menubar, tearoff=0)

        for item in ['新建', '打开', '读取', '另存为']:
            if item == '打开':
                fmenu.add_command(label=item, command=self.open_folder)
            elif item == '新建':
                fmenu.add_command(label=item, command=self.new_file)
            elif item == '保存':
                fmenu.add_command(label=item)
            elif item == '另存为':
                fmenu.add_command(label=item)
            else:
                fmenu.add_command(label=item)
        return fmenu

    def about_menu(self):
        amenu = Menu(self.menubar, tearoff=0)
        for item in ['gray', '隐藏的项目']:
            amenu.add_checkbutton(label=item,command=self.color)
        return amenu
    def color(self):
        self.colortype=-self.colortype
        print(self.colortype)
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("CIF files", "*.cif"), ("All files", "*.*")])

        if file_path:
            content = self.read_specific_line(file_path, "_cell_length_")
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, content)
            self.cif_file_path = file_path
            self.save_cif_file()

    def read_specific_line(self, file_path, target_text):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                relevant_lines = [line for line in lines if target_text in line]
                content = '\n'.join([line.replace(target_text, '').strip() for line in relevant_lines])
                return content
        except Exception as e:
            return f"读取文件时发生错误: {e}"

    def new_file(self):
        folder_path = filedialog.askdirectory(title="选择文件夹路径")
        if folder_path:
            new_folder_name = simpledialog.askstring("输入", "请输入新文件夹的名称：", initialvalue="NewFolder")
            if new_folder_name:
                self.work_path = os.path.join(folder_path, new_folder_name)
                os.makedirs(self.work_path)
                print(f"已在路径 {folder_path} 下创建新文件夹: {new_folder_name}")
                self.check_create_folder()
                self.open_file_dialog()

    def copy_files_to_destination(self, source_directory, destination_directory):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        source_path = os.path.join(current_directory, source_directory)
        destination_path = os.path.join(destination_directory)

        try:
            shutil.copytree(source_path, destination_path)
            print(f"Files copied from '{source_path}' to '{destination_path}' successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_create_folder(self):
        subfolders = ["cif", "wav", "prm", "slc", "img"]
        for subfolder in subfolders:
            folder_path = os.path.join(self.work_path, subfolder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")
            else:
                print(f"Folder already exists: {folder_path}")

        subfolder = "cel"
        folder_path = os.path.join(self.work_path, subfolder)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                os.makedirs(folder_path)
                print(f"文件夹 '{folder_path}' 已清空并重新创建。")
            except Exception as e:
                print(f"清空文件夹 '{folder_path}' 时发生错误: {e}")
        else:
            try:
                os.makedirs(folder_path)
                print(f"文件夹 '{folder_path}' 已创建。")
            except Exception as e:
                print(f"创建文件夹 '{folder_path}' 时发生错误: {e}")

    def open_folder(self):
        file_path = filedialog.askopenfilename(title="选择文件", filetypes=[("CIF files", "*.cif"), ("All files", "*.*")])

        if file_path:
            self.work_path = self.extract_path_before_subfolders(file_path, 2)
            self.cif_file_path = file_path
            content = self.read_specific_line(file_path, "_cell_length_")

            self.text_box.delete("1.0", tk.END)
            self.text_box.insert(tk.END, content)

            print(self.work_path)

    def save_cif_file(self):
        if self.cif_file_path and self.work_path:
            cif_filename = os.path.basename(self.cif_file_path)
            destination_path = os.path.join(self.work_path, "cif", cif_filename)
            shutil.copyfile(self.cif_file_path, destination_path)
            print(f"CIF文件已另存到: {destination_path}")

    def extract_path_before_subfolders(self, file_path, num_subfolders):
        components = file_path.split('/')
        num_subfolders = num_subfolders * (-1)
        extracted_path = '/'.join(components[:num_subfolders])
        return extracted_path

if __name__ == '__main__':
    a = GUI()
    a.root.mainloop()

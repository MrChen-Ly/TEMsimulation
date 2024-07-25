
这是一个基于Drprobe程序的TEM模拟UI界面拓展包
=======
这里将介绍如何使用这个拓展程序进行TEM模拟参数的设置与使用
----
1.获取Dr.Probe 程序包
-------
访问[Dr.probe官网](https://er-c.org/barthel/drprobe/drprobe-download.html)下载Dr.probe package Command-line tools <br>

2.将Dr.Probe 程序加载至系统文件夹
-------
将下载的Dr.probe 程序包中的程序组件（Buildcell.exe; CellMuncher.exe; celslc.exe; msa.exe; wavimg.exe）<br>
复制到系统文件夹中（路径一般为：C:\Windows\System32）也可以通过在菜单栏中找到命令行程序cmd.exe所在的文件夹位置找到系统路径

3.创建工作路径文件夹
-----
将Workpath文件夹拷贝到你的工作文件夹路径中，后续的模拟数据结果都将保存在这个文件夹中<br>
-cif 文件夹用于保存你的原始结构模拟数据；（注意cif文件中的Label需要同时标注上元素符号， 例如：Dy1 ；否则模拟过程中可能报错）<br>
-cel 文件夹用于保存通过buildcell.exe生成的cel文件,并用于后续切片模拟,注意:当出现celslc.exe报错时,一般首先检查cel文件夹中的文件是否有效 <br>
-slc 文件夹用于保存你的slc文件
-wav 文件夹用于保存你的波函数文件
-img 文件夹用于保存最终生成的图像,一般是.dat格式,可以使用dat2tif.exe转换为tif格式
-prm 文件夹用于保存你当前模拟使用的参数文件
具体的相关详细信息可以在dr.probe官网介绍中了解
-exe 文件夹保存有所有的拓展程序包

4.运行模拟主程序
------



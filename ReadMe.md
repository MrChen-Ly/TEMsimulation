
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
 * -cif 文件夹用于保存你的原始结构模拟数据；<br>
   		注意: cif文件中的Label需要同时标注上元素符号， 例如：Dy1 ；否则模拟过程中可能报错
 * -cel 文件夹用于保存通过buildcell.exe生成的cel文件,并用于后续切片模拟<br>
      注意: 当出现celslc.exe报错时,一般首先检查cel文件夹中的文件是否有效 <br>
 * -slc 文件夹用于保存你的slc文件<br>
 * -wav 文件夹用于保存你的波函数文件<br>
 * -img 文件夹用于保存最终生成的图像,一般是.dat格式,可以使用dat2tif.exe转换为tif格式<br>
 * -prm 文件夹用于保存你当前模拟使用的参数文件<br>
     具体的相关详细信息可以在dr.probe官网介绍中了解<br>
 * -exe 文件夹保存有所有的拓展程序包<br>

4.运行模拟主程序
------
 * 1.将你需要进行模拟的cif文件放置在workpath\cif文件夹中
 * 2.运行workpath\exe文件夹中的TEM_contral0104.exe文件
 * 3.点击菜单栏中的“文件”中的“打开”
 * 4.选择cif文件夹中需要进行模拟的cif文件
 * 5.等待程序运行，出现读取到的a，b，c的取值
 * 6.点击“运行”，进行参数设置
 * 7.参数列表如图所示：<br>
   分为文件命名部分：<br>
   workpath:文件路径，默认为cif文件所在路径；<br>sub_workfolder：img文件夹中的子文件夹名称，默认为cif文件名。<br>cif_name:cif文件的名称<br>doc——name of save：文件保存是的命名，默认为cif文件名称
 * 


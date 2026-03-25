# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 15:29:17 2024

@author: chen
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 20:48:42 2024

@author: admin
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 11:44:45 2024

@author: chen
"""

# %load  NCSI-DyScO3-simulation.py

# Import necesary packages 

import ncsisim_drprobe as simdrp
import subprocess

# define parameter

workingdir='E:\\RunTemp\\Drprobe\\' #default current workingdir


coordinates=289
for i in range(1, coordinates+1):
    
    max_ix = coordinates
    num_digits = len(str(max_ix + 1))
    celname=f'STO_110_Output_{(i):0{num_digits}d}'
    folder_path=f'{workingdir}\\cel'

    
    cmd_command = f'cd /d {workingdir}&& {workingdir[0:2]} && CellMuncher -f img\SrTiO_change_Hcoor\STO110\cel\{celname}.cel -o cel\{celname}.cel --repeat=x,1 --repeat=y,1 --cif'
    #print(cmd_command)
    output = subprocess.check_output(cmd_command, shell=True, encoding="utf-8")
    #print(output)
    #Define WorkingDir
    simdrp.commands.workdir(workingdir,output=False)
 
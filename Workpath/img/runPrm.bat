cd c:\Users\chen\githubclone\clonefolder\TEMsimulationUI\Workpath
c:
Buildcell --cif=cif\STO001Oshift2H.cif --output=cel\STO001Oshift2H.cel
cellmuncher -f cel\STO001Oshift2H.cel -o cel\STO001Oshift2H1.cel  -B Sr,0.0048 -B Ti,0.004 -B  O,0.012 -B  H,0.006  --cif --override
CellMuncher -f cel\STO001Oshift2H1.cel -o cel\STO001Oshift2H15.cel --repeat=x,2 --repeat=y,2 --cif
celslc -cel cel\STO001Oshift2H15.cel -slc slc\STO001Oshift2H -nx 178 -ny 180 -nz 4 -ht 300. -abs -dwf
md img\STO001Oshift2H
msa -prm prm\msa_STO001Oshift2H.prm -out wav\STO001Oshift2H /ctem
wavimg -prm prm\wavimg_STO001Oshift2H.prm /nli
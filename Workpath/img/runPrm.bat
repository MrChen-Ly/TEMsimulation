cd C:/Users/chen/githubclone/clonefolder/TEMsimulationUI/Workpath
C:
Buildcell --cif=cif\SrTiO3.cif --output=cel\SrTiO3.cel
cellmuncher -f cel\SrTiO3.cel -o cel\SrTiO31.cel  -B Sr,0.005 -B Ti,0.005 -B  O,0.0110803  --cif --override
CellMuncher -f cel\SrTiO31.cel -o cel\SrTiO315.cel --repeat=x,1 --repeat=y,1 --cif
celslc -cel cel\SrTiO315.cel -slc slc\SrTiO3 -nx 90 -ny 90 -nz 2 -ht 300. -abs -dwf
md img\SrTiO3
msa -prm prm\msa_SrTiO3.prm -out wav\SrTiO3 /ctem
wavimg -prm prm\wavimg_SrTiO3.prm /nli
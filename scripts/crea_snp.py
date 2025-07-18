"""
Crea un snapshot de los casos.
Suma opciones para que funcione correctamente en el SADI.
"""

import psse34
import psspy

import os
import sys
import glob

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()


def crea_snp(savfile, dyrfiles):
    # abro el caso
    psspy.case(savfile)

    # ubico archivos conec y conet
    folder = os.path.dirname(savfile)
    conec = os.path.join(folder, os.path.basename(savfile).replace(".sav", "_CC.flx"))
    conet = os.path.join(folder, os.path.basename(savfile).replace(".sav", "_CT.flx"))
    
    # genero el primer dyr
    if len(dyrfiles) == 0:
        raise ValueError("No hay *.dyr a cargar")
    psspy.dyre_new([1,1,1,1], dyrfiles[0], conec, conet, "")

    with open(conec, "r") as cc: cc_lines = cc.readlines()
    with open(conet, "r") as ct: ct_lines = ct.readlines()

    # genero los dyr restantes
    tmp_conec = os.path.join(folder, "tmp_CC.flx")
    tmp_conet = os.path.join(folder, "tmp_CT.flx")
    for dyr in dyrfiles[1:]:
        psspy.dyre_add([_i,_i,_i,_i], dyr, tmp_conec, tmp_conet)
        
        with open(tmp_conec, "r") as cc: tmp_cc_lines = cc.readlines()
        with open(tmp_conet, "r") as ct: tmp_ct_lines = ct.readlines()

        # Inserta nuevas lineas en los archivos CC y CT
        for line in tmp_cc_lines:
            if not line.startswith("C"):
                cc_lines.insert(-3, line)                
               
        for line in tmp_ct_lines:
            if not line.startswith("C") and not "IF (.NOT. IFLAG) GO TO 9000" in line:
                ct_lines.insert(-6, line)
                    
        # limpia los archivos temporales    
        os.remove(tmp_conec)
        os.remove(tmp_conet)
        
    with open(conec, "w") as cc: cc.writelines(cc_lines)
    with open(conet, "w") as ct: ct.writelines(ct_lines)
                
    # guardo el snapshot pero antes ajusto opciones
    psspy.set_netfrq(1)
    psspy.set_osscan(1,0)
    psspy.set_genang_3(1, 180.0,0.0,0)    
    if psspy.busexs(2620) == 0:    
        psspy.set_relang(1,2620,'1')
    psspy.dynamics_solution_param_2([_i,_i,_i,_i,_i,_i,_i,_i],[_f,_f, 0.002,_f,_f,_f,_f,_f])
    ierr = psspy.snap(sfile=savfiles[0].replace(".sav", ".snp"))
    assert ierr == 0


if __name__ == "__main__":   
    savfiles = []
    dyrfiles = []
    for f in sys.argv[1:]:
        if f.endswith(".sav"):
            savfiles.append(os.path.abspath(f))
        if f.endswith(".dyr"):
            dyrfiles.append(os.path.abspath(f))
        
    psspy.psseinit()
    for savfile in savfiles:
        crea_snp(savfile, dyrfiles)

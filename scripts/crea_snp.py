"""
Crea un snapshot de los casos.
Suma opciones para que funcione correctamente en el SADI.
"""

import psse34
import psspy

import argparse
import os

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()


def crea_snp(savfile, snapfile, conec, conet, dyrfiles):
    # abro el caso
    psspy.psseinit()
    psspy.case(savfile)

    # ubico archivos conec y conet
    # folder = os.path.dirname(savfile)
    # conec = os.path.join(folder, os.path.basename(savfile).replace(".sav", "_CC.flx"))
    # conet = os.path.join(folder, os.path.basename(savfile).replace(".sav", "_CT.flx"))
    
    # genero el primer dyr
    if len(dyrfiles) == 0:
        raise ValueError("No hay *.dyr a cargar")
    psspy.dyre_new([1,1,1,1], dyrfiles[0], conec, conet, "")

    with open(conec, "r") as cc: cc_lines = cc.readlines()
    with open(conet, "r") as ct: ct_lines = ct.readlines()

    # genero los dyr restantes
    tmp_conec = conec.replace(".flx", "_tmp.flx")
    tmp_conet = conet.replace(".flx", "_tmp.flx")
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
    ierr = psspy.snap(sfile=snapfile)
    assert ierr == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crea archivo .cnv a partir de .sav y scripts .py.")    
    parser.add_argument("--sav", required=True, help="Caso de entrada .SAV o .CNV")    
    parser.add_argument("--dyr", nargs='+', required=False, help="Archivos dinamicos")
    
    args = parser.parse_args()
    
    basename = os.path.basename(args.sav).replace(".sav", "").replace(".cnv", "")
    conec = "conec/{}.flx".format(basename)
    conet = "conet/{}.flx".format(basename)
    snp   = "snp/{}.snp".format(basename)

    crea_snp(args.sav, snp, conec, conet, args.dyr)


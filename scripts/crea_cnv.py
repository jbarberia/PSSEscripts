# coding: latin-1
"""
Convierte los casos a CNV
"""

import argparse
import psse34
import psspy

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()

def crea_cnv(savfile, outfile, pyfiles):
    """
    Convierte los casos que se pasen en funcion de los pyfiles.
    Si no se pasa ninguno, se toma una conversion estandar.   
    """
    psspy.psseinit()
    psspy.case(savfile)
    
    if not pyfiles:
        psspy.cong(0)
        
        # P (%)
        z_P = 20.0
        i_P = 80.0
        
        # Q (%)
        z_Q = 50.0
        i_Q = 50.0
        
        psspy.conl(0,1,1,[0,0],[ i_P, z_P, i_Q, z_Q])
        psspy.conl(0,1,2,[0,0],[ i_P, z_P, i_Q, z_Q])
        psspy.conl(0,1,3,[0,0],[ i_P, z_P, i_Q, z_Q])        
        
        psspy.ordr(0)    
        psspy.fact()
        psspy.tysl(0)

    else:
        for py in pyfiles:
            execfile(py)       
    
    psspy.save(outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crea archivo .cnv a partir de .sav y scripts .py.")    
    parser.add_argument("--sav", required=True, help="Caso de entrada .SAV")
    parser.add_argument("--cnv", required=True, help="Caso de salida .CNV")
    parser.add_argument("--py", nargs='+', required=False, help="Archivos de conversion de demanda")
    
    args = parser.parse_args()
    
    crea_cnv(args.sav, args.cnv, args.py)

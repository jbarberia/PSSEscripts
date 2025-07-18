# coding: latin-1
"""
Convierte los casos a CNV
"""

import psse34
import psspy
import sys
import os

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()

def crea_cnv(savfile, pyfiles):
    """
    Convierte los casos que se pasen en funcion de los pyfiles.
    Si no se pasa ninguno, se toma una conversion estandar.   
    """
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
    
    psspy.save(savfile.replace(".sav", ".cnv"))


if __name__ == "__main__":   
    savfiles = []
    pyfiles = []
    for f in sys.argv[1:]:
        if f.endswith(".sav"):
            savfiles.append(os.path.abspath(f))
        if f.endswith(".py"):
            pyfiles.append(os.path.abspath(f))
        
    psspy.psseinit()
    for savfile in savfiles:
        crea_cnv(savfile, pyfiles)

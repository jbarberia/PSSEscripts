# coding: latin-1
import argparse
import psse34
import psspy

import os
import sys
import argparse

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Simulacion Dinamica')
    parser.add_argument('files', nargs='*', help='Archivos de entrada (.cnv, .snp, .dll, .py)')
    parser.add_argument('-o', '--outfile', required=True, help='Archivo de salida de la simulacion')

    args = parser.parse_args()

    cnvfiles = []
    snpfiles = []
    dllfiles = []
    idvfiles = []
    pyfiles  = []

    for f in args.files:
        if f.endswith(".cnv"):
            cnvfiles.append(os.path.abspath(f))
        elif f.endswith(".snp"):
            snpfiles.append(os.path.abspath(f))
        elif f.endswith(".dll"):
            dllfiles.append(os.path.abspath(f))
        elif f.endswith(".py"):
            pyfiles.append(os.path.abspath(f))
        elif f.endswith(".idv"):
            idvfiles.append(os.path.abspath(f))

    assert len(cnvfiles) == 1, "Debe haber exactamente un archivo .cnv"
    assert len(snpfiles) == 1, "Debe haber exactamente un archivo .snp"

    cnvfile = cnvfiles[0]
    snpfile = snpfiles[0]

    # Inicia el psse     
    psspy.psseinit()

    # Inicia el caso
    psspy.case(cnvfile)
    psspy.rstr(snpfile)
    
    # Carga los dll
    for dll in dllfiles:
        psspy.addmodellibrary(dll)
   
    # Pone outputfile
    outfile = args.outfile
        
    # Corre cada python (en strt debe estar la variable outfile)
    for py in pyfiles:
        execfile(py)
    
    # Guarda el caso post-falla
    psspy.save(outfile.replace(".outx", ".cnv").replace(".out", ".cnv"))


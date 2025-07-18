# coding: latin-1
"""
Este script corre los ACCC para varios SAVs y un unico juego de archivos SUB, MON, CON
"""
import os
import sys
import shutil

import psse34
import psspy

from unidecode import unidecode

_i = psspy.getdefaultint()
_f = psspy.getdefaultreal()
_s = psspy.getdefaultchar()


# Opciones ---------------------------------------------------------------------
ACCC_OPTIONS = {
    # OPCIONES ACCC
    "tol"    :   _f,
    "OPTACC1":   0, # tap flag, 0 - disable, 1 - step, 2 - direct
    "OPTACC2":   0, # area interchage, 0 - disable
    "OPTACC3":   0, # phase shift, 0 - disable
    "OPTACC4":   0, # dc taps, 0 - disable
    "OPTACC5":   0, # switched shunt, 0 - disable, 1 - enable, 2 - enable cont.
    "OPTACC6":   1, # solution method, 1 - FNSL
    "OPTACC7":   1, # non div. solution, 1 - enable
    "OPTACC8":   0, # induction mach, 0 - stall, 1 - trip
    "OPTACC9":   1, # induction mach failure, 1 - treat as solve
    "OPTACC10":  0, # dispatch mode, 0 - disable

    # OPCIONES ACCIONES CORRECTIVAS
    "OPTCOR1":   0, # corr. actions, 0 - disable, 1 - enable
    "OPTCOR2":   5, # num. powerflows
    "OPTCOR3":   0, # genenerator control
    "OPTCOR4":   0, # load control
    "OPTCOR5":   0, # phase shifter control
    "OPTCOR6":   0, # off-line generator control
    "OPTCOR7":   0, # tap control
    "OPTCOR8":   0, # switched shunt control

    # VALUES
    "VALUES1":  0.1, # bus voltage violation tolerance
    "VALUES2":  0.1, # branch flow violation tolerance
    "VALUES3":  0.1, # generator control weight
    "VALUES4":  0.1, # load control weight
    "VALUES5":  0.1, # phase shifter control weight
    "VALUES6":  0.1, # off-line gen control weight
    "VALUES7":  0.1, # tap settings control weight
    "VALUES8":  0.1, # switched shunt control weight

    # LABELS - NOMBRE DEL SUBSISTEMA DE CONTROL
    "LABELS1":  "", # generator dispatch subsystem, generalmente vacio por OPTACC10 = 0
    "LABELS2":  "", # generator control subsystem
    "LABELS3":  "", # load control subsystem
    "LABELS4":  "", # phase shifter control subsystem
    "LABELS5":  "", # off-line gen control subsystem
    "LABELS6":  "", # tap settings control subsystem
    "LABELS7":  "", # switched shunt control subsystem

    # THROWOVER FILE
    "thrfile":  "",

    # INERTIA FILE
    "inlfile":  "",
}


# Funciones --------------------------------------------------------------------
def chequear_error(fun, ierr, case, comment):
    _, error_string = psspy.apierrstr(fun, ierr)
    case = os.path.basename(case)
    if ierr != 0:
        sys.stderr.write("Error en funcion {} ierr={}, para el caso {}, {}\n{}\n".format(fun, ierr, case, comment, error_string))
        exit(1)
        

def prepara_caso():
    """
    Ajustes para que funcione el modulo de contingencias dentro del SADI
    """
    _i = psspy.getdefaultint()
    _f = psspy.getdefaultreal()
    _s = psspy.getdefaultchar()

    # Reactores zig zags de paraguay en el caso del SADI
    psspy.two_winding_chng_6(95370,99379,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,95370,_i,_i,_i,0,_i,_i,_i],[ 9999.0, 9999.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
    psspy.two_winding_chng_6(95540,95541,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,95541,_i,_i,_i,0,_i,_i,_i],[ 9999.0, 9999.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")
    psspy.two_winding_chng_6(95500,95501,r"""1""",[_i,_i,_i,_i,_i,_i,_i,_i,95501,_i,_i,_i,0,_i,_i,_i],[ 9999.0, 9999.0,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],[_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f,_f],"","")

    # Ajusta strings del titulo para que sean ASCII    
    title_1, title_2 = psspy.titldt()
    psspy.case_title_data(
        unidecode(title_1),
        unidecode(title_2),
    )
    
    ierr = psspy.fnsl([0,0,0,0,0,0,0,0])
    chequear_error("fnsl", ierr, case, "Preparacion flujo de carga")
    assert psspy.solved() == 0


if __name__ == "__main__":
    psspy.psseinit()

    # Lee los archivos de entrada
    files = sys.argv[1:]
    sav = []
    mon = None
    con = None
    sub = None

    for file in files:
        if os.path.isfile(file):
            if file.endswith(".sav"):
                sav.append(file)
            if file.endswith(".mon"):
                mon = file
            if file.endswith(".con"):
                con = file
            if file.endswith(".sub"):
                sub = file
             
    if not sav:
        exit("Falta archivo .sav")
    if not mon:
        exit("Falta archivo .mon")
    if not con:
        exit("Falta archivo .con")
    if not sub:
        exit("Falta archivo .sub")

    # Para cada caso corre ACCC    
    for case in sav:
        psspy.case(case)
        prepara_caso()
        
        basename = os.path.basename(case).replace(".sav", "")
        dfx = os.path.join(case.replace(".sav", ".dfx"))
        psspy.dfax_2([1,1,0], sub, mon, con, dfx)

        accfile = os.path.join(case.replace(".sav", ".acc"))
        tmp_zipfile = os.path.join(os.path.expanduser("~"), basename + ".zip") # Evita problemas de permisos con gdrive
        
        # Corre este para obtener el zip file
        ierr = psspy.accc_with_dsp_3(
            dfxfile=dfx,
            accfile=accfile,
            zipfile=tmp_zipfile,
            optacc11=1,
            **ACCC_OPTIONS
        )
        chequear_error("accc_with_dsp_3", ierr, case, "ACCC")

        zipfile = os.path.join(case.replace(".sav", ".zip"))
        shutil.move(tmp_zipfile, zipfile)

        # Corre ACCC con acciones correctivas
        psspy.case(case)
        prepara_caso()

        ierr = psspy.accc_with_cor_3(
            dfxfile=dfx,
            accfile=accfile,
            **ACCC_OPTIONS
        )
        chequear_error("accc_with_cor_3", ierr, case, "ACCC con acciones correctivas")

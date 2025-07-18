# coding: latin-1
"""
Compila los archivos fuente y de libreria en una determinada carpeta para generar el dsurs.dll
"""

import os
import sys
import argparse

import psse34
import psse_env_manager

path_str = [
    r"C:\Program Files (x86)\Intel\oneAPI\compiler\2024.1\bin32",
    r"C:\Program Files (x86)\Intel\oneAPI\compiler\2024.1\bin",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\bin\Hostx86\x86",
    r"C:\Program Files (x86)\Windows Kits\10\bin\10.0.19041.0\x86",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE",
    r"C:\Users\User\Desktop\Usuarios_PSSE\Lib",
]

lib_str = [
    r"C:\Program Files (x86)\Intel\oneAPI\compiler\2024.1\lib32",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\lib\x86",
    r"C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\um\x86",
    r"C:\Program Files (x86)\Windows Kits\10\Lib\10.0.19041.0\ucrt\x86",
    r"C:\Users\User\Desktop\Usuarios_PSSE\Lib",
]

incl_str = [
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\include",
    r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Tools\MSVC\14.29.30133\atlmfc\include",
    r"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\um",
    r"C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\shared",
]

os.environ['PATH']    = ";".join(path_str)
os.environ['LIB']     = ";".join(lib_str)
os.environ['INCLUDE'] = ";".join(incl_str)


def compila(dllname, files):
    # remueve archivos viejos
    if os.path.isfile(dllname): os.remove(dllname)

    # src files
    src_lst = []
    for ext in ['.flx','.f','.for','.f90']:       #include conec & conet files
        for f in files:
            if f.endswith(ext):
                src_lst.append(f)

    # obj files
    objlibfiles = []
    for ext in ['.obj', '.lib']:
        for f in files:
            if f.endswith(ext):
                objlibfiles.append(f)

    psse_vrsn = 34
    ivfversion = 18
    addopstr = psse_env_manager.ivf_compiler_options_add(ivfversion, "/Qdiag-disable:10448")
    addopstr = psse_env_manager.ivf_compiler_options_add(ivfversion, "/Qm32")

    ierr = psse_env_manager.create_dll(psse_vrsn, src_lst, modsources=[], 
        objlibfiles=objlibfiles, dllname=dllname, workdir=os.path.dirname(dllname), showprg=True,
        useivfvrsn=ivfversion, shortname='DSUSR', description='User Model',
        majorversion=1, minorversion=0, buildversion=0, companyname='', mypathlib=False,
        keep=False, keepf=False)
    
    assert ierr == 0
    
    # retiro .lib
    os.remove(dllname.replace(".dll", ".lib"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compilador de modelos de PSSE')    
    parser.add_argument('files', nargs='+', help='Archivos .lib .f .for .f90 .flx')
    parser.add_argument('-o', '--output', default='dsusr.dll', help='Archivo de salida .dll')
    args = parser.parse_args()
    
    files = [os.path.abspath(f) for f in args.files]    
    compila(args.output, files)

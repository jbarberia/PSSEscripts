# coding: latin-1
import subprocess
import os
import sys
import tempfile


def parallel_run(*args):
    "Corre las rutinas en paralelo e imprime cada una en orden"
    processes = []
    for c in args:
        f = tempfile.TemporaryFile()
        p = subprocess.Popen(c, stdout=f)
        processes.append((c, p, f))

    for c, p, f in processes:    
        p.wait()
        f.seek(0)
        output = f.read().decode(errors="ignore")
        f.close()
        
        output = output.replace("\r\n", "\n\t")
        
        if p.returncode != 0:
            sys.stderr.write("ERROR EN: {}\n".format(c))
            print("ERROR EN:", )        
        print(c)
        print(output)


carpetas = ["sav", "cnv", "acc", "dfx", "zip", "snp", "dyr", "conec", "conet", "dll"]
carpetas += [
    "reporte_accc",
    "reporte_ascc"
]
for c in carpetas:
    os.makedirs(c, exist_ok=True)


# EDITAR ABAJO -----------------------------------------------------------------

savfiles = [
    r"sav\inv24hr.sav", 
    r"sav\inv24pi.sav", 
    r"sav\inv24va.sav", 
    r"sav\ver2425pid.sav", 
    r"sav\ver2425pin.sav", 
    r"sav\ver2425va.sav", 
]

SUB = r"sav\estatico.sub"
MON = r"sav\estatico.mon"
CON = r"sav\estativo.con"

# Corridas ACCC
accc = []
for sav in savfiles:
    accc.append('python2 scripts/accc.py --sav "{}" --mon "{}" --con "{}" --sub "{}"'.format(sav, MON, CON, SUB))
parallel_run(*accc)

# Reportes ACCC
reportes_accc = []
for acc in filter(lambda s: s.endswith(".acc"), os.listdir("acc")):    
    reportes_accc.append('python2 scripts/reporte_accc.py --acc "acc/{}" --xlsx "reporte_accc/{}"'.format(acc, acc.replace(".acc", ".xlsx")))
parallel_run(*reportes_accc)

# # Crea CNV
# conversion_cnv = []
# for sav in savfiles:
#     conversion_cnv.append('python2 scripts/crea_cnv.py --sav "{}" --cnv "cnv/{}"'.format(sav, os.path.basename(sav).replace(".sav", ".cnv")))
# parallel_run(*conversion_cnv)

# # Crea SNP
# creacion_snp = []
# dyrfiles = " ".join(['"dyr/{}"'.format(f) for f in os.listdir("dyr") if f.endswith(".dyr")])
# for sav in savfiles:
#     creacion_snp.append('python2 scripts/crea_snp.py --sav "{}" --dyr {}'.format(sav, dyrfiles))
# parallel_run(*creacion_snp)

# # Crea DLL - no se corre en paralelo porque trae problemas en PSSE ENV MNG
# compilacion = []
# for snp in os.listdir("snp"):
#     basename = os.path.basename(snp).removesuffix(".snp")
#     sources = ""
#     sources += ' "conec/{}.flx"'.format(basename)
#     sources += ' "conet/{}.flx"'.format(basename)
#     sources += ' lib/mod3424_1.lib'

#     out = "dll/" + basename + ".dll"
#     compilacion.append('python2 scripts/compila.py --files {} -o {}'.format(sources, out))
#     parallel_run(compilacion[-1])




        
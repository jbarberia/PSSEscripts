# coding: latin-1
from itertools import product
import os
import shutil
import subprocess
import argparse
import time

PSSPLT = r"C:\Program Files (x86)\PTI\PSSE34\PSSBIN\PSSPLT34.exe"
PRINTER_OUTPUT = r"C:\Users\User\Documents\ms_print.pdf"

if __name__ == "__main__":   
    parser = argparse.ArgumentParser(description='Impresión en batch de Outfiles')    
    parser.add_argument('--outfiles', nargs='+', help='Archivos de outx y out')
    parser.add_argument('--idvfiles', nargs='+', help='Archivos idv para graficar')
    parser.add_argument('-o', '--output_folder', default=".", help='Archivo de salida pdf')

    args = parser.parse_args()

    for idv, outfile in product(args.outfiles, args.idvfiles):
        with open(idv) as infile:
            with open('tmp.idv', 'w') as tmpfile:
                data = infile.read()
                data = data.replace('%1%', outfile)
                tmpfile.write(data)
                
        subprocess.run([PSSPLT, "-inpdev", tmpfile])
        time.sleep(2)
        
        os.remove(tmpfile)
        out_basename = os.path.basename(outfile).replace(".outx", "").replace(".out", "")
        idv_basename = os.path.basename(idv).replace(".idv", "")
        output = os.path.join(args.output_folder, "{}-{}.pdf".format(out_basename, idv_basename))
        shutil.move(PRINTER_OUTPUT, output)

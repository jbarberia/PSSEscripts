import sys
import psse34
import pssexcel

import argparse
import psse34
import pssexcel

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convertir archivo .acc a .xlsx con pssexcel.")
    parser.add_argument("--acc", help="Ruta al archivo .acc")
    parser.add_argument(
        "--xlsx",
        help="Ruta de salida del archivo .xlsx (por defecto, mismo nombre que accfile)",
        default=None
    )

    args = parser.parse_args()

    pssexcel.accc(
        args.acc,
        ['s','v','g','l','b','i', 'w'],
        show=False,
        namesplit=False,    
        xlsfile=args.xlsx)

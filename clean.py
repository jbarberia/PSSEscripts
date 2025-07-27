"""
Limpia las carpetas de archivos temporales.
"""

import os

carpetas = ["cnv", "acc", "dfx", "zip", "snp", "conec", "conet", "dll"]
carpetas += [
    "reporte_accc",
    "reporte_ascc"
]

for c in carpetas:
    files = os.listdir(c)
    for f in files:
        path = os.path.join(c, f)
        if os.path.isfile(path):
            os.remove(path)

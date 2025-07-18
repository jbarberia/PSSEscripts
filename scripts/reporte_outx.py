# coding: latin-1
import os
import sys
import psse34
import pssplot
# import dyntools
import argparse

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

cm = 1/2.54
plt.style.use('seaborn-bright')
mpl.rcParams.update({             
    'font.size':    7.5,
    'figure.autolayout': True,
    'figure.figsize': (15*cm, 7*cm),
    'savefig.dpi': 300,
    'legend.fontsize': 'small',
    'legend.loc': 'best',
    'legend.frameon': False, 
    
})



def tipo_simulacion(columnas):
    "determina el tipo de simulacion para cambiar el tipo de grafico a realizar"
    col_short = columnas.map(lambda x: x[:4])
    col_short = col_short.unique().sort_values().tolist()
       
    if col_short == ["PMEC", "SPD "]:
        return "GOVERNOR"
    elif col_short == ['ETRM', 'VREF']:
        return "EXCITER"        
    else:
        return "SISTEMA"
    




def plot(outfile):
    ierr, strtitle1, strtitle2, stridents, fchandata, ftimedata = pssplot.getoutxdata(outfile)
    
    path = outfile.replace(".outx", "").replace(".out", "")
    title = os.path.basename(outfile.replace(".outx", "").replace(".out", ""))
   
    df = pd.DataFrame(fchandata).T
    df.columns = stridents
    df.index = ftimedata[0]
    
    simulacion = tipo_simulacion(df.columns)
    
    if simulacion == "GOVERNOR" or simulacion == "EXCITER":
        maquinas = df.columns.map(lambda s: s.split("[")[-1]).unique()
        maquinas = maquinas.map(lambda s: s.split("BUS")[-1]).unique()
        
        for maquina in maquinas:
            chan = df.filter(regex=".*" + maquina)
            nombre_maquina = maquina.split(" ")[0]
            
            if simulacion == "GOVERNOR":
                sorted_chan = chan.columns.sort_values()
                
                ax1 = chan[sorted_chan[0]].plot(label=sorted_chan[0])
                ax1.set_ylabel(sorted_chan[0][:4])
                
                ax2 = ax1.twinx()
                chan[sorted_chan[1]].plot(ax=ax2, color="C1", label=sorted_chan[1])
                ax2.set_ylabel(sorted_chan[1][:4])
                               
                ax1.set_title(title)
                ax1.set_xlabel("Tiempo (s)")
                plt.savefig(path + "_" + nombre_maquina + "_" + simulacion + ".png")
                plt.gcf().clear()
                           
            else:            
                ax = chan.plot()
                ax.set_ylabel(" / ".join(chan.columns.str[:4]))
                ax.set_title(title)
                ax.set_xlabel("Tiempo (s)")
                plt.savefig(path + "_" + nombre_maquina + "_" + simulacion + ".png")
                plt.gcf().clear()

                
    elif simulacion == "SISTEMA":
                        
        chan_filter = lambda x: df.filter(regex=x)
        angulos   = chan_filter(r"^ANGL")
        tensiones = chan_filter(r"^VOLT")
        flujos    = chan_filter(r"^POWR.* TO")
        frec      = chan_filter(r"^FREQ") * 50 + 50
        maquinas  = chan_filter(r"^POWR(?!.*\bTO\b)")
                                      
        if not angulos.empty:
            ax = angulos.plot()
            ax.set_ylim(-100.0, 100.0)    
            ax.set_title(title)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel(u"ANGL (grados)")    
            plt.savefig(path + "_ANGULOS.png")
            plt.gcf().clear()
        
        if not tensiones.empty:        
            ax = tensiones.plot()
            ax.set_ylim(0.0, 1.2)   
            ax.set_xlim(0.0, 10)
            ax.set_title(title)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel(u"VOLT (pu)")
            plt.savefig(path + "_TENSIONES.png")
            plt.gcf().clear()
            
        if not flujos.empty:
            ax = flujos.plot()
            ax.set_title(title)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("MW")
            plt.savefig(path + "_FLUJOS.png")
            plt.gcf().clear()
            
        if not maquinas.empty:
            ax = maquinas.plot()
            ax.set_title(title)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel(u"MW (pu en base de Mquina)")
            plt.savefig(path + "_GENMW.png")
            plt.gcf().clear()

        if not frec.empty:                   
            ax = frec.plot()
            ax.set_ylim(48, 52)
            ax.set_title(title)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("FREC (Hz)")    
            plt.savefig(path + "_FRECUENCIA.png")
            plt.gcf().clear()
            
            
    
    
    
    
    
    






if __name__ == "__main__":   
       
    outfiles = []
    for f in sys.argv[1:]:
        if f.endswith(".outx") or f.endswith(".out"):
            outfiles.append(os.path.abspath(f))
    
    for outfile in outfiles:
        plot(outfile)
    
    

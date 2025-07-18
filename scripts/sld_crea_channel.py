"""
Este script permite obtener las lineas del archivo *.psa
Se deben seleccionar todas los elementos en el SLD a monitorear

#TODO deberia evolucionar a otro tipo de script.
"""

import psse34
import psspy
import re
import sliderPy


def content_selection():
    "Monitoreo los elementos seleccionados en el SLD"
    mydoc = sliderPy.GetActiveDocument()
    diagram = mydoc.GetDiagram()
    components = diagram.GetComponents()

    channel = []
    for component in components:
        if component.IsSelected() == False:
            continue
        
        map_string = re.findall(r"\S+", component.GetMapString())
        if len(map_string) == 0:
            continue

        if map_string[0] in ["BU"]:#, "ME", "SWS", "LO", "FXS"]:
            busi = int(map_string[1])
            channel.append("PLACE VOLT&ANG at BUS {} IN CHANNEL".format(busi))
            channel.append("PLACE BSFREQ   at BUS {} IN CHANNEL".format(busi))
            channel.append("")
        
        if map_string[0] in ["ME"]:
            busi = int(map_string[1])
            id = str(map_string[2])
            channel.append("PLACE ANGLE from BUS {} MACHINE {} IN CHANNEL".format(busi, id))
            channel.append("PLACE PELEC from BUS {} MACHINE {} IN CHANNEL".format(busi, id))
            channel.append("PLACE QELEC from BUS {} MACHINE {} IN CHANNEL".format(busi, id))
            channel.append("")

        elif map_string[0] == "T3":
            busi = int(map_string[1])
            busj = int(map_string[2])
            busk = int(map_string[3])
            ckt = map_string[4]

            channel.append("PLACE 3WNDFLOWPQ  from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busi, busj, busk, ckt))
            channel.append("PLACE 3WNDFLOWMVA from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busi, busj, busk, ckt))
            channel.append("PLACE 3WNDRELAY3  from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busi, busj, busk, ckt))
            channel.append("")
            channel.append("PLACE 3WNDFLOWPQ  from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busj, busk, busi, ckt))
            channel.append("PLACE 3WNDFLOWMVA from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busj, busk, busi, ckt))
            channel.append("PLACE 3WNDRELAY3  from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busj, busk, busi, ckt))
            channel.append("")
            channel.append("PLACE 3WNDFLOWPQ  from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busk, busi, busj, ckt))
            channel.append("PLACE 3WNDFLOWMVA from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busk, busi, busj, ckt))
            channel.append("PLACE 3WNDRELAY3  from BUS {} TO BUS {} TO BUS {} CKT {} IN CHANNEL".format(busk, busi, busj, ckt))
            channel.append("")

        elif map_string[0] in ["TR", "SYS", "LII"]:
            busi = int(map_string[1])
            busj = int(map_string[2])
            ckt = map_string[3]
            channel.append("PLACE FLOWPQ  from BUS {} TO BUS {} CKT {} IN CHANNEL".format(busi, busj, ckt))
            channel.append("PLACE FLOWMVA from BUS {} TO BUS {} CKT {} IN CHANNEL".format(busi, busj, ckt))
            channel.append("PLACE RELAY2  from BUS {} TO BUS {} CKT {} IN CHANNEL".format(busi, busj, ckt))
            channel.append("")
            channel.append("PLACE FLOWPQ  from BUS {} TO BUS {} CKT {} IN CHANNEL".format(busj, busi, ckt))
            channel.append("PLACE FLOWMVA from BUS {} TO BUS {} CKT {} IN CHANNEL".format(busj, busi, ckt))
            channel.append("PLACE RELAY2  from BUS {} TO BUS {} CKT {} IN CHANNEL".format(busj, busi, ckt))
            channel.append("")
            
    return "\n".join(channel)


if __name__ == "__main__":
    channel = content_selection()
    psspy.beginreport()
    psspy.report(channel)    

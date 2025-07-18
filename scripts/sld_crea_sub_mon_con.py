# coding: latin-1
"""
Este script permite obtener los archivo de configuración
Se deben seleccionar todas los elementos en el SLD a monitorear
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

    subsystem = []
    monitor = []
    contingency = []
    for component in components:
        if component.IsSelected() == False:
            continue
        
        map_string = re.findall(r"\S+", component.GetMapString())
        if len(map_string) == 0:
            continue

        if map_string[0] in ["BU", "ME", "SWS", "LO", "FXS"]:
            busi = int(map_string[1])
            monitor.append("MONITOR VOLTAGE LIMIT BUS {}".format(busi))
            subsystem.append("BUS {}".format(busi))
            # monitor.append("MONITOR VOLTAGE DEVIATION BUS {} 0.01 0.01".format(busi))
        
        if map_string[0] in ["ME"]:
            busi = int(map_string[1])
            contingency.append("CONTINGENCY GEN-{}".format(busi))
            contingency.append("DISCONNECT BUS {}".format(busi))
            contingency.append("END")

        elif map_string[0] == "T3":
            busi = int(map_string[1])
            busj = int(map_string[2])
            busk = int(map_string[3])
            ckt = map_string[4]
                                  
            monitor.append("MONITOR BRANCH FROM BUS {} TO BUS {} TO BUS {} CKT {}".format(busi, busj, busk, ckt))
            
            contingency.append("CONTINGENCY {}-{}-{}-{}".format(busi, busj, busk, ckt))
            contingency.append("OPEN BRANCH FROM BUS {} TO BUS {} TO BUS {} CIRCUIT {}".format(busi, busj, busk, ckt))
            contingency.append("END")

        elif map_string[0] in ["TR", "SYS", "LII"]:
            busi = int(map_string[1])
            busj = int(map_string[2])
            ckt = map_string[3]
            
            monitor.append("MONITOR BRANCH FROM BUS {} TO BUS {} CKT {}".format(busi, busj, ckt))
            
            contingency.append("CONTINGENCY {}-{}-{}".format(busi, busj, ckt))
            contingency.append("OPEN BRANCH FROM BUS {} TO BUS {} CKT {}".format(busi, busj, ckt))
            contingency.append("END")
            
    return "\n".join(subsystem), "\n".join(monitor), "\n".join(contingency)


if __name__ == "__main__":
    sub_content, mon_content, con_content = content_selection()

    psspy.beginreport()
    psspy.report("SUBSYSTEM 'SYSTEM'\n")
    psspy.report(sub_content)
    psspy.report("\nEND")
    psspy.report("\nEND")

    psspy.beginreport()
    psspy.report(con_content)
    psspy.report("\nEND")

    psspy.beginreport()
    psspy.report(mon_content)
    psspy.report("\nEND")

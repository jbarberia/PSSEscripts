import os
import sys
import psse34
import psspy
import pssarrays
import pandas as pd
import numpy as np

psspy.psseinit()

def get_bus_voltage_df(solutions):
    bus_voltage_dfs = []
    for solution in solutions:
        bus_voltage = pd.DataFrame()
        bus_voltage["BUS"] = solution.mvbuslabel
        bus_voltage["MIN"] = solution.mvrecmin
        bus_voltage["MAX"] = solution.mvrecmax
        bus_voltage["CONTINGENCY"] = solution.solncolbl
        bus_voltage["SOLUTION TYPE"] = solution.stype
        bus_voltage["VOLTS"] = solution.volts
        bus_voltage_dfs.append(bus_voltage)

    
    bus_voltage = pd.concat(bus_voltage_dfs)
    if bus_voltage.empty:
        return bus_voltage
    base_case = bus_voltage[bus_voltage.CONTINGENCY == "BASE CASE"]
    base_case_volts = base_case.set_index("BUS").VOLTS
    bus_voltage["BASE VOLTS"] = bus_voltage.apply(
        lambda x: base_case_volts[x.BUS], axis=1
    )
    bus_voltage["DEVIATION"] = bus_voltage["VOLTS"] - bus_voltage["BASE VOLTS"]
    return bus_voltage


def get_branch_flow_df(solutions):
    branch_flow_dfs = []
    for solution in solutions:
        branch_flow = pd.DataFrame()
        branch_flow["BRANCH"] = solution.melement
        branch_flow["CONTINGENCY"] = solution.solncolbl
        branch_flow["SOLUTION TYPE"] = solution.stype
        branch_flow["MVA FLOW"] = solution.mvaflow
        branch_flow["MW FLOW"] = solution.brnpflow
        branch_flow["MVAR FLOW"] = solution.brnqflow
        branch_flow["I as MVA"] = solution.ampflow
        branch_flow["RATE"] = solution.rate
        branch_flow_dfs.append(branch_flow)
    branch_flow = pd.concat(branch_flow_dfs)
    branch_flow["LOADING"] = abs(branch_flow["I as MVA"]) / branch_flow["RATE"] * 100
    branch_flow["LOADING"] = branch_flow["LOADING"].replace([np.inf, -np.inf], 0)
    return branch_flow


def get_load_shed_df(solutions):
    load_shed_df = []
    for solution in solutions:
        load_shed = pd.DataFrame()
        load_shed["BUS"] = solution.lshedbus
        load_shed["CONTINGENCY"] = solution.solncolbl
        load_shed["SOLUTION TYPE"] = solution.stype
        if load_shed.empty:
            continue
        load_shed["BASE LOAD"] = solution.loadshed[0]
        load_shed["CONT LOAD"] = solution.loadshed[1]
        load_shed["LOAD SHED"] = load_shed["BASE LOAD"] - load_shed["CONT LOAD"]
        load_shed_df.append(load_shed)

    if len(load_shed_df) > 0:
        load_shed = pd.concat(load_shed_df)
    else:
        load_shed = pd.DataFrame(
            columns=[
                "BUS",
                "CONTINGENCY",
                "SOLUTION TYPE",
                "BASE LOAD",
                "CONT LOAD",
                "LOAD SHED",
            ]
        )
    return load_shed


def get_gen_dispatch_df(solutions):
    gen_dispatch_df = []
    for solution in solutions:
        if not "gdispbus" in solution.keys():
            continue
        gen_dispatch = pd.DataFrame()
        gen_dispatch["BUS"] = solution.gdispbus
        gen_dispatch["CONTINGENCY"] = solution.solncolbl
        gen_dispatch["SOLUTION TYPE"] = solution.stype
        gen_dispatch["BASE GEN"] = solution.gendisp[0]
        gen_dispatch["CONT GEN"] = solution.gendisp[1]
        gen_dispatch["DIFF GEN"] = gen_dispatch["CONT GEN"] - gen_dispatch["BASE GEN"]
        gen_dispatch_df.append(gen_dispatch)

    if len(gen_dispatch_df) > 0:
        gen_dispatch = pd.concat(gen_dispatch_df)
    else:
        gen_dispatch = pd.DataFrame(
            columns=[
                "BUS",
                "CONTINGENCY",
                "SOLUTION TYPE",
                "BASE GEN",
                "CONT GEN",
                "DIFF GEN",
            ]
        )
    return gen_dispatch


if __name__ == "__main__":
    
    accfile = sys.argv[1]
    output_folder = os.path.dirname(accfile)
    acc_basename = os.path.basename(accfile)

    accsum = pssarrays.accc_summary(accfile)
    solutions = []
    for stype in ["CONTINGENCY", "CORRECTIVE ACTION"]:
        for colabel in accsum.colabel:
            accsol = pssarrays.accc_solution(accfile, colabel, stype)
            if accsol:
                accsol["stype"] = stype
                accsol["melement"] = accsum.melement
                accsol["rate"] = accsum.rating.a
                accsol["mvbuslabel"] = accsum.mvbuslabel
                accsol["mvrecmax"] = accsum.mvrecmax
                accsol["mvrecmin"] = accsum.mvrecmin
                solutions.append(accsol)

                if colabel == "BASE CASE":
                    pssarrays.accc_violations_report(
                        accfile,
                        stype,
                        0.5,
                        5,
                        "a",
                        80,
                        os.path.abspath(
                            os.path.join(
                                output_folder,
                                acc_basename.replace(".acc", "_{}.txt".format(stype.lower()))
                            ),
                        ),
                    )

    psspy.accc_single_run_report_5(
        [5,1,2,1,1,1,1,0,1,0,0,0,1,1],
        [0,0,0,0,6000],
        [ 0.5, 5.0, 100.0,0.0,0.0,0.0, 99999.],
        accfile,
    )

    psspy.accc_single_run_report_5(
        [0,1,1,1,1,1,1,0,1,0,0,0,1,1],
        [0,0,0,0,6000],
        [ 0.5, 5.0, 100.0,0.0,0.0,0.0, 99999.],
        accfile
    )

    bus_voltage = get_bus_voltage_df(solutions)
    branch_flow = get_branch_flow_df(solutions)
    load_shed = get_load_shed_df(solutions)
    gen_dispatch = get_gen_dispatch_df(solutions)
    
    excel_file = os.path.abspath(os.path.join(
        output_folder,
        acc_basename.replace(".acc", ".xlsx"))
    )

    with pd.ExcelWriter(
        excel_file, engine="xlsxwriter"
    ) as writer:
        
        # Normal columns
        bus_voltage.to_excel(writer, sheet_name="Bus Voltage", index=False, float_format='%.4f')
        branch_flow.to_excel(writer, sheet_name="Branch Flow", index=False, float_format='%.2f')
        load_shed.to_excel(writer, sheet_name="Load Shed", index=False, float_format='%.2f')
        gen_dispatch.to_excel(writer, sheet_name="Generator Dispatch", index=False, float_format='%.2f')

        # Pivot DF
        sort_contingency = lambda df: df[["BASE CASE"] + df.columns[df.columns != "BASE CASE"].tolist()]

        if not bus_voltage.empty:
            pivot_bus_voltage = sort_contingency(bus_voltage.pivot_table("VOLTS", "BUS", "CONTINGENCY"))
            pivot_bus_voltage.to_excel(writer, sheet_name="Pivot Bus Voltage", index=True, float_format='%.4f')
        
        if not branch_flow.empty:
            pivot_branch_flow = sort_contingency(branch_flow.pivot_table("LOADING", "BRANCH", "CONTINGENCY"))
            pivot_branch_flow.to_excel(writer, sheet_name="Pivot Branch Loading", index=True, float_format='%.2f')
        
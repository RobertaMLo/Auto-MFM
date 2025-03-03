from cerebellum.analysis.spiking_results import (
    BasicSimulationReport
)

from bsb import from_storage

from cerebellum.analysis.structure_analysis import CellPlacement3D, StructureReport

# codice della Mary che mi fa il report di reco e sim.
reco_file = "mouse_cerebellum.hdf5"

sim_name = "basal_activity" #simulation name set in the scaffold (hdf5 file)

scaffold = from_storage(reco_file)
print('\n\n====================\nHere yours parameters set in the network!!!!!!!!!\n====================')
print('Granule Cells')
print(scaffold.simulations[sim_name].cell_models["granule_cell"].constants)
print('Golgi Cells')
print(scaffold.simulations[sim_name].cell_models["golgi_cell"].constants)
print('Stellate')
print(scaffold.simulations[sim_name].cell_models["stellate_cell"].constants)
print('Basket cells')
print(scaffold.simulations[sim_name].cell_models["basket_cell"].constants)
print('Putkinje')
print(scaffold.simulations[sim_name].cell_models["purkinje_cell"].constants)


#print(scaffold.simulations["basal_activity"].connection_models["stellate_to_stellate"].weight)
#print(scaffold.simulations["basal_activity"].connection_models["basket_to_basket"].synapse["weight"])

# RECONSTRUCTION REPORT
#reco_pdf = "mouse_cerebellum.pdf"
#print('\n====================\nI am building your reconstruction report: ',reco_pdf,'\n====================') 
#report_struct = StructureReport(reco_file)
#report_struct.print_report(reco_pdf)

# SIMULATION REPORT - basal activity - se voglio reco commento ( e anche gli input li commento di conseguenza)
nio_folder = "./new_nios_zplusIe400/nio_files_4"
sim_basal_pdf = "nio_files_4.pdf"

print('=====================\nI am building simulation report: ',sim_basal_pdf,'for sim stored in: ', nio_folder,'\n====================') 

report_sim = BasicSimulationReport(
    scaffold, simulation_name=sim_name, folder_nio=nio_folder
)
report_sim.print_report(sim_basal_pdf)


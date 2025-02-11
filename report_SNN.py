#from cerebellum.analysis.spiking_results import (
#    BasicSimulationReport
#)

from bsb import from_storage

#from cerebellum.analysis.structure_analysis import CellPlacement3D, StructureReport

# codice della Mary che mi fa il report di reco e sim.
#reco_file = "mouse_cerebellum.hdf5"
reco_file = "morphologies.hdf5"
reco_pdf = "reco_awake.pdf"
scaffold = from_storage(reco_file)

print('Granule Cells')
print(scaffold.simulations["basal_activity"].cell_models["granule_cell"].constants)
print('Golgi Cells')
print(scaffold.simulations["basal_activity"].cell_models["golgi_cell"].constants)
print('Stellate')
print(scaffold.simulations["basal_activity"].cell_models["stellate_cell"].constants)
print('Basket cells')
print(scaffold.simulations["basal_activity"].cell_models["basket_cell"].constants)
print('Putkinje')
print(scaffold.simulations["basal_activity"].cell_models["purkinje_cell"].constants)


#print(scaffold.simulations["basal_activity"].connection_models["stellate_to_stellate"].weight)
#print(scaffold.simulations["basal_activity"].connection_models["basket_to_basket"].synapse["weight"])

# RECONSTRUCTION REPORT - se voglio sim commento
#report_struct = StructureReport(reco_file)
#report_struct.print_report(reco_pdf)

# SIMULATION REPORT - basal activity - se voglio reco commento ( e anche gli input li commento di conseguenza)
"""
nio_folder = "./new_nios_plus/nio_files_4"
sim_basal_pdf = "nio_files_4.pdf"
report_sim = BasicSimulationReport(
    scaffold, simulation_name="basal_activity", folder_nio=nio_folder
)
report_sim.print_report(sim_basal_pdf)
"""

from cerebellum.analysis.spiking_results import (
    BasicSimulationReport
)

from bsb import from_storage

from cerebellum.analysis.structure_analysis import CellPlacement3D, StructureReport

# codice della Mary che mi fa il report di reco e sim.
reco_file = "mouse_cerebellum.hdf5" ## THIS IS AWAKEEEEEEEE
#reco_file = "mouse_cereb_nest.hdf5" ##THIS IS IN VITROOOOOO 

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



print('*** SYNAPTIC PARAMETERS ***')
print('glomerulus_to_granule')
print(scaffold.simulations[sim_name].connection_models["glomerulus_to_granule"].synapse["weight"])

print('glomerulus_to_golgi')
print(scaffold.simulations[sim_name].connection_models["glomerulus_to_golgi"].synapse["weight"])

print('golgi_to_granule (glom in SNN)')
print(scaffold.simulations[sim_name].connection_models["golgi_to_glomerulus"].synapse["weight"])

print('golgi_to_golgi')
print(scaffold.simulations[sim_name].connection_models["golgi_to_golgi"].synapse["weight"])

print('ascending_axon_to_golgi')
print(scaffold.simulations[sim_name].connection_models["ascending_axon_to_golgi"].synapse["weight"])

print('ascending_axon_to_purkinje')
print(scaffold.simulations[sim_name].connection_models["ascending_axon_to_purkinje"].synapse["weight"])

print('parallel_fiber_to_golgi')
print(scaffold.simulations[sim_name].connection_models["parallel_fiber_to_golgi"].synapse["weight"])

print('parallel_fiber_to_purkinje')
print(scaffold.simulations[sim_name].connection_models["parallel_fiber_to_purkinje"].synapse["weight"])

print('parallel_fiber_to_stellate')
print(scaffold.simulations[sim_name].connection_models["parallel_fiber_to_stellate"].synapse["weight"])

print('parallel_fiber_to_basket')
print(scaffold.simulations[sim_name].connection_models["parallel_fiber_to_basket"].synapse["weight"])

print('stellate_to_purkinje')
print(scaffold.simulations[sim_name].connection_models["stellate_to_purkinje"].synapse["weight"])

print('basket_to_purkinje')
print(scaffold.simulations[sim_name].connection_models["basket_to_purkinje"].synapse["weight"])

print('stellate_to_stellate')
print(scaffold.simulations[sim_name].connection_models["stellate_to_stellate"].synapse["weight"])

print('basket_to_basket')
print(scaffold.simulations[sim_name].connection_models["basket_to_basket"].synapse["weight"])


# RECONSTRUCTION REPORT
reco_pdf = "mouse_cerebellum_awake.pdf"
#reco_pdf = "mouse_cerebellum2.pdf"
print('\n====================\nI am building your reconstruction report: ',reco_pdf,'\n====================') 
report_struct = StructureReport(reco_file)
report_struct.print_report(reco_pdf)

# SIMULATION REPORT - basal activity - se voglio reco commento ( e anche gli input li commento di conseguenza)
#nio_folder = "./new_nios_zplusIe400/nio_files_40"
#sim_basal_pdf = "nio_files_40.pdf"

#print('=====================\nI am building simulation report: ',sim_basal_pdf,'for sim stored in: ', nio_folder,'\n====================') 

#report_sim = BasicSimulationReport(
#    scaffold, simulation_name=sim_name, folder_nio=nio_folder
#)
#report_sim.print_report(sim_basal_pdf)


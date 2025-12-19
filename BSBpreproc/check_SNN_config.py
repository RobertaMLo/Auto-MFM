from cerebellum.analysis.spiking_results import (
    BasicSimulationReport
)

from bsb import from_storage

from cerebellum.analysis.structure_analysis import CellPlacement3D, StructureReport

reco_file = "mouse_cerebellum.hdf5"

sim_name = "basal_activity" #simulation name set in the scaffold (hdf5 file)

scaffold = from_storage(reco_file)
print('\n\n====================\nHere yours parameters set in the network!!!!!!!!!\n====================')

print('\n\n *** CELL PARAMETERS ***')
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



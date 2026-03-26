#!/bin/bash

folder_nio="/new_nios_vitro/new_nios_vitro_40"

conn_ag='ascending_axon_to_golgi'
conn_ap='ascending_axon_to_purkinje'
conn_bb='basket_to_basket'
conn_bp='basket_to_purkinje'
conn_glg='glomerulus_to_golgi'
conn_glgr='glomerulus_to_granule'
conn_ggl='golgi_to_glomerulus'
conn_gg='golgi_to_golgi'
conn_mg='mossy_fibers_to_glomerulus'
conn_pb='parallel_fiber_to_basket'
conn_pg='parallel_fiber_to_golgi'
conn_pp='parallel_fiber_to_purkinje'
conn_ps='parallel_fiber_to_stellate'
conn_sp='stellate_to_purkinje'
conn_ss='stellate_to_stellate'


python3 analysis_plv.py -conn $conn_ag -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_ap -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_bb -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_bp -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_glg -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_glgr -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_ggl -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_gg -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_mg -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_pg -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_sp -folder_nio $folder_nio
python3 analysis_plv.py -conn $conn_ss -folder_nio $folder_nio


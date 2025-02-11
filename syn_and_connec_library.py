"""
Configurations of the network_scaffold
"""
from __future__ import print_function
import numpy as np


def get_connectivity_and_synapses_matrix(NAME, SI_units=True, number=5):


    # creating empty arry of objects (future dictionnaries)
    M = np.empty((number, number), dtype=object)


    if NAME == 'CRBL_CONFIG_20PARALLEL_wN_PLOS23':
        # MLI AND PC: ALL PARAMS N-NORMALIZED, K PARALLEL TO OTHER POP * 0.2
        ######################### HO MESSO Q * K!!!!!
        ######################## THIS CONFIG = SAME RATIONALE OF PLOS 2023
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 35., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530, 'Q': 0.437, 'Tsyn': 1.25, 'Erev': 0.} #Q normlaized per parallel and ascending -- 0.87 is standard value
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 272., 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.} #grc_to_mli NO norm (pf_Stell*0.2 + pf_bask*0.2)
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.} #mli_to_mli norm for bask and stell -- normalizzo se il presyn è diverso (in grc ho SOLO pfs)
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.275, 'Tsyn': 3.50, 'Erev': 0.} #Q normalized per parallel and ascending -- 0.55 is standard value
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        
               # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'


    elif NAME == 'CRBL_CONFIG_20PARALLEL_wN_PLOS23_Kgocgrc_red':
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50*0.5, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 35., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530*0.25, 'Q': 0.437, 'Tsyn': 1.25, 'Erev': 0.} #Q normlaized per parallel and ascending -- 0.87 is standard value
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 272., 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.} #grc_to_mli NO norm (pf_Stell*0.2 + pf_bask*0.2)
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.} #mli_to_mli norm for bask and stell -- normalizzo se il presyn è diverso (in grc ho SOLO pfs)
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.275, 'Tsyn': 3.50, 'Erev': 0.} #Q normalized per parallel and ascending -- 0.55 is standard value
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 0.60, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        
        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'


    elif NAME == 'CRBL_CONFIG_20PARALLEL_wN_PLOS23_Qgrcpc_untouch':
        # MLI AND PC: ALL PARAMS N-NORMALIZED, K PARALLEL TO OTHER POP * 0.2
        ######################### HO MESSO Q * K!!!!!
        ######################## THIS CONFIG = SAME RATIONALE OF PLOS 2023
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 35., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530, 'Q': 0.437, 'Tsyn': 1.25, 'Erev': 0.} #Q normlaized per parallel and ascending -- 0.87 is standard value
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 272., 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.} #grc_to_mli NO norm (pf_Stell*0.2 + pf_bask*0.2)
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.} #mli_to_mli norm for bask and stell -- normalizzo se il presyn è diverso (in grc ho SOLO pfs)
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.55, 'Tsyn': 3.50, 'Erev': 0.} #Q untouch =  0.55 is standard value
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}


        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'


    elif NAME == 'CRBL_CONFIG_20PARALLEL_wN_PLOS23_redKmfGoC':
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 15., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.} #PLOS Kmfgoc = 35 - QUI FURTHER REDUCTION: 15
        grc_goc = {'K': 530, 'Q': 0.437, 'Tsyn': 1.25, 'Erev': 0.} #Q normlaized per parallel and ascending -- 0.87 is standard value
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 272., 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.} #grc_to_mli NO norm (pf_Stell*0.2 + pf_bask*0.2)
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.} #mli_to_mli norm for bask and stell -- normalizzo se il presyn è diverso (in grc ho SOLO pfs)
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.275, 'Tsyn': 3.50, 'Erev': 0.} #Q normalized per parallel and ascending -- 0.55 is standard value
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}

        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'


    elif NAME == 'CRBL_CONFIG_20PARALLEL_wN_MLI_NO_NORM':
        #K PARALLEL TO OTHER POP * 0.2
        # Q is weighted for N presyn (N = bask and stell for _from_MLI ; N = granules for _from_aa and _from_pf)!!!!!
        ######################## THIS CONFIG = SAME RATIONALE OF PLOS 2023
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 35., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530, 'Q': 0.437, 'Tsyn': 1.25, 'Erev': 0.} #Q normlaized per parallel and ascending -- 0.87 is standard value
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 272., 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.} #grc_to_mli NO NORM
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 33, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.} #mli_to_mli NO NORM
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.275, 'Tsyn': 3.50, 'Erev': 0.} #Q normalized per parallel and ascending -- 0.55 is standard value
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}

        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'

    elif NAME == 'CRBL_CONFIG_20PARALLEL_wN_MLI_NORM':
        # K PARALLEL TO OTHER POP * 0.2
        ######################## THIS CONFIG = SAME RATIONALE OF PLOS 2023
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 35., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530, 'Q': 0.437, 'Tsyn': 1.25, 'Erev': 0.} #Q normlaized per parallel and ascending -- 0.87 is standard value
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 125.24, 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.} #grc_to_mli norm for bask and stell
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.} #mli_to_mli norm for bask and stell
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.275, 'Tsyn': 3.50, 'Erev': 0.} #Q normalized per parallel and ascending -- 0.55 is standard value
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}

        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'

    elif NAME == 'CRBL_CONFIG_20PARALLEL_no_aapf_norm':
        # MLI AND PC: ALL PARAMS N-NORMALIZED, K PARALLEL TO OTHER POP * 0.2
        # AS PLOS2023 BUT Q is NOT NORMALIZED PER AA AND PF
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 35., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530, 'Q': 0.87, 'Tsyn': 1.25, 'Erev': 0.}
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 272., 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.}
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.55, 'Tsyn': 3.50, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}

        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'

    elif NAME == 'CRBL_CONFIG_20PARALLEL_untouch':
        # COSì COME SONO SENZA ULTERIORI ELABORAZIONI
        # to mf -------------------------------------------------------
        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc -------------------------------------------------------
        mf_grc = {'K': 4., 'Q': 0.23, 'Tsyn': 1.90, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 3.50, 'Q': 0.36, 'Tsyn': 4.50, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc Kgrc = Kp*factor + Ka ; Qgrc = (Qa*n_syn_a*Ka+Qp*n_syn_p*Kp*factor)/(Ka+Kp*factor)-------------------------------------------------------
        #mf_goc = {'K': 57.1, 'Q': 0.24, 'Tsyn': 5., 'Erev': 0.}
        mf_goc = {'K': 110., 'Q': 0.24, 'Tsyn': 5.00, 'Erev': 0.}
        grc_goc = {'K': 530, 'Q': 0.87, 'Tsyn': 1.25, 'Erev': 0.}
        goc_goc = {'K': 20.00, 'Q': 1.12, 'Tsyn': 5.00, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 125.24, 'Q': 0.15, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 15.66, 'Q': 0.531, 'Tsyn': 2.00, 'Erev': -80.}
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 392.00, 'Q': 0.55, 'Tsyn': 3.50, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 7.12, 'Q': 1.36, 'Tsyn': 4.67, 'Erev': -80.}
        pc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}

        # Riempio per colonna - leggo per colonna
        M[:, 0] = [mf_grc.copy(), grc_grc.copy(), goc_grc.copy(), mli_grc.copy(), pc_grc.copy()]  # post-synaptic: grc
        M[:, 1] = [mf_goc.copy(), grc_goc.copy(), goc_goc.copy(), mli_goc.copy(), pc_goc.copy()]  # post-synaptic: goc
        M[:, 2] = [mf_mli.copy(), grc_mli.copy(), goc_mli.copy(), mli_mli.copy(), pc_mli.copy()]  # post-synaptic: mli
        M[:, 3] = [mf_pc.copy(), grc_pc.copy(), goc_pc.copy(), mli_pc.copy(), pc_pc.copy()]  # post-synaptic: pc
        M[:, 4] = [mf_mf.copy(), grc_mf.copy(), goc_mf.copy(), mli_mf.copy(), pc_mf.copy()]  # post-synaptic: mf

        M[0, 0]['name'] = 'to_grc'
        M[0, 1]['name'] = 'to_goc'
        M[0, 2]['name'] = 'to_mli'
        M[0, 3]['name'] = 'to_pc'
        M[0, 4]['name'] = 'to_mf'


    else:
        print('====================================================')
        print('------------ NETWORK NOT RECOGNIZED !! ---------------')
        print('====================================================')

    if SI_units:
        # quando passo M a load_config.py setto SI_units=True, quindi gli passo i V
        print('synaptic network_scaffold parameters in SI units [V, F, s]')
        for m in M.flatten():
            # NANO SIEMENS ----> SIEMENS
            if 'Q' in m:
                m['Q'] *= 1e-9
            if 'Qp' in m:
                m['Qp'] *= 1e-9
            if 'Qa' in m:
                m['Qa'] *= 1e-9
            # MILLI SEC and MILLI VOLT ----> SEC and VOLT
            m['Erev'] *= 1e-3
            m['Tsyn'] *= 1e-3

    else:
        print('synaptic network_scaffold parameters --NOT-- in SI units [mV, pF, ms]')

    return M

if __name__=='__main__':

    M = get_connectivity_and_synapses_matrix('CRBL_CONFIG', 5, SI_units=True)
    print(__doc__)

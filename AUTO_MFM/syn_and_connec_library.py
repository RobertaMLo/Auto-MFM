"""
Configurations of the network_scaffold
"""
from __future__ import print_function
import numpy as np


def get_connectivity_and_synapses_matrix(NAME, SI_units=True, number=5):


    # creating empty arry of objects (future dictionnaries)
    M = np.empty((number, number), dtype=object)

    if NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5':
        print('************* STANDARD TF CONFIGURATION ************')

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.23, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_1':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.253, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_2':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.276, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_3':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.299, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_4':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.322, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.345, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_5_bis':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.368, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_6':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.391, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_7':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.414, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_8':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.437, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    
    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_9':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.460, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}

        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m1':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.207, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m2':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.184, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m3':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.161, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m4':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.138, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    
    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m5':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.115, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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
        

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m6':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.092, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m7':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.069, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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


    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m8':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.046, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    
    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m9':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.023, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_m10':

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.0, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 579.32, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 4.07, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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

    elif NAME == 'CRBL_CONFIG_AUTOMFM_AWAKE_FIT_5_ATAXIC':
        #reduction of KpfPC impacting on KgrcPC
        #reduction of KscPC impacting on KmlipC

        mf_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_mf = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to grc ---------------------------------------------------------------------
        ## kmfgrc *PLv
        mf_grc = {'K': 2.024, 'Q': 0.0, 'Tsyn': 5.8, 'Erev': 0.}
        grc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        goc_grc = {'K': 1.77, 'Q': 0.36, 'Tsyn': 13.61, 'Erev': -80.}
        mli_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_grc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to goc -----------------------------------------------------------------------
        ## kgrcgoc summed per consistency con PC
        mf_goc = {'K': 38.5, 'Q': 0.24, 'Tsyn': 0.23, 'Erev': 0.}
        grc_goc = {'K': 590.03, 'Q': 0.44, 'Tsyn': 0.875, 'Erev': 0.}
        goc_goc = {'K': 28, 'Q': 1.12, 'Tsyn': 10, 'Erev': -80.}
        mli_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        pc_goc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to mli -----------------------------------------------------------------------
        ## k mli mli * PLV
        mf_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_mli = {'K': 260.24, 'Q': 0.07, 'Tsyn': 0.64, 'Erev': 0.}
        goc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_mli = {'K': 6.71, 'Q': 0.547, 'Tsyn': 2.00, 'Erev': -80.}  # 6.71 se pesato per plv - 16. se nn pesato
        pc_mli = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        # to pc -------------------------------------------------------------------------
        ## kgrc pc summed altrimenti bassissima
        mf_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        grc_pc = {'K': 439.7, 'Q': 0.275, 'Tsyn': 1.10, 'Erev': 0.}
        goc_pc = {'K': 0., 'Q': 0., 'Tsyn': 0., 'Erev': 0.}
        mli_pc = {'K': 3.75, 'Q': 1.22, 'Tsyn': 2.80, 'Erev': -80.}
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
        #print('synaptic network_scaffold parameters in SI units [V, F, s]')
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

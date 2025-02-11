import numpy as np
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from cell_library import get_neuron_params
from syn_and_connec_library import get_connectivity_and_synapses_matrix
from params_reformat import reformat_syn_parameters_eglif, pseq_eglif
from theoretical_tools import pseq_params, TF_my_template,\
    pseq_params_eglif_goc,TF_my_template_goc


def load_transfer_functions(CELL, NTWK, P_FILE, alpha):
    """
    returns the transfer function of the mean field model
    """

    # NTWK
    M = get_connectivity_and_synapses_matrix(NTWK, 5)

    # CELL
    params = get_neuron_params(CELL, SI_units=True)
    reformat_syn_parameters_eglif(CELL, params, M)
    print('..................... Loading TFs\nNeuron and Network: ', CELL, NTWK)
    try:
        P = np.load(P_FILE, allow_pickle=True)
        print('Loaded P file: ', P_FILE)
        print('\n')
        params['P'] = P
        print(P)

        def TF(fe, fi, XX):
            return TF_my_template(fe, fi, XX, *pseq_params(params), alpha)

    except IOError:
        print('=======================================================')
        print('===========  Fit is not available  ====================')
        print('=======================================================')

    return TF


def load_transfer_functions_molt(CELL, NTWK, P_FILE, alpha, we, wi):
    """
    returns the transfer function of the mean field model
    """

    # NTWK
    M = get_connectivity_and_synapses_matrix(NTWK, 5)

    # CELL
    params = get_neuron_params(CELL, SI_units=True)
    reformat_syn_parameters_eglif(CELL, params, M)
    try:
        P = np.load(P_FILE, allow_pickle=True)
        params['P'] = P
        print(P)

        def TF(fe, fi, XX):
            return TF_my_template(fe*we, fi*wi, XX, *pseq_params(params), alpha)

    except IOError:
        print('=======================================================')
        print('===========  Fit is not available  ====================')
        print('=======================================================')

    return TF

def load_transfer_functions_goc(CELL, NTWK, P_FILE, alpha):
    """
    returns the transfer function of the mean field model
    """

    # NTWK
    M = get_connectivity_and_synapses_matrix(NTWK, 5)

    # CELL
    params = get_neuron_params(CELL, SI_units=True)
    reformat_syn_parameters_eglif(CELL, params, M)
    print('..................... Loading TFs\nNeuron and Network: ', CELL, NTWK)
    try:
        P = np.load(P_FILE, allow_pickle=True)
        print('Loaded P file: ', P_FILE)
        print('\n')
        params['P'] = P

        def TF(fe_m, fe_g, fi, XX):
            return TF_my_template_goc(fe_m, fe_g, fi, XX, *pseq_params_eglif_goc(params), alpha)

    except IOError:
        print('=======================================================')
        print('===========  Fit is not available  ====================')
        print('=======================================================')

    return TF


def load_transfer_functions_goc_molt(CELL, NTWK, P_FILE, alpha):
    """
    returns the transfer function of the mean field model
    """

    # NTWK
    M = get_connectivity_and_synapses_matrix(NTWK, 5)

    # CELL
    params = get_neuron_params(CELL, SI_units=True)
    reformat_syn_parameters_eglif(CELL, params, M)
    print('..................... Loading TFs\nNeuron and Network: ', CELL, NTWK)
    try:
        P = np.load(P_FILE, allow_pickle=True)
        print('Loaded P file: ', P_FILE)
        print('\n')
        params['P'] = P

        def TF(fe_m, Nm, fe_g, Ng, fi, Ni, XX):
            return TF_my_template_goc(fe_m*Nm, fe_g*Ng, fi*Ni, XX, *pseq_params_eglif_goc(params), alpha)

    except IOError:
        print('=======================================================')
        print('===========  Fit is not available  ====================')
        print('=======================================================')

    return TF
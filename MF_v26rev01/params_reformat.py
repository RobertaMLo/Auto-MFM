import numpy as np

def reformat_syn_parameters_eglif(CELL, params, M):
    """
    valid if CELL is specified in cell_library
    """
    # M : row = connected cells("from"), column post synaptic target ("to"_cell).
    # SO e.g.:  to_pc: row 1 = grc, row 3 = mli. col 3 = pc
    if CELL == 'PC' :
        # sinapsi to_Purkinje
        params['Qe'], params['Te'], params['Ee']= M[1, 3]['Q'], M[1,3]['Tsyn'], M[1,3]['Erev']
        params['Ke'] = M[1, 3]['K']
        params['Qi'], params['Ti'], params['Ei'] = M[3, 3]['Q'], M[3, 3]['Tsyn'], M[3, 3]['Erev']
        params['Ki'] = M[3, 3]['K']

    elif CELL == 'GrC':
        # sinapsi to_Granular
        params['Qe'], params['Te'], params['Ee'] = M[0, 0]['Q'], M[0, 0]['Tsyn'], M[0, 0]['Erev']
        params['Qi'], params['Ti'], params['Ei'] = M[2, 0]['Q'], M[2, 0]['Tsyn'], M[2, 0]['Erev']
        params['Ke'] = M[0, 0]['K']
        params['Ki'] = M[2, 0]['K']

    elif CELL=='GoC':
        # sinapsi to_Golgi
        params['Qe_m'], params['Te_m'] = M[0, 1]['Q'], M[0, 1]['Tsyn']
        params['Qe_g'], params['Te_g'] = M[1, 1]['Q'], M[1, 1]['Tsyn']
        params['Ee'] = M[0, 1]['Erev']  # tanto sia granuli sia mossy sono eccitatorie
        params['Qi'], params['Ti'], params['Ei'] = M[2, 1]['Q'], M[2, 1]['Tsyn'], M[2, 1]['Erev']
        params['Ke_m'] = M[0, 1]['K']
        params['Ke_g'] = M[1, 1]['K']
        params['Ki'] = M[2, 1]['K']

    elif CELL == 'MLI':
        # sinapsi to_Molecular layer
        params['Qe'], params['Te'], params['Ee'] = M[1, 2]['Q'], M[1, 2]['Tsyn'], M[1, 2]['Erev']
        params['Qi'], params['Ti'], params['Ei'] = M[3, 2]['Q'], M[3, 2]['Tsyn'], M[3, 2]['Erev']
        params['Ke'] = M[1, 2]['K']
        params['Ki'] = M[3, 2]['K']


def pseq_eglif(cell_params):
    """ I'm the function to extract all parameters for the sim
    (can't pass a dict() in Numba )"""

    # those parameters have to be set
    El, Gl = cell_params['El'], cell_params['Gl']
    Ee, Ei = cell_params['Ee'], cell_params['Ei']

    Cm = cell_params['Cm']
    kadap, k2, k1 = cell_params['kadap'], cell_params['k2'], cell_params['k1']
    A1, A2, Ie = cell_params['A1'], cell_params['A2'], cell_params['Ie']
    tm = cell_params['tm']

    trefrac, delta_v = cell_params['Trefrac'], cell_params['delta_v']

    vthresh, vreset = cell_params['Vthre'], cell_params['Vreset']

    # then those can be optional
    if 'vspike' not in cell_params.keys():
        vspike = vthresh + 5 * delta_v  # as in the Brian simulator !
    else:
        vspike = cell_params['vspike']

    return El, Gl, Cm, Ee, Ei, vthresh, vreset, vspike, \
           trefrac, delta_v, kadap, k2, k1, A2, A1, Ie, tm
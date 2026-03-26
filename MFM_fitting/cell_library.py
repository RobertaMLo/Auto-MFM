"""
Library of single-neurons configurations
"""
from __future__ import print_function

def get_neuron_params(NAME,  SI_units=True, name='', number=1):

    if NAME == 'GrC':
        params = {'name': name, 'N': number,
                  'Gl': 0.2899, 'Cm': 7., 'Trefrac': 1.5, 'tm': 24.15,
                  'El': -62., 'Vthre': -41., 'Vreset': -70., 'delta_v': 0.3,
                  'kadap': 0.022, 'k2': 0.041, 'k1': 0.311, 'A2': -0.94, 'A1': 0.01, 'Ie': -0.888}

    elif NAME == 'GoC':
        params = {'name': name, 'N': number,
                  'Gl': 3.2955, 'Cm': 145., 'Trefrac': 2., 'tm': 44.,
                  'El': -62., 'Vthre': -55., 'Vreset': -75., 'delta_v': 0.4,
                  'kadap': 0.217, 'k2': 0.023, 'k1': 0.031, 'A2': 178.01, 'A1': 259.988, 'Ie': 16.214}

    elif NAME == 'MLI':
        params = {'name': name, 'N': number,
                  'Gl': 1.6, 'Cm': 14.6, 'Trefrac': 1.59, 'tm': 9.125,
                  'El': -68., 'Vthre': -53., 'Vreset': -78., 'delta_v': 1.1,
                  'kadap': 2.025, 'k2': 1.096, 'k1': 1.887, 'A2': 5.863, 'A1': 5.953, 'Ie': 3.711} #mf PLOS version:3.711*1.2

    elif NAME == 'PC':
        params = {'name': name, 'N': number,
                  'Gl': 7.1064, 'Cm': 334., 'Trefrac': 0.5, 'tm': 47.,
                  'El': -59., 'Vthre': -43., 'Vreset': -69., 'delta_v': 3.5,
                  'kadap': 1.491, 'k2': 0.041, 'k1': 0.195, 'A2': 172.622, 'A1': 157.622, 'Ie': 780} #700 std #mf PLOS version:742.54*1.2

    elif NAME == 'GrC_IB2KO':
        params = {'name': name, 'N': number,
                  'Gl': 0.132, 'Cm': 3.2, 'Trefrac': 1.5, 'tm': 24.15,
                  'El': -62., 'Vthre': -41., 'Vreset': -70., 'delta_v': 0.3,
                  'kadap': 0.022, 'k2': 0.041, 'k1': 0.311, 'A2': -0.94, 'A1': 0.01, 'Ie': -0.888}

    elif NAME == 'GrC_WT':
        params = {'name': name, 'N': number,
                  'Gl': 0.147, 'Cm': 3.6, 'Trefrac': 1.5, 'tm': 24.15,
                  'El': -62., 'Vthre': -41., 'Vreset': -70., 'delta_v': 0.3,
                  'kadap': 0.022, 'k2': 0.041, 'k1': 0.311, 'A2': -0.94, 'A1': 0.01, 'Ie': -0.888}

    else:
        print('====================================================')
        print('------------ CELL NOT RECOGNIZED !! ---------------')
        print('====================================================')

    if SI_units:
        # print('cell parameters in SI units')
        # MILLI V to V ---------------------------------------------------------------------------------
        params['El'] = 1e-3 * params['El']
        params['Vthre'] = 1e-3 * params['Vthre']
        params['Vreset'] = 1e-3 * params['Vreset']
        params['delta_v'] = 1e-3 * params['delta_v']
        if 'vspike' in params: params['vspike'] = 1e-3 * params['vspike']

        # MILLI s to s -----------------------------------------------------------------------------
        if 'tm' in params: params['tm'] = 1e-3 * params['tm']
        params['Trefrac'] = 1e-3 * params['Trefrac']

        # KILO Hz to Hz --> (ms)^-1 to s^-1 --> (10^-3)^-1 = 10^3 ----------------------------------
        if 'k2' in params: params['k2'] = 1e3 * params['k2']
        if 'k1' in params: params['k1'] = 1e3 * params['k1']

        # (MEGA H)^-1 to H^-1 --> (10^6)^-1 = 10^-6 -------------------------------------------------
        if 'kadap' in params: params['kadap'] = 1e-6 * params['kadap']

        # NANO S to S ------------------------------------------------------------------------------
        if 'a' in params: params['a'] = 1e-9 * params['a']
        params['Gl'] = 1e-9 * params['Gl']

        # PICO A to A -------------------------------------------------------------------------------
        if 'b' in params: params['b'] = 1e-12 * params['b']
        if 'A2' in params: params['A2'] = 1e-12 * params['A2']
        if 'A1' in params: params['A1'] = 1e-12 * params['A1']
        if 'Ie' in params: params['Ie'] = 1e-12 * params['Ie']

        # PICO F to F -------------------------------------------------------------------------------
        params['Cm'] = 1e-12 * params['Cm']
    else:
        print('cell parameters --NOT-- in SI units')

    return params.copy()


if __name__ == '__main__':
    paramsPC = get_neuron_params('PC', True, name='', number=1)
    print(__doc__)

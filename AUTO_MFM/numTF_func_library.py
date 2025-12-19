"""
Library of standard function to get all the ingredients needed to compute the TF NUMERICAL TEMPLATE:
1) frequency span
2) firing rate (i.e. fout = numTF) of a single experiment (=one fe-fi couple)
3) loop to compute 2) for each fe-fi couple
4) routine to save results

<function_name>_goc can be used for population with 3 synaptic connections (as GoC)

"""
import numpy as np
"""
from CRBL_MF_Model.Zebrine_plus.params_library.cell_library import get_neuron_params
from CRBL_MF_Model.Zebrine_plus.params_library.syn_and_connec_library import get_connectivity_and_synapses_matrix
from CRBL_MF_Model.Zebrine_plus.params_library.params_reformat import reformat_syn_parameters_eglif, pseq_eglif
from CRBL_MF_Model.Zebrine_plus.numerical_network.alpha_cond_generation import g_alpha_exc, g_alpha_inhib,\
    g_alpha_exc_grc_goc, g_alpha_exc_mossy_goc
from CRBL_MF_Model.Zebrine_plus.numerical_network.eglif_simulator import eglif_solver, eglif_solver_goc
"""
"""
from ..params_library.cell_library import get_neuron_params
from ..params_library.syn_and_connec_library import get_connectivity_and_synapses_matrix
from ..params_library.params_reformat import reformat_syn_parameters_eglif, pseq_eglif
from numerical_network.alpha_cond_generation import g_alpha_exc, g_alpha_inhib,\
    g_alpha_exc_grc_goc, g_alpha_exc_mossy_goc
from numerical_network.eglif_simulator import eglif_solver, eglif_solver_goc
"""


from cell_library import get_neuron_params
from syn_and_connec_library import get_connectivity_and_synapses_matrix
from params_reformat import reformat_syn_parameters_eglif, pseq_eglif
from alpha_cond_generation import g_alpha_exc, g_alpha_inhib,\
    g_alpha_exc_grc_goc, g_alpha_exc_mossy_goc
from eglif_simulator import eglif_solver, eglif_solver_goc



import os
import time


def set_freq_span(femin, femax, fimin, fimax, dfe, dfi):
    return np.arange(femin, femax, dfe), np.arange(fimin, fimax, dfi)

def set_freq_span_goc(fe_g_min, fe_g_max, fe_m_min, fe_m_max, fimin, fimax, dfe_g, dfe_m, dfi):
    return np.arange(fe_g_min, fe_g_max, dfe_g), np.arange(fe_m_min, fe_m_max, dfe_m),  np.arange(fimin, fimax, dfi)


def single_experiment_eglif_alpha(t, fe, fi, params, seed=0):
    """
    Run eglif_sim for a pair of (fe,fi
    ALPHA-FUNCTION CONDUCTANCE
    ADAPTATION computed as mean
    """

    ## fe and fi total synaptic activities, they include the synaptic number
    I = np.zeros(len(t))

    vm, w, w_vett, t_spikes = eglif_solver(t, I, g_alpha_exc(t, fe, params), g_alpha_inhib(t, fi, params),
                                   *pseq_eglif(params))


    froutput = ( len(t_spikes) / (3 * t.max() / 4)) #3/4 because 1/4 is transeint time (not considered)


    #w_int = np.trapz(w[int(len(t)/4):], t[int(len(t)/4):]) #Consider form first quarter

    # for the moment seed = 0, but if I want to add different seed --> del vars at each iter
    del vm
    del t_spikes

    return froutput, w


def single_experiment_eglif_alpha_goc(t, fe_g, fe_m, fi, params, seed=0):
    """
    Run eglif_sim for a pair of (fe,fi
    ALPHA-FUNCTION CONDUCTANCE
    ADAPTATION computed as mean
    """

    ## fe and fi total synaptic activities, they include the synaptic number
    I = np.zeros(len(t))

    vm, w, w_vett, t_spikes = eglif_solver_goc(t, I, g_alpha_exc_grc_goc(t, fe_g, params),
                                               g_alpha_exc_mossy_goc(t, fe_m, params),
                                               g_alpha_inhib(t, fi, params), *pseq_eglif(params))


    froutput = ( len(t_spikes) / (3 * t.max() / 4)) #3/4 because 1/4 is transeint time (not considered)


    #w_int = np.trapz(w[int(len(t)/4):], t[int(len(t)/4):]) #Consider form first quarter

    # for the moment seed = 0, but if I want to add different seed --> del vars at each iter
    del vm
    del t_spikes

    return froutput, w


## =====================================
## ====== TF Numerical Template ========
## =====================================
# Here I'm computing the numerical template of the TF as a collection of single trace experiment
def generate_transfer_function_eglif_alpha(params, t, Fe_eff, fiSim, SEED, verbose=True):

        """ Generate the numerical template of the transfer function:
        - alpha conductance
        - fixed step for fe
        - adaptation as mean of w_vett
        """

        print('******************************** GENERATE TF **********************************************')
        print('*******************************************************************************************')

        MEANfreq = np.zeros((fiSim.size, Fe_eff.size))
        SDfreq = np.zeros((fiSim.size, Fe_eff.size))
        w = np.zeros((fiSim.size, Fe_eff.size))

        # wec = np.zeros(SEED) ## In future if I want to run simulation for different Seed --> different g
        # vec = np.zeros(SEED)

        for fi in range(np.shape(fiSim)[0]):
            for fe in range(np.shape(Fe_eff)[0]):

                # for seed in np.arange(1, SEED):
                #    vec[seed], wec[seed], len_spikes, t_max = single_experiment_eglif_alpha(t,
                #                                        Fe_eff[fe]*params['Ke'], fiSim[fi]*params['Ki'],
                #                                        params, seed=seed)

                vec, wec = single_experiment_eglif_alpha(t, Fe_eff[fe], fiSim[fi], params)

                if verbose:
                    # print('Seed : ', seed)
                    print(" exc :", fe, " over ", Fe_eff.size, ' Fe= ', Fe_eff[fe])
                    print(" inh :", fi, " over ", fiSim.size, ' Fi= ', fiSim[fi])
                    print('Fout: ', vec)

                MEANfreq[fi, fe] = vec.mean()  ## Write in column - fixed fi for varying fe
                SDfreq[fi, fe] = vec.std()
                w[fi, fe] = wec.mean()

                del vec
                del wec

        print('******************************** END GENERATE TF ******************************************')
        print('*******************************************************************************************')

        return MEANfreq, SDfreq, w


def generate_transfer_function_eglif_alpha_goc(params, t, Fe_eff_grc, Fe_eff_mossy, fiSim, SEED, verbose=True):
    """ Generate the numerical template of the transfer function:
    - alpha conductance
    - fixed step for fe
    - adaptation as mean of w_vett
    """

    print('******************************** GENERATE TF **********************************************')
    print('*******************************************************************************************')

    MEANfreq = np.zeros((fiSim.size, Fe_eff_grc.size, Fe_eff_mossy.size))
    SDfreq = np.zeros((fiSim.size, Fe_eff_grc.size, Fe_eff_mossy.size))
    w = np.zeros((fiSim.size, Fe_eff_grc.size, Fe_eff_mossy.size))

    # wec = np.zeros(SEED) ## In future if I want to run simulation for different Seed --> different g
    # vec = np.zeros(SEED)

    for fi in range(np.shape(fiSim)[0]):
        for fe_g in range(np.shape(Fe_eff_grc)[0]):
            for fe_m in range(np.shape(Fe_eff_mossy)[0]):

                # for seed in np.arange(1, SEED):
                #    vec[seed], wec[seed], len_spikes, t_max = single_experiment_eglif_alpha(t,
                #                                        Fe_eff[fe]*params['Ke'], fiSim[fi]*params['Ki'],
                #                                        params, seed=seed)

                vec, wec = single_experiment_eglif_alpha_goc(t, Fe_eff_grc[fe_g], Fe_eff_mossy[fe_m],
                                                             fiSim[fi], params)

                if verbose:
                    # print('Seed : ', seed)
                    print(" exc: mossy to goc:", fe_m, " over ", Fe_eff_mossy.size, ' Fe= ', Fe_eff_mossy[fe_m])
                    print(" exc: grc to goc: ", fe_g,  " over ", Fe_eff_grc.size, ' Fe= ', Fe_eff_grc[fe_g])
                    print(" inh :", fi, " over ", fiSim.size, ' Fi= ', fiSim[fi])
                    print('Fout: ', vec)

                MEANfreq[fi, fe_g, fe_m] = vec.mean()  ## Write in column - fixed fi for varying fe
                SDfreq[fi, fe_g, fe_m] = vec.std()
                w[fi, fe_g, fe_m] = wec.mean()

                del vec
                del wec

    print('******************************** END GENERATE TF ******************************************')
    print('*******************************************************************************************')

    return MEANfreq, SDfreq, w


def save_complete_sim(neuron_model, conn_model, Fout_mean, Fout_sd, Adap, fe, fi, tsim, dt):


    params = get_neuron_params(neuron_model)
    M = get_connectivity_and_synapses_matrix(conn_model)
    reformat_syn_parameters_eglif(neuron_model, params, M)

    sim_params = {'cell':neuron_model, 'conn':conn_model, 'tsim': tsim, 'dt': dt}

    date_time = time.strftime("%Y%m%d_%H%M%S")

    FOLDER = date_time + '_' + neuron_model +'_'+ conn_model +'_fe' + str(int(fe[0])) + '_' + str(int(fe[-1])) + '_fi' + str(int(fi[0])) + '_' + \
            str(int(fi[-1])) + '_tsim' + str(int(tsim.max()))

    path = os.getcwd()
    if os.path.exists(path + FOLDER):
        print('Folder %s for num TF has been already created!' % FOLDER)
    else:
        try:
            os.mkdir(FOLDER)
        except OSError:
            print("Creation of the directory %s failed" % FOLDER)
        else:
            print("Successfully created the directory %s " % FOLDER)

        np.save(FOLDER + '/numTF.npy', Fout_mean)
        np.save(FOLDER + '/FoutSD.npy', Fout_sd)
        np.save(FOLDER + '/adaptation.npy', Adap)
        np.save(FOLDER + '/fe_vector.npy', fe)
        np.save(FOLDER + '/fi_vector.npy', fi)
        np.save(FOLDER + '/sim_len.npy', sim_params)
        np.save(FOLDER + '/params.npy', params)


def save_complete_sim_goc(neuron_model, conn_model, Fout_mean, Fout_sd, Adap, fe_g, fe_m, fi, tsim, dt):
    params = get_neuron_params(neuron_model)
    M = get_connectivity_and_synapses_matrix(conn_model)
    reformat_syn_parameters_eglif(neuron_model, params, M)

    sim_params = {'cell':neuron_model, 'conn':conn_model, 'tsim': tsim, 'dt': dt}

    date_time = time.strftime("%Y%m%d_%H%M%S")

    FOLDER = date_time + '_' + neuron_model +'_'+ conn_model +'_fe_g' + str(int(fe_g[0])) + '_' + str(int(fe_g[-1])) + \
             '_fe_m' + str(int(fe_m[0])) + '_' + str(int(fe_m[-1])) +\
             '_fi' + str(int(fi[0])) + '_' + str(int(fi[-1])) + '_tsim' + str(int(tsim.max()))

    path = os.getcwd()
    if os.path.exists(path + FOLDER):
        print('Folder %s for num TF has been already created!' % FOLDER)
    else:
        try:
            os.mkdir(FOLDER)
        except OSError:
            print("Creation of the directory %s failed" % FOLDER)
        else:
            print("Successfully created the directory %s " % FOLDER)

        np.save(FOLDER + '/numTF.npy', Fout_mean)
        np.save(FOLDER + '/FoutSD.npy', Fout_sd)
        np.save(FOLDER + '/adaptation.npy', Adap)
        np.save(FOLDER + '/fe_g_vector.npy', fe_g)
        np.save(FOLDER + '/fe_m_vector.npy', fe_m)
        np.save(FOLDER + '/fi_vector.npy', fi)
        np.save(FOLDER + '/sim_len.npy', sim_params)
        np.save(FOLDER + '/params.npy', params)

"""
I'm a super code.
I'm the best MF never written 'cause I don't work alone, I work with my bff BSB and nest.
Togehter we are more physiological reliable :D
"""

import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from numTF_func_library import *


def generate_transfer_function_eglif_alpha_2pop_BSB(params, t, Fe_eff, fiSim, SEED, verbose=True):
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

    for fi in range(len(fiSim)):
        for fe in range(len(Fe_eff)):

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


def generate_transfer_function_eglif_alpha_goc_BSB(params, t, Fe_eff_grc, Fe_eff_mossy, fiSim, SEED, verbose=True):
    """ Generate the numerical template of the transfer function:
    - alpha conductance
    - fixed step for fe
    - adaptation as mean of w_vett
    """

    print('******************************** GENERATE TF **********************************************')
    print('*******************************************************************************************')

    MEANfreq = np.zeros((fiSim.size, Fe_eff_grc.size))
    SDfreq = np.zeros((fiSim.size, Fe_eff_grc.size))
    w = np.zeros((fiSim.size, Fe_eff_grc.size))

    # wec = np.zeros(SEED) ## In future if I want to run simulation for different Seed --> different g
    # vec = np.zeros(SEED)

    for fi in range(len(fiSim)):
        for fe_g in range(len(Fe_eff_grc)):

                # for seed in np.arange(1, SEED):
                #    vec[seed], wec[seed], len_spikes, t_max = single_experiment_eglif_alpha(t,
                #                                        Fe_eff[fe]* params['Ke'], fiSim[fi]*params['Ki'],
                #                                        params, seed=seed)

                vec, wec = single_experiment_eglif_alpha_goc(t, Fe_eff_grc[fe_g], Fe_eff_mossy,
                                                             fiSim[fi], params)

                if verbose:
                    # print('Seed : ', seed)
                    print("Mossy input: ",Fe_eff_mossy)
                    print(" exc: grc to goc: ", fe_g,  " over ", Fe_eff_grc.size, ' Fe= ', Fe_eff_grc[fe_g])
                    print(" inh :", fi, " over ", fiSim.size, ' Fi= ', fiSim[fi])
                    print('Fout: ', vec)

                MEANfreq[fi, fe_g] = vec.mean()  ## Write in column - fixed fi for varying fe
                SDfreq[fi, fe_g] = vec.std()
                w[fi, fe_g] = wec.mean()

                del vec
                del wec

    print('******************************** END GENERATE TF ******************************************')
    print('*******************************************************************************************')

    return MEANfreq, SDfreq, w


def save_complete_sim(neuron_model, conn_model, Fout_mean, Fout_sd, Adap, fe, fi, delta_e, delta_i, tsim, dt):
    params = get_neuron_params(neuron_model)
    M = get_connectivity_and_synapses_matrix(conn_model)
    reformat_syn_parameters_eglif(neuron_model, params, M)

    sim_params = {'cell':neuron_model, 'conn':conn_model, 'tsim': tsim, 'dt': dt}

    date_time = time.strftime("%Y%m%d_%H%M%S")

    FOLDER = date_time + '_' + neuron_model +'_'+ conn_model +'_tsim' + str(int(tsim.max()))

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
        np.save(FOLDER + '/fe.npy', fe)
        np.save(FOLDER + '/fi.npy', fi)
        np.save(FOLDER + '/delta_e.npy', delta_e)
        np.save(FOLDER + '/delta_i.npy', delta_i)
        np.save(FOLDER + '/sim_len.npy', sim_params)
        np.save(FOLDER + '/params.npy', params)


def read_csv_file(file_path):
    import csv
    file = open(file_path)
    csvreader = csv.reader(file)
    rows = []

    for row in csvreader:
        rows.append(row)

    file.close()

    rows=np.array(rows)
    mossy_input = rows[:,0]
    f_mean = rows[:,1]
    #f_sd = rows[:,2]

    #mossy_input[i] = type string --> need to map into an array of type float
    mossy_input = list(map(float, mossy_input))
    f_mean = list(map(float, f_mean))
    #f_sd = list(map(float, f_sd))

    return np.array(mossy_input), np.array(f_mean) #,np.array(f_sd)



def routine_POP2conn(fe_mean, fi_mean):

    MeanFreq, SDFreq, w_score = generate_transfer_function_eglif_alpha_2pop_BSB(params, t, fe_mean, fi_mean, args.SEED)

    delta_e_vett = np.zeros(len(f_m_allspan))
    delta_i_vett = np.zeros(len(fi_mean))

    save_complete_sim(args.Neuron_Model, args.Network_Model, MeanFreq, SDFreq, w_score, fe_mean,
                      fi_mean, delta_e_vett, delta_i_vett, t, args.dt)

    #plt.imshow(MeanFreq)
    #plt.show()

    return MeanFreq, SDFreq, w_score


def routine_POP3conn(f_m_allspan, fe_g_mean, fi_mean):

    n_bin_grc = 20  # reduce range: no need to have a large span around the mean
    n_bin_goc = 40

    # 2D matrix: save vals of freq range for each mossy input
    fe_grc_vett_tot, fi_vett_tot = np.zeros([n_bin_grc, len(f_m_allspan)]), \
                                   np.zeros([n_bin_goc, len(f_m_allspan)])

    delta_grc_vett, delta_i_vett = np.zeros([len(f_m_allspan)]), \
                                   np.zeros([len(f_m_allspan)])

    MeanFreq, SDFreq, w_score = np.zeros([n_bin_goc, n_bin_grc, len(f_m_allspan)]), \
                                np.zeros([n_bin_goc, n_bin_grc, len(f_m_allspan)]), \
                                np.zeros([n_bin_goc, n_bin_grc, len(f_m_allspan)])

    # test code : step = max - min/ n_bin
    # step = ((fe_g_mean[2]+1)  -  (fe_g_mean[2]-1)) / n_bin_grc
    # vec_freq = np.arange( (fe_g_mean[2]-1), (fe_g_mean[2]+1) , step)

    for i in range(len(f_m_allspan)):
        # delta_lf_grc  = stdev #from 0 to 8 HZ --> first three steps
        # delta_0_goc = stdev

        # delta_g = 2
        # delta_i = 12

        # if f_m_allspan[i] <= 8:
        #    delta_g = fe_g_sd[i]

        # if f_m_allspan[i] == 0:
        #    delta_i = fi_sd[i]

        #1e-6 to avoid error IF delta_g = 0 - fmean = 0
        delta_g = (20 * fe_g_mean[i] / 100)+1e-6
        delta_i = (20 * fi_mean[i] / 100)+1e-6

        step_g = ((fe_g_mean[i] + delta_g) - (fe_g_mean[i] - delta_g)) / n_bin_grc
        step_i = ((fi_mean[i] + delta_i) - (fi_mean[i] - delta_i)) / n_bin_goc

        print('delta gran', delta_g)
        print('delta goc', delta_i)

        fe_grc_vett = np.arange(fe_g_mean[i] - delta_g, fe_g_mean[i] + delta_g, step_g)
        fi_vett = np.arange(fi_mean[i] - delta_i, fi_mean[i] + delta_i, step_i)

        fe_grc_vett_tot[:, i], fi_vett_tot[:, i] = fe_grc_vett, fi_vett

        MeanFreq[:, :, i], SDFreq[:, :, i], w_score[:, :, i] = generate_transfer_function_eglif_alpha_goc_BSB(params, t,
                                                                                    fe_grc_vett, f_m_allspan[i], fi_vett,
                                                                                                              args.SEED)

    save_complete_sim(args.Neuron_Model, args.Network_Model, MeanFreq, SDFreq, w_score, fe_grc_vett_tot,
                          fi_vett_tot, delta_g, delta_i, t, args.dt)


    return MeanFreq, SDFreq, w_score



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import argparse
    import numpy as np

    parser = argparse.ArgumentParser(description=
                                     """ 
                                   'Main routine for numerical template generation'
                                   """,
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("root_dir",
                        help="Root path of the project")
    parser.add_argument("Neuron_Model", help="Choose a neuronal model from 'cell_library.py'")
    parser.add_argument("Network_Model", help="Choose a network_scaffold model (synaptic and connectivity properties)"
                                              "\nfrom 'syn_and_conn_library'.py")

    parser.add_argument('-SEED', type=int, default=0, help="seed number")

    parser.add_argument('-t_stop', type=float, default=5., help="length of the simulation [s]")
    parser.add_argument('-dt', type=float, default=1e-4, help=" time step [s]")

    args = parser.parse_args()

    params = get_neuron_params(args.Neuron_Model)
    M = get_connectivity_and_synapses_matrix(args.Network_Model)
    reformat_syn_parameters_eglif(args.Neuron_Model, params, M)

    t = np.arange(0, args.t_stop+args.dt, args.dt)
    print(params)


    #load frequencies span defined with bsb_preprocessing
    root_dir = args.root_dir #'/Users/robertalorenzi/PycharmProjects/bsb_ws/CRBL_MF_Model/'

    if args.Neuron_Model == 'PC' or args.Neuron_Model == 'MLI':
        """
        #BSB3 old pipeline
        csv_stats = [root_dir + 'bsb_preprocessing/GRC_STATS/grc_fr_stats.csv',
                 root_dir + 'bsb_preprocessing/MLI_STATS/mli_fr_stats.csv']
        """
       
        # BSB4
        csv_stats = [root_dir + 'granule_cell_fr_for_TF.csv',
                 root_dir + 'MLI_cell_fr_for_TF.csv']
    

        
        f_m_allspan, fe_mean = read_csv_file(csv_stats[0])
        _, fi_mean = read_csv_file(csv_stats[1])

        print(np.max(fe_mean))
        print(np.max(fi_mean))

        MeanFreq, SDFreq, w_score = routine_POP2conn(fe_mean=fe_mean, fi_mean=fi_mean)


    elif 'GrC' in args.Neuron_Model or args.Neuron_Model == 'GoC':
        """
        #BSB3 old pipeline
        csv_stats = [root_dir +'bsb_preprocessing/GRC_STATS/grc_fr_stats.csv',
                 root_dir + 'bsb_preprocessing/GOC_STATS/golgi_fr_stats.csv']
        """

        # BSB4
        csv_stats = [root_dir + 'granule_cell_fr_for_TF.csv',
                 root_dir + 'golgi_cell_fr_for_TF.csv']

        f_m_allspan, fe_mean = read_csv_file(csv_stats[0])
        _, fi_mean = read_csv_file(csv_stats[1])

        print(np.max(fe_mean))
        print(np.max(fi_mean))

        if 'GrC' in args.Neuron_Model : MeanFreq, SDFreq, w_score = routine_POP2conn(fe_mean=f_m_allspan, fi_mean=fi_mean)

        if args.Neuron_Model == 'GoC': MeanFreq, SDFreq, w_score = routine_POP3conn(f_m_allspan=f_m_allspan,
                                                                                    fe_g_mean=fe_mean, fi_mean=fi_mean)


    else: print("Neuron Model not defined")


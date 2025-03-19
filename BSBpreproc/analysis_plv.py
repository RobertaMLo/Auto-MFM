from bsb import from_storage
import numpy as np
from quantities import ms
from cerebellum.analysis.spiking_results import SpikeSimulationReport
import matplotlib.pyplot as plt
from elephant.phase_analysis import phase_locking_value
from elephant.statistics import fanofactor
from  elephant.conversion import BinnedSpikeTrain
from elephant.spike_train_correlation import covariance
from elephant.statistics import instantaneous_rate
from elephant.kernels import GaussianKernel
from elephant.signal_processing import hilbert
from elephant.spike_train_correlation import cross_correlation_histogram
import time
import argparse
import os 

if __name__ == '__main__':

  
    parser = argparse.ArgumentParser(description=
                                    """ 
                                    'Pipeline to compute the synchrony, return the plv'
                                    """,
                                    formatter_class=argparse.RawTextHelpFormatter)

    
    parser.add_argument("-conn", type= str,
                        help="choose conbnectivity strategy")
    
    parser.add_argument("-prot_dir", default='/home/bcc/projects/BSB4_demo/cerebellum_0.5.0/cerebellum',
                        help="folder of cerebellum")
    
    parser.add_argument("-folder_nio", default = '/new_nios/nio_files_40',
                        help="choose conbnectivity strategy")


    args = parser.parse_args()


    prot_dir = args.prot_dir
    simulation_name = 'basal_activity'
    folder_nio = prot_dir + args.folder_nio
    scaffold=from_storage(prot_dir+ '/mouse_cerebellum.hdf5')
    conn_set = scaffold.get_connectivity_set(args.conn)
    pre_cell = args.conn.split('_to_')[0]
    if pre_cell == 'parallel_fiber' or pre_cell == 'ascending_axon':
        pre_cell = 'granule_cell'
    post_cell = args.conn.split('_to_')[1]

    conns = conn_set.load_connections().all()
    ids_pre_post = [conn[:, 0] for conn in conns]

    pre = ids_pre_post[0]
    post = ids_pre_post[1]
    pre_per_post = {}
    convs = []

    dt = 0.1
    for i in np.unique(post):
        j = np.where(post == i)
        pre_per_post[i] = pre[j]
        convs.append(len(pre[j]))

    mean_conv = np.mean(convs)
    print(f'Check mean convergence: {mean_conv}')
    report = SpikeSimulationReport(scaffold, simulation_name=simulation_name, folder_nio=folder_nio)
    pre_spikes = report.all_spikes[np.where(np.array(report.populations) == pre_cell)[0][0]]
    senders = np.array(pre_spikes.array_annotations['senders'])
    senders = senders - min(senders)


    spike_trains = []
    frs = []
    phases = []
    for j in range(len(post)): 
        for i, pre in enumerate(pre_per_post[j]):
            ids = np.where(senders == pre)[0]
            spikes_pre = pre_spikes[ids]
            spike_trains.append(spikes_pre)
            firing_rate = instantaneous_rate(spikes_pre, sampling_period=0.1*ms, border_correction=True, kernel='auto') #GaussianKernel(sigma=20 * ms))
            frs.append(firing_rate)
            phase = hilbert(firing_rate)
            phases.append(np.angle(phase))
            # plt.scatter(spikes_grc, np.ones(len(spikes_grc))*i, marker='|', color='red', s = 1)

    # print(f'Phases: {phases}')
    ff = fanofactor(spike_trains)
    print('Fano Factor Grc: ', ff)

    cov = covariance(BinnedSpikeTrain(spike_trains, bin_size=50*ms))
    print(np.mean(cov))

    #plt.imshow(cov, vmin=0, vmax=1)
    #plt.colorbar()
    #plt.savefig('cov.png')

    #plt.close()

    
    print('Starting PLVs computing ...')
    start = time.perf_counter()
    plm = np.zeros(shape=(len(phases), len(phases)))
    for i, p1 in enumerate(phases):
        for j, p2 in enumerate(phases):
             plm[i, j] = phase_locking_value(p1, p2)
    end = time.perf_counter()

    print(f'END! Total time: {end - start}')

    plt.imshow(plm, vmin=0, vmax=1)
    plt.colorbar()
    conn = args.conn
    plt.savefig(f'plm_{conn}.png')

    mean_pl = np.mean(plm)
    std_pl = np.std(plm)
    txt_folder = prot_dir + '/sync_stat/'
    os.makedirs(txt_folder, exist_ok=True)
    txt_name = txt_folder + f'/{conn}.txt'
    np.savetxt(txt_name, [mean_pl,std_pl,ff])
    print('Mean Phase Locking Value: ', mean_pl)

    # cross_corr = cross_correlation_histogram(BinnedSpikeTrain(spike_trains, bin_size=10*ms))
    # print('Cross Correlation Histogram: ', np.mean(cross_corr))













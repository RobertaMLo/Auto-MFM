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

## File to compute the plm TO ONE CELL!!!!
## IT MUST BE SAVED IN THE SAME FOLDER WHERE .HDF5 WAS CREATED FOR SOME HIDDEN DEPENDECIES IN HDF5 FILE.

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=
                                    """ 
                                    'Pipeline to compute the synchrony, return the plv'
                                    """,
                                    formatter_class=argparse.RawTextHelpFormatter)

    
    parser.add_argument("-conn", default = 'parallel_fiber_to_purkinje',
                        help="choose connectivity strategy")
    
    parser.add_argument("-prot_dir", default='/home/bcc/projects/BSB4_demo/cerebellum_0.5.0/cerebellum',
                        help="folder of cerebellum")
    
    parser.add_argument("-folder_nio", default = '/new_nios/nio_files_40',
                        help="simulation to compute plv")
    
    parser.add_argument("-scaffold", default = '/mouse_cerebellum.hdf5',
                        help="choose the scaffold .hdf5")


    args = parser.parse_args()


    prot_dir = args.prot_dir #'/home/bcc/projects/BSB4_demo/cerebellum_0.5.0/cerebellum'
    folder_nio = prot_dir+ args.folder_nio #'/new_nios_vitro/new_nios_vitro_40'
    scaffold=from_storage(prot_dir+ args.scaffold) #'/mouse_cerebellum.hdf5')
    conn = args.conn #'glomerulus_to_granule' #'golgi_to_glomerulus' #'ascending_axon_to_basket' #'parallel_fiber_to_stellate' #'parallel_fiber_to_stellate'
    pf_pc_conn_set = scaffold.get_connectivity_set(conn) #'parallel_fiber_to_purkinje'
    
    conns = pf_pc_conn_set.load_connections().all()
    ids_pre_post = [conn[:, 0] for conn in conns]

    pre = ids_pre_post[0]
    post = ids_pre_post[1]
    grc_per_pc = {}
    convs = []

    simulation_name = 'basal_activity'
    dt = 0.1
    for i in np.unique(post):
        j = np.where(post == i)
        grc_per_pc[i] = pre[j]
        convs.append(len(pre[j]))

    mean_conv = np.mean(convs)
    print(f'Check mean convergence: {mean_conv}')
    report = SpikeSimulationReport(scaffold, simulation_name='basal_activity', folder_nio=folder_nio)
    grc_spikes = report.all_spikes[np.where(np.array(report.populations) == "granule_cell")[0][0]]
    senders = np.array(grc_spikes.array_annotations['senders'])
    senders = senders - min(senders)


    spike_trains = []
    frs = []
    phases = []
    for i, grc in enumerate(grc_per_pc[0]):
        ids = np.where(senders == grc)[0]
        spikes_grc = grc_spikes[ids]
        spike_trains.append(spikes_grc)
        firing_rate = instantaneous_rate(spikes_grc, sampling_period=0.1*ms, border_correction=True, kernel=GaussianKernel(sigma=20 * ms))
        frs.append(firing_rate)
        phase = hilbert(firing_rate)
        phases.append(np.angle(phase))
        # plt.scatter(spikes_grc, np.ones(len(spikes_grc))*i, marker='|', color='red', s = 1)

    # print(f'Phases: {phases}')
    ff = fanofactor(spike_trains)
    print('Fano Factor Grc: ', ff)

    cov = covariance(BinnedSpikeTrain(spike_trains, bin_size=50*ms))
    mean_covar = np.mean(cov)
    print('Covariance (mean) - binsize 50ms: ', mean_covar)

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
    plt.savefig('plm'+conn+'.png')

    mean_pl = np.mean(plm)
    print('Mean Phase Locking Value: ', mean_pl)

    # cross_corr = cross_correlation_histogram(BinnedSpikeTrain(spike_trains, bin_size=10*ms))
    # print('Cross Correlation Histogram: ', np.mean(cross_corr))
    
    np.savetxt('analysis_plv_'+conn+'.txt', (mean_pl, ff, mean_covar, mean_conv))













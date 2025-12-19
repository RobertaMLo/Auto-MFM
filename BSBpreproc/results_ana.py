import numpy as np
from scipy import signal
from neo import io
from os.path import join, realpath, isfile, exists
from os import listdir, makedirs
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
import argparse


def main():


    parser = argparse.ArgumentParser(description="\
                                    Script to read nio file.\
                                    Adapted from neurocomputational lab code. All the glory is theirs ;).\
                                    Usage: nest_base_RL folder_result [options]\
                                     ")

    parser.add_argument("folder_result", help="Absolute path of the folder containing .nio file")
    parser.add_argument("--time_from", help="starting time [ms]", type=float, default=200.00)
    parser.add_argument("--time_to", help="ending time [ms]", type=float, default=5000.00)
    parser.add_argument("--dt", help="integration time [ms]", type = float, default = 0.1)

    args = parser.parse_args()


    time_from = args.time_from
    time_to = args.time_to
    dt = args.dt
    folder_result = args.folder_result

    if not exists(os.path.join(folder_result,'images')):
            makedirs(os.path.join(folder_result,'images'))

    folder_result_images  = os.path.join(folder_result,'images')

    #time_from = 200.00 # in ms
    #time_to = 1200.00 # in ms
    #dt = 0.05 # in ms
    time_resolution = dt /1000. # in second

    #folder_result = "nio_cluster"

    spikes_res = []
    cell_dict = {}
    current_id = 0
    for f in listdir(folder_result):
        file_ = join(folder_result, f)
        if isfile(file_) and (".nio" in file_):
            print(f)
            block = io.NixIO(file_, mode="ro").read_all_blocks()[0]
            spiketrains = block.segments[0].spiketrains

            for st in spiketrains:
                cell_type = st.annotations["device"].split("_rec")[0]
                if (cell_type not in cell_dict) and (cell_type != "stimulus"):
                    cell_dict[cell_type] = {"id": current_id, "senders": []}
                    current_id += 1
                    spikes_res.append([])
                if (cell_type != "stimulus"):
                    if (len(st.annotations["senders"])) > 0:
                        spikes_res[cell_dict[cell_type]["id"]].append(st)
                        cell_dict[cell_type]["senders"].extend(st.annotations["senders"])
    for cell_type in cell_dict:
        print(cell_type)
        cell_dict[cell_type]["senders"] = np.unique(cell_dict[cell_type]["senders"])



    #order_ct = ["mossy_fibers","glomerulus","granule_cell","golgi_cell","purkinje_cell","stellate_cell","basket_cell"]

    order_ct = ["mossy_fibers", "glomerulus","granule","golgi","purkinje", "stellate", "basket"] #questo per config su mio computer. Vedere nomi in yamal

    #order_ct = ["mossy", "gloms","granule","golgi","purkinje","stellate","basket"] #questo per config su mio computer. Vedere nomi in yamal

    u_gids = []
    u_cell_types = []
    for i, cell_type in enumerate(order_ct):
        senders = cell_dict[cell_type]["senders"].tolist()
        print(senders)
        u_gids.extend(senders)
        u_cell_types.extend([i] * len(senders))
    sorting = np.argsort(u_gids)
    u_gids = np.array(u_gids)[sorting]
    u_cell_types = np.array(u_cell_types)[sorting]

    inv_convert = np.full(np.max(u_gids)+1, -1)
    for i, u_gid in enumerate(u_gids):
        inv_convert[u_gid] = i



    tot_num_neuron = len(u_gids)
    all_spikes = np.zeros((int((time_to - time_from) / dt) + 1, tot_num_neuron), dtype=bool)
    for cell_type in order_ct:
        if cell_type not in cell_dict:
            raise Exception(f"No spikes for cell type: {cell_type}")
        print(f"Storing spikes for {cell_type}")
        for st in spikes_res[cell_dict[cell_type]["id"]]:
            spikes = st.magnitude
            senders = inv_convert[np.array(st.annotations["senders"])]
            filter_spikes = (spikes > time_from) * (spikes <= time_to)
            spikes = spikes[filter_spikes]
            spikes = np.asarray(np.floor((spikes - time_from) / dt), dtype=int)
            senders = np.array(senders)[filter_spikes]
            all_spikes[(spikes, senders)] = True



    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return np.float32([float(int(value[i:i + lv // 3], 16)) for i in range(0, lv, lv // 3)])

    num_filter = len(order_ct)
    """
    filter_colors = np.array([


    [0.,0.,0.], # default
    [0, 0, 0], # mf
    [.7, 0.15, 0.15], # grc
    [.196, .808, 0.988], # ubc
    [0,.45,.7], # golgi
    [0.275, 0.800, 0.275], # purkinje
    [1, 0.84, 0], # stellate
    [1, 0.647, 0]]) # basket
    """
    #["mossy","gloms","granule","golgi","purkinje","stellate","basket"]

    filter_colors = np.zeros((num_filter+1, 3), np.float32)

    filter_colors = np.array([ '#0A0A0A', '#D88DBF', '#26CCDB', '#FF0000', '#0306F8', '#037D03', '#FFEB06', '#FF9A06'])
    """
    for i in range(num_filter):
        if i<10:
            filter_colors[i+1] = hex_to_rgb(plt.rcParams['axes.prop_cycle'].by_key()['color'][i])/255.
        else:
            np.random.seed(i + i * 10)
            filter_colors[i + 1] = np.random.rand(3)
            if np.sum(filter_colors[i + 1]) < 1.5:
                filter_colors[i+1] *= 1.5 / np.sum(filter_colors[i+1])
            filter_colors[i + 1][filter_colors[i + 1] > 1.0] = 1.0

            """

    gid2color = filter_colors[u_cell_types + 1]

    nb_neurons = np.zeros(num_filter)
    for i, uf in enumerate(order_ct):
        nb_neurons[i] = np.where(u_cell_types==i)[0].size
    counts = np.zeros(num_filter+1)
    counts[1:] = np.cumsum(nb_neurons)



    fig, ax = plt.subplots(figsize=(15, 7))
    # Fig 1.1: Spike raster plot
    times, newIds = np.where(all_spikes)
    ax.scatter((times + time_from)*dt, newIds, marker='.', c=gid2color[newIds], s=0.005)
    ax.invert_yaxis()
    ax.set_xlabel('Time in ms')
    ax.set_ylabel('Neuron id')
    ax.set_title('Spike raster plot')
    # ax.set_xlim(time_from, time_to)
    ax.set_ylim(0, len(u_gids))
    plt.tight_layout()
    plt.savefig(os.path.join(folder_result_images,"raster_all"))
    plt.clf()

    length_fr = int(np.ceil(num_filter / 2.0)) * 2 # nb rows

    fig = plt.figure(figsize=(15, length_fr * 2))
    # Fig 1.1: Spike raster plots
    for i in range(num_filter):
        times, newIds = np.where(all_spikes[:, int(counts[i]):int(counts[i+1])])
        ax = plt.subplot2grid((length_fr,2), (i//2*2,i%2), rowspan=2)
        ax.scatter((times + time_from)*dt, newIds, marker='o', c=gid2color[newIds + int(counts[i])], s=0.005 * 10000 / nb_neurons[i], alpha=1)
        ax.invert_yaxis()
        ax.set_xlabel('Time in ms')
        ax.set_ylabel('Neuron id')
        ax.set_title(f'Spike raster plot for {order_ct[i]}')
    plt.tight_layout()
    plt.savefig(os.path.join(folder_result_images,"raster.png"), dpi=400, facecolor='white')


    del times, newIds, spikes_res, spiketrains, cell_dict
    plt.close("all")

    # Firing rates computation
    w_single = 500 # steps

    kernel_single = signal.windows.triang(w_single) * 2 / w_single # normalized boxcar kernel for single-trial firing rate

    time_interval = np.arange(time_from + w_single * dt, time_to - w_single * dt + dt / 10., dt)
    firing_rates = np.zeros((all_spikes.shape[0] - w_single * 2, num_filter))
    std_rates = np.zeros((all_spikes.shape[0] - w_single * 2, num_filter))
    fano_factors = np.zeros((all_spikes.shape[0] - w_single * 2, num_filter))
    for i in range(num_filter):
        print(order_ct[i], int(nb_neurons[i]))
        R = signal.lfilter(kernel_single, 1, all_spikes[:, int(counts[i]):int(counts[i+1]):10], axis=0) / time_resolution
        firing_rates[:, i] = np.mean(R, axis=1)[w_single:-w_single]
        #fano_factors[:, i] = (np.var(R, axis=1))[w_single:-w_single] / firing_rates[:, i]
        std_rates[:, i] = np.std(R, axis=1)[w_single:-w_single]


    # Firing rates fig
    fig = plt.figure(figsize=(15, length_fr))
    for i in range(num_filter):
        ax = plt.subplot2grid((length_fr,2), (i//2*2,i%2), rowspan=2)
        ax.fill_between(time_interval, (firing_rates-std_rates)[:, i], (firing_rates+std_rates)[:, i], alpha=0.5, color=filter_colors[i+1])
        ax.plot(time_interval, firing_rates[:, i], color=filter_colors[i+1])
        ax.set_xlabel('Time in ms')
        ax.set_ylabel('Rate in Hz')
        ax.set_title(f'Mean estimated firing rate for {order_ct[i]} (kernel width = {w_single * dt} ms)')
    plt.tight_layout()
    plt.savefig(os.path.join(folder_result_images,"FR.png"))
    plt.clf()

    np.savetxt(os.path.join(folder_result,'pop_firing_rate_avg.txt'), firing_rates)
    np.savetxt(os.path.join(folder_result,'pop_firing_rate_sd.txt'), std_rates)
    print('Population firing rates saved in: ', folder_result)

    order_ct = np.array(order_ct)
    nb_neurons_int = nb_neurons.astype(int)
    vect_all = np.array(list(zip(order_ct, nb_neurons_int) ), dtype = [('string', 'U10'), ('integer', 'i4')])

    np.savetxt(os.path.join(folder_result,'number_cells.txt'), vect_all, fmt = '%s %d', delimiter = ' ')
    print('Population number cells saved in: ', folder_result)


if __name__ == "__main__":
    main()

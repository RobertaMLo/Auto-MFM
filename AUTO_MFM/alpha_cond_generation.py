import numpy as np
import collections
import plotly.graph_objects as go
from random import gauss, seed

def poisson_spikes(t, K, freq, seed = 19):
    #print('Freq passed to poisson spikes generator:  ',freq)
    dt = t[1] - t[0] #just not to pass again dt
    spks = []
    np.random.seed(seed=seed) #init the random generator: for each trial I get the same random numbers

    for n in range(int(K)):
        spkt = t[np.random.rand(len(t)) < freq*dt] # Determine the list of spike time
        idx = [n]*len(spkt) #neuron ID number - same length as spkt
        spkn = np.concatenate([[idx], [spkt]], axis = 0).T #combine the two list
        if len(spkn)>0:
            spks.append(spkn)

    if not spks:
            spks = np.zeros([1, 2])
            spks[0,1] = t.max() +1
    else:
            spks = np.concatenate(spks, axis=0)

    spkt_final = np.sort(spks[:, 1], kind='quicksort') # for the moment just interested in spike times.

    return spkt_final


def spikes_occurrency(t, freq, K):
    spkt_final = poisson_spikes(t, K, freq)
    coll = collections.Counter(spkt_final)
    spkt_and_occur = np.zeros([spkt_final.size, 2])
    i = 0
    for val in coll:
        #print(val, coll[val])
        spkt_and_occur[i,:] = val, coll[val]
        i += 1

    return spkt_and_occur


def g_alpha(t, spks_and_occ, Tsyn, Q):
    """
        Alpha fuction implementation: see Brian documentation.
        https://brian2.readthedocs.io/en/stable/user/converting_from_integrated_form.html

        IDEA: Whene spike events: Update the t-derivative
    """
    dt = t[1] - t[0]
    g0 = 0
    spkt, occ_spkt = spks_and_occ[:, 0], spks_and_occ[:, 1]
    g = np.ones(t.size) * g0  # init to first value
    x = np.ones(t.size) * 0  # x = dg/dtt

    event = 0
    for i in range(1, t.size):
        g[i] = g[i - 1] + dt * (x[i - 1] - g[i - 1] / Tsyn)  # dg/dt
        x[i] = x[i - 1] + dt * (-x[i - 1] / Tsyn)  # dg/dtt

        if event < spkt.size:
            if spkt[event] <= t[i]:
                x[i] = x[i] + ( (Q*occ_spkt[event]) * np.exp(1) / Tsyn)  # Update di dg/dtt
                event += 1

    return g


def g_alpha_exc(t, fe, params):
    #print("\nI'm computing the alpha conductance for excitatory synapses...")
    return g_alpha(t, spikes_occurrency(t, fe, params['Ke']), params['Te'], params['Qe'])


def g_alpha_inhib(t, fi, params):
    #print("\nI'm computing the alpha conductance for inhibithory synapses .....")
    return g_alpha(t, spikes_occurrency(t, fi, params['Ki']), params['Ti'], params['Qi'])

def g_alpha_exc_mossy_goc(t, fe, params):
    #print("\nI'm computing the alpha conductance for mossy-goc synapses .....")
    return g_alpha(t, spikes_occurrency(t, fe, params['Ke_m']), params['Te_m'], params['Qe_m'])

def g_alpha_exc_grc_goc(t, fe, params):
    #print("\nI'm computing the alpha conductance for grc-goc synapses .....")
    return g_alpha(t, spikes_occurrency(t, fe, params['Ke_g']), params['Te_g'], params['Qe_g'])


def plot_g_alpha(t, ge, gi):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=ge,
                             mode='lines',
                             name='g_exc'))
    fig.add_trace(go.Scatter(x=t, y=gi,
                             mode='lines',
                             name='g_inhib'))

    fig.update_layout(title='Exponential Conductance',
                      xaxis_title='t [s]',
                      yaxis_title='g [nS]')
    fig.show()

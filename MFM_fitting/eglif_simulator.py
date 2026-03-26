import numpy as np
from random import gauss, seed
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def set_Ie_distr(t, ie_m, ie_std=10*1e-12):
    seed(1)
    Ie = np.zeros(len(t))
    for ie_ind in range(t.size):
        Ie[ie_ind] = gauss(ie_m, ie_std)

    return Ie

#### RISOLUTORE EGLIF
def eglif_solver(t, I, Ge, Gi,
                 El, Gl, Cm, Ee, Ei, vthresh, vreset, vspike, trefrac, delta_v, kadap, k2, k1, A2, A1, Ie, tm):

    """ I'm the method solving the EGLIF equations
    returns : activity vm, time instant of the spikes t_spikes, adaptation w_vett
    (and other suffs)
    """

    #print("\nNow solving the E-GLIG Model ...........")

    dt = t[1]-t[0]
    last_spike = -np.inf  # time of the last spike, for the refractory period
    V, spikes = El * np.ones(len(t), dtype=float), []
    Vc = []
    w, i_dep, wpi = 0., 0., 0.  # w and i_exp are the exponential and adaptation currents
    waver, wcounting = 0., 0.
    w_vett = np.zeros(len(t), dtype=float)

    Ie_vett = set_Ie_distr(t, Ie)

    #print(Ie_vett)
    #print('------------------', dt)

    #print('Simulation params: length= ', len(self.t)-1,' dt= ',self.dt)
    #print('Gl: ',self.Gl,' Cm: ',self.Cm)

    for i in range(len(t) - 1):
        # print('simulation Step (time) = ',i,' over ',len(t)-1)
        # print('w before update: ', w)
        w = w + dt * (kadap * (V[i] - El) - k2 * w)
        # print('w after update: ', w)
        #i_dep = 0
        i_dep = i_dep + dt * (- k1 * i_dep)
        # print('Adaptation: ', w)
        # print('Depolarization: ', i_dep)

        if i > len(t) / 4:  # only after a transient
            waver += w
            wcounting += 1.0
            # print('wcounting: ', wcounting)
            # wpi += (a * (V[i] - El))
            wpi += (kadap * (V[i] - El) - k2 * w)
            # print('waver = sum di w: ', waver)
            # print('wcounting ', wcounting)


        if i > len(t) / 4:
            if V[i] < vthresh:
                Vc.append(V[i])
                # print('UNDER THRS:\t', 'V= ',V[i], '\t', 'Adap= ', w, '\t', 'Dep= ', i_dep)

        if (t[i] - last_spike) > trefrac:  # only when non refractory

            ## Vm dynamics calculus -- EGLIF Equations
            ## print values each 10 iterarions
            V[i + 1] = V[i] + (dt / Cm) * (Gl * (V[i] - El) - w + i_dep + Ie_vett[i] + I[i] +
                                            Ge[i] * (Ee - V[i]) + Gi[i] * (Ei - V[i]))

            if V[i + 1] < -0.079:
                V[i + 1] = -0.079

            # print('SPIKE:\t','V= ',V[i + 1], '\t', 'Adap= ', w, '\t', 'Dep= ', i_dep)
            # print('\n','\n','INTEGRATE V => V[i+1] = ', V[i+1], '\n','\n')

        if V[i + 1] > vspike:  # what happens when spiking...
        # print('\n','\n',' => V[i+1] = ', V[i+1], ' ; vspike = ', vspike, '  vreset = ', vreset, '\n','\n')

            V[i + 1] = vreset  # reset at t = t_spike
            w = w + A2  # then we increase the adaptation current
            i_dep = A1  # and the depolarisation current
            last_spike = t[i + 1]

            """print('******************************* SPIKE *******************************\n'
                    't spike: ',last_spike, ' v_spike: ',self.vspike)
            print('Reset post spike:\t', 'V = ', V[i + 1], '\t', 'w = ', w, '\t', 'i_dep = ', i_dep)"""


            if last_spike > t.max() / 4:
                # print('Adding one spike to the spikes vector')
                spikes.append(t[i + 1])


        w_vett[i] = w  # save the adaptation current values in the whole simulation

        """
        if i % 100 == 0:  # to print values every 10 iteration
            print('----------------------------------- Iteration # ',i)
            print('V[i]', V[i])
            print('(dt/Cm) * Gl * (V - El): ', (dt/Cm)*Gl*(V[i]-El))
            print('(dt/Cm) * w: ', (dt/Cm)*w)
            print('(dt/Cm) * i dep: ', (dt/Cm)*i_dep)
            print('(dt/Cm) * Ge[i] * (Ee-V[i])', (dt/Cm)*Ge[i]*(Ee-V[i]))
            print('(dt/Cm) * Gi[i] * (Ei-V[i])', (dt/Cm)*Gi[i]*(Ei-V[i]))
        """

    t_spikes = np.array(spikes)

    #w_int = np.trapz(w_vett[int(len(self.t) / 4):], self.t[int(len(self.t) / 4):])

    #print('...... Simulation is ended !!!')

    return V, waver / wcounting, w_vett, t_spikes


def eglif_solver_goc(t, I, Ge_grc, Ge_mossy, Gi, \
              El, Gl, Cm, Ee, Ei, vthresh, vreset, vspike, trefrac, delta_v, kadap, k2, k1, A2, A1, Ie,
              tm):
    """ I'm the method solving the EGLIF equations
        returns : activity vm, time instant of the spikes t_spikes, adaptation w_vett
        (and other suffs)
        """

    # print("\nNow solving the E-GLIG Model ...........")

    dt = t[1] - t[0]
    last_spike = -np.inf  # time of the last spike, for the refractory period
    V, spikes = El * np.ones(len(t), dtype=float), []
    Vc = []
    w, i_dep, wpi = 0., 0., 0.  # w and i_exp are the exponential and adaptation currents
    waver, wcounting = 0., 0.
    w_vett = np.zeros(len(t), dtype=float)

    Ie_vett = set_Ie_distr(t, Ie)

    # print(Ie_vett)
    # print('------------------', dt)

    # print('Simulation params: length= ', len(self.t)-1,' dt= ',self.dt)
    # print('Gl: ',self.Gl,' Cm: ',self.Cm)

    for i in range(len(t) - 1):
        # print('simulation Step (time) = ',i,' over ',len(t)-1)
        # print('w before update: ', w)
        w = w + dt * (kadap * (V[i] - El) - k2 * w)
        # print('w after update: ', w)
        # i_dep = 0
        i_dep = i_dep + dt * (- k1 * i_dep)
        # print('Adaptation: ', w)
        # print('Depolarization: ', i_dep)

        if i > len(t) / 4:  # only after a transient #Standard is 4 but here I put 6
            waver += w
            wcounting += 1.0
            # print('wcounting: ', wcounting)
            # wpi += (a * (V[i] - El))
            wpi += (kadap * (V[i] - El) - k2 * w)
            # print('waver = sum di w: ', waver)
            # print('wcounting ', wcounting)

        if i > len(t) / 4: #Standard is 4 but here I put 6
            if V[i] < vthresh:
                Vc.append(V[i])
                # print('UNDER THRS:\t', 'V= ',V[i], '\t', 'Adap= ', w, '\t', 'Dep= ', i_dep)

        if (t[i] - last_spike) > trefrac:  # only when non refractory

            ## Vm dynamics calculus -- EGLIF Equations
            ## print values each 10 iterarions
            V[i + 1] = V[i] + (dt / Cm) * (Gl * (V[i] - El) - w + i_dep + Ie_vett[i] + I[i] +
                                           Ge_grc[i] * (Ee - V[i]) + Ge_mossy[i] * (Ee - V[i]) + Gi[i] * (Ei - V[i]))

            # print('SPIKE:\t','V= ',V[i + 1], '\t', 'Adap= ', w, '\t', 'Dep= ', i_dep)
            # print('\n','\n','INTEGRATE V => V[i+1] = ', V[i+1], '\n','\n')


            if V[i + 1] < -0.079:
                V[i + 1] = -0.079

        if V[i + 1] > vspike:  # what happens when spiking...
            # print('\n','\n',' => V[i+1] = ', V[i+1], ' ; vspike = ', vspike, '  vreset = ', vreset, '\n','\n')

            V[i + 1] = vreset  # reset at t = t_spike
            w = w + A2  # then we increase the adaptation current
            i_dep = A1  # and the depolarisation current
            last_spike = t[i + 1]

            """print('******************************* SPIKE *******************************\n'
                    't spike: ',last_spike, ' v_spike: ',self.vspike)
            print('Reset post spike:\t', 'V = ', V[i + 1], '\t', 'w = ', w, '\t', 'i_dep = ', i_dep)"""

            if last_spike > t.max() / 4:
                # print('Adding one spike to the spikes vector')
                spikes.append(t[i + 1])

        w_vett[i] = w  # save the adaptation current values in the whole simulation

        """
        if i % 100 == 0:  # to print values every 10 iteration
            print('----------------------------------- Iteration # ',i)
            print('V[i]', V[i])
            print('(dt/Cm) * Gl * (V - El): ', (dt/self.Cm)*self.Gl*(V[i]-self.El))
            print('(dt/Cm) * w: ', (dt/self.Cm)*w)
            print('(dt/Cm) * i dep: ', (dt/self.Cm)*i_dep)
            print('(dt/Cm) * Ge[i] * (Ee-V[i])', (dt/self.Cm)*Ge[i]*(self.Ee-V[i]))
            print('(dt/Cm) * Gi[i] * (Ei-V[i])', (dt/self.Cm)*Gi[i]*(self.Ei-V[i]))
            """

    t_spikes = np.array(spikes)

    # w_int = np.trapz(w_vett[int(len(self.t) / 4):], self.t[int(len(self.t) / 4):])

    # print('...... Simulation is ended !!!')

    return V, waver / wcounting, w_vett, t_spikes


######## CALCOLA IL VALORE DI TF
def froutput_single_experiment(t, t_spikes):
    #print('Number of spikes: ', len(t_spikes))
    return (len(t_spikes)/ (3 * t.max() / 4))


def plot_eglif(t, V, w, tspikes):

    fig = make_subplots(rows=2, cols=1, subplot_titles=('Activity [V]', 'Adaptation [A]'))

    fig.add_trace(go.Scatter(x=t, y=V, mode='lines', name='Vm',  line=dict(color = "salmon")),
                      row=1, col=1)

    fig.add_trace(go.Scatter(x=t, y=w, mode='lines', name='W'),
                      row=2, col=1)

    fig.update_layout(title='# of spikes: '+str(len(tspikes)),
                          xaxis_title='t [s]')
    fig.show()
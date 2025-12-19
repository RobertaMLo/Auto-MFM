import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
sys.path.append('../')
import os

from load_config_TF import *
from master_equation_CRBL_MF import *
from theoretical_tools import *


def plot_MF_activity(t, X, title):
    fig = go.Figure()

    fig = make_subplots(rows=5, cols=1)

    fig.add_trace(go.Scatter(x=t, y=X[:,0],
                                 mode='lines',
                                 name='GrC',
                                 line=dict(color = "red")),
                      row=4, col=1
                      )

    fig.add_trace(go.Scatter(x=t, y=X[:,1],
                                 mode='lines',
                                 name='GoC',
                                 line=dict(color = "blue")),
                      row=3, col=1
                      )
    fig.add_trace(go.Scatter(x=t, y=X[:,9],
                                 mode='lines',
                                 name='MLI',
                                 line=dict(color = "orange")),
                      row=2, col=1
                      )

    fig.add_trace(go.Scatter(x=t, y=X[:,10],
                                 mode='lines',
                                 name='PCz-',
                                 line=dict(color = "green")),
                      row=1, col=1
                      )

    fig.add_trace(go.Scatter(x=t, y=X[:,8],
                                 mode='lines',
                                 name='mossy fibers',
                                 line=dict(color = "black")),
                      row=5, col=1
                      )


    fig.update_xaxes(title_text="time [s]", row=5, col=1)


    # Update yaxis properties
    fig.update_yaxes(title_text="Activity [Hz]", row=3, col=1)
    """
    fig.update_yaxes(title_text="GrC[Hz]", row=4, col=1)
    fig.update_yaxes(title_text="GoC[Hz]", row=3, col=1)
    fig.update_yaxes(title_text="MLI[Hz]", row=2, col=1)
    fig.update_yaxes(title_text="PC[Hz]", row=1, col=1)
    fig.update_yaxes(title_text="mf[Hz]", row=5, col=1)
    """
    axis_style = dict(
      showline=True,
      linecolor='black',
      linewidth=1,
      showgrid=False,
      zeroline=False,
      mirror=False        #true to have the box
    )


    # Update title
    fig.update_layout(
                      title_text=title,
                      height=600, width=400,
                      plot_bgcolor = 'rgba(0,0,0,0)', #remove bckg
                      xaxis=axis_style, xaxis2=axis_style, xaxis3=axis_style, xaxis4=axis_style, xaxis5=axis_style,
                      yaxis=axis_style, yaxis2=axis_style, yaxis3=axis_style, yaxis4=axis_style, yaxis5=axis_style,
                      font=dict(family="Arial, sans-serif", size=14, color="black")
    )



    for i, idx in enumerate([10, 9, 1, 0, 8]):  # Indici delle colonne in X
      y_min, y_max = np.min(X[:, idx]), np.max(X[:, idx])
      tick_values = np.linspace(y_min, y_max, 3)
      fig.update_yaxes(tickmode="array", tickvals=tick_values, tickformat=".0f", row=i+1, col=1)

    fig.show()


def rect_input(time, t_start, t_end, minval, freq, noise_freq):

        """
        time = time vector of simulation
        t_start = start of the step INDEX
        t_end = end of the step INDEX
        minval = baseline value (deviation from 0)
        freq = peak value
        noise_freq = random noise frequencies
        """

        y = np.ones(len(time)) * freq + np.random.rand(len(time)) * noise_freq
        y[:t_start] = y[:t_start]*0+np.random.rand(t_start)*noise_freq
        y[t_end:] = y[t_end:]*0+np.random.rand(len(time) - t_end)*noise_freq
        y = y + minval

        return y


if __name__ == '__main__':
    

    root_path = os.getcwd()+'/' #folder where P coefficients were stored
    NTWK = 'CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC'

    FILE_GrC = root_path  + '20250605_163824_GrC_CRBL_CONFIG_PLV_ONLYK_tsim5_alpha2.0_fit.npy'

    FILE_GoC = root_path + '20250624_200053_GoC_CRBL_CONFIG_PLV_ONLYK_new_tsim5_alpha2.0_fit.npy'

    FILE_MLI = root_path + '20250625_151658_MLI_CRBL_CONFIG_PLV_ONLYK_GoCasorev00_tsim5_alpha1.8_fit.npy'

    FILE_PC = root_path + '20250702_235209_PC_CRBL_CONFIG_PLV_ONLYK_GoCautoinib_asorev00_debugQmliPC_tsim5_alpha2.3_fit.npy'

    NRN1, NRN2, NRN3, NRN4 = 'GrC', 'GoC', 'MLI', 'PC'

    TFgrc = load_transfer_functions(NRN1, NTWK, FILE_GrC, alpha=2.0)
    TFgoc = load_transfer_functions_goc(NRN2, NTWK, FILE_GoC, alpha=2)
    TFmli = load_transfer_functions(NRN3, NTWK, FILE_MLI, alpha=1.8)
    TFpc = load_transfer_functions(NRN4, NTWK, FILE_PC, alpha=6)

    Ngrc = 29916
    Ngoc = 71
    Nmossy = 2340
    Nmli = 302+150
    Npc = 69

    dt = 1e-4
    sim_len = 0.5
    t = np.arange(0, sim_len, dt)

    T = 3.5e-3
    w = 0. #adaptation not included at the moment

    

    f_backnoise = np.random.rand(len(t))*4
    
    CI_vec = [0.5, 5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, f_backnoise[0], 15, 38, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]

    X_back = find_fixed_point_mossy(TFgrc, TFgoc, TFmli, TFpc, CI_vec, t, w, f_backnoise,
                            Ngrc, Ngoc, Nmossy, Nmli, Npc, T, verbose=False)


    
    #plot_MF_activity_withSD(t[1000:], X_cort[1000:], fmossy_cort[1000:], mytitle = 'Baseline', font_size = 12, linew=1.5)
    plot_MF_activity(t, X_back, 'Backnoise')


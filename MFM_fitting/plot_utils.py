import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

import sys
import numpy as np
sys.path.append('../')


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
                                 name='PCz',
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
                      height=600, width=800,
                      plot_bgcolor = 'rgba(0,0,0,0)', #remove bckg
                      xaxis=axis_style, xaxis2=axis_style, xaxis3=axis_style, xaxis4=axis_style, xaxis5=axis_style,
                      yaxis=axis_style, yaxis2=axis_style, yaxis3=axis_style, yaxis4=axis_style, yaxis5=axis_style,
                      font=dict(family="Arial, sans-serif", size=16, color="black")
    )



    for i, idx in enumerate([10, 9, 1, 0, 8]):  # Indici delle colonne in X
      y_min, y_max = np.min(X[:, idx]), np.max(X[:, idx])
      tick_values = np.linspace(y_min, y_max, 3)
      fig.update_yaxes(tickmode="array", tickvals=tick_values, tickformat=".0f", row=i+1, col=1)

    fig.show()



def plot_MF_activity_withSD(t, X, finput, mytitle, font_size=22, linew=1.5):
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(2.4, 4.1))  # for half of 1/4 of A4
    fig.suptitle(mytitle, fontsize=font_size + 2)

    def get_three_ticks(data, variance):
        """
        To get equispaced ticks based on avg and std
        """
        y_min = np.min(data - np.sqrt(variance))
        y_max = np.max(data + np.sqrt(variance))
        y_mid = (y_min + y_max) / 2
        return [round(y_min), round(y_mid), round(y_max)]

    # PC --------------------------------------------------------------------------------------------------------------

    pc_line, = ax1.plot(t, X[:, 10], 'green', linewidth=linew, label='PC')
    ax1.fill_between(t, X[:, 10] - np.sqrt(X[:, 15]), X[:, 10] + np.sqrt(X[:, 15]), color='green', alpha=0.5)

    # Three ticks for each subplot (max min and middle point between max and min)
    ax1.set_yticks(get_three_ticks(X[:, 10], X[:, 15]))

    ax1.set_xticks([])

    # MLI --------------------------------------------------------------------------------------------------------------
    mli_line, = ax2.plot(t, X[:, 9], 'orange', linewidth=linew, label='MLI')
    ax2.fill_between(t, X[:, 9] + np.sqrt(abs(X[:, 11])), X[:, 9] - np.sqrt(abs(X[:, 11])), facecolor='orange',
                     alpha=0.5)

    ax2.set_yticks(get_three_ticks(X[:, 9], X[:, 11]))

    ax2.set_xticks([])

    # GoC --------------------------------------------------------------------------------------------------------------
    goc_line, = ax3.plot(t, X[:, 1], 'blue', linewidth=linew, label='GoC')
    ax3.fill_between(t, X[:, 1] + np.sqrt(abs(X[:, 6])), X[:, 1] - np.sqrt(abs(X[:, 6])), facecolor='blue', alpha=0.5)

    # to get the generic y labels at middle of suplots
    ax3.set_ylabel('Activity [Hz]', fontsize=font_size, ha='center', va='center', labelpad=20)

    ax3.set_yticks(get_three_ticks(X[:, 1], X[:, 6]))

    ax3.set_xticks([])

    # GrC --------------------------------------------------------------------------------------------------------------
    grc_line, = ax4.plot(t, X[:, 0], 'red', linewidth=linew, label='GrC')
    ax4.fill_between(t, X[:, 0] + np.sqrt(abs(X[:, 2])), X[:, 0] - np.sqrt(abs(X[:, 2])), facecolor='red', alpha=0.5)

    ax4.set_yticks(get_three_ticks(X[:, 0], X[:, 2]))

    ax4.set_xticks([])

    # Input ------------------------------------------------------------------------------------------------------------
    input_line, = ax5.plot(t, finput, 'black', linewidth=linew, label='Input')

    ax5.set_yticks(get_three_ticks(finput, np.zeros_like(finput)))

    ax5.set_xlabel('time [s]', fontsize=font_size, ha='center', va='center', labelpad=20)

    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # fig.tight_layout()
    fig.subplots_adjust(hspace=0.5, top=0.92, bottom=0.1)

    legend_lines = [pc_line, mli_line, goc_line, grc_line, input_line]

    fig.legend(handles=legend_lines, loc="center left", fontsize=font_size - 2, ncol=1, frameon=True,
               bbox_to_anchor=(0.95, 0.5))

    plt.show()


def plot_MF_activity_withSD_more(t, X, finput, mytitle, font_size=14, linew=1.5, axes = None):

    if axes is None:
      fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5, 1, figsize=(2.4, 4.1))  # for half of 1/4 of A4
      fig.suptitle(mytitle, fontsize=font_size + 2)

    else:
        fig = axes[0].figure

    ax1, ax2, ax3, ax4, ax5 = axes

    def get_three_ticks(data, variance):
        """
        To get equispaced ticks based on avg and std
        """
        y_min = np.min(data - np.sqrt(variance))
        y_max = np.max(data + np.sqrt(variance))
        y_mid = (y_min + y_max) / 2
        return [round(y_min), round(y_mid), round(y_max)]

    # PC --------------------------------------------------------------------------------------------------------------

    pc_line, = ax1.plot(t, X[:, 10], 'green', linewidth=linew, label='PC')
    ax1.fill_between(t, X[:, 10] - np.sqrt(X[:, 15]), X[:, 10] + np.sqrt(X[:, 15]), color='green', alpha=0.2)

    # Three ticks for each subplot (max min and middle point between max and min)
    ax1.set_yticks(get_three_ticks(X[:, 10], X[:, 15]))

    ax1.set_xticks([])

    # MLI --------------------------------------------------------------------------------------------------------------
    mli_line, = ax2.plot(t, X[:, 9], 'orange', linewidth=linew, label='MLI')
    ax2.fill_between(t, X[:, 9] + np.sqrt(abs(X[:, 11])), X[:, 9] - np.sqrt(abs(X[:, 11])), facecolor='orange',
                     alpha=0.5)

    ax2.set_yticks(get_three_ticks(X[:, 9], X[:, 11]))

    ax2.set_xticks([])

    # GoC --------------------------------------------------------------------------------------------------------------
    goc_line, = ax3.plot(t, X[:, 1], 'blue', linewidth=linew, label='GoC')
    ax3.fill_between(t, X[:, 1] + np.sqrt(abs(X[:, 6])), X[:, 1] - np.sqrt(abs(X[:, 6])), facecolor='blue', alpha=0.2)

    # to get the generic y labels at middle of suplots
    ax3.set_ylabel('Activity [Hz]', fontsize=font_size, ha='center', va='center', labelpad=20)

    ax3.set_yticks(get_three_ticks(X[:, 1], X[:, 6]))

    ax3.set_xticks([])

    # GrC --------------------------------------------------------------------------------------------------------------
    grc_line, = ax4.plot(t, X[:, 0], 'red', linewidth=linew, label='GrC')
    ax4.fill_between(t, X[:, 0] + np.sqrt(abs(X[:, 2])), X[:, 0] - np.sqrt(abs(X[:, 2])), facecolor='red', alpha=0.2)

    ax4.set_yticks(get_three_ticks(X[:, 0], X[:, 2]))

    ax4.set_xticks([])

    # Input ------------------------------------------------------------------------------------------------------------
    input_line, = ax5.plot(t, finput, 'black', linewidth=0.9, label='Input')

    ax5.set_yticks(get_three_ticks(finput, np.zeros_like(finput)))

    ax5.set_xlabel('time [s]', fontsize=font_size, ha='center', va='center', labelpad=20)

    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    # fig.tight_layout()
    fig.subplots_adjust(hspace=0.5, top=0.92, bottom=0.1)

    legend_lines = [pc_line, mli_line, goc_line, grc_line, input_line]

    fig.legend(handles=legend_lines, loc="center left", fontsize=font_size - 2, ncol=1, frameon=True,
               bbox_to_anchor=(0.95, 0.5))

    return fig, axes
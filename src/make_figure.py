import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib as mpl


def figure_plotter():
    """A function to plot the main result of the paper"""

    sns.set_style('ticks')
    mpl.rcParams['font.family'] = 'Helvetica'
    search_path = os.path.join(os.getcwd(), '..', 'data',
                               'scopus', 'search')

    soci_temporal = pd.read_csv(os.path.join(search_path, 'temporal', 'SOCI.tsv'),
                                sep='\t', index_col=0)
    busi_temporal = pd.read_csv(os.path.join(search_path, 'temporal', 'BUSI.tsv'),
                                sep='\t', index_col=0)
    econ_temporal = pd.read_csv(os.path.join(search_path, 'temporal', 'ECON.tsv'),
                                sep='\t', index_col=0)
    comb_temporal = busi_temporal + soci_temporal + econ_temporal
    comb_temporal = comb_temporal[90:]
    soci_temporal = soci_temporal[90:]
    busi_temporal = busi_temporal[90:]
    econ_temporal = econ_temporal[90:]
    soci_temporal['pc_ML'] = (soci_temporal['is_ML'] / soci_temporal['Total']) * 100
    busi_temporal['pc_ML'] = (busi_temporal['is_ML'] / busi_temporal['Total']) * 100
    econ_temporal['pc_ML'] = (econ_temporal['is_ML'] / econ_temporal['Total']) * 100
    comb_temporal['pc_ML'] = (comb_temporal['is_ML'] / comb_temporal['Total']) * 100
    df_topics = pd.read_csv(os.path.join(search_path, 'topics', 'topics_df.tsv'),
                            sep='\t', index_col=0)
    df_topics = df_topics[df_topics.sum().sort_values(ascending=False).index]
    df_topics = df_topics.loc[df_topics.sum(axis=1).sort_values(ascending=False).index]
    df_topics.drop('is_ML', axis=1, inplace=True)
    df_topics = df_topics * 100
    scalar_dict = {}
    for subj in ['BUSI', 'ECON', 'SOCI']:
        with open(os.path.join(search_path, 'scalars', subj + '.txt'), 'r') as f:
            scalar_dict[subj] = float(f.read())

    fig, (ax1) = plt.subplots(1, 1, figsize=(14, 14 / 1.618))
    comb_temporal['pc_ML'].plot(ax=ax1, color='#3e8abb', zorder=2)
    ax1.tick_params(axis='y', which='minor', bottom=False)
    ax1.tick_params(axis='x', which='minor', bottom=False)
    ax1.xaxis.set_tick_params(labelsize=14)
    ax1.yaxis.set_tick_params(labelsize=14)
    ax1.set_xlim(0, ax1.get_xlim()[1])
    ax1.spines['bottom'].set_bounds(0, ax1.get_xlim()[1] - 18)
    ax1.set_ylim(-.1, ax1.get_ylim()[1])
    ax1.spines['right'].set_bounds(0, ax1.get_ylim()[1])
    ax1.yaxis.set_label_position("right")
    ax1.set_ylabel('Proportion of Machine Learning  Articles', fontsize=16)
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))

    inset_ax = inset_axes(ax1,
                          width="110%",
                          height="120%",
                          loc='upper left',
                          bbox_to_anchor=(0.0825, 0.6, .24, .4),
                          bbox_transform=ax1.transAxes)
    n_colors = 256
    palette = sns.diverging_palette(220, 20, n=n_colors)
    color_min, color_max = [0, df_topics.max().max()]
    corr = pd.melt(df_topics.reset_index(), id_vars='index')
    corr.columns = ['x', 'y', 'value']
    x = corr['x']
    y = corr['y']
    size = corr['value'].abs()
    x_labels = [v for v in x.unique()]
    y_labels = [v for v in y.unique()]
    x_to_num = {p[1]: p[0] for p in enumerate(x_labels)}
    y_to_num = {p[1]: p[0] for p in enumerate(y_labels)}
    size_scale = 80

    def value_to_color(val):
        val_position = float((val - color_min)) / \
                       (color_max - color_min)
        ind = int(val_position * (n_colors - 1))
        return palette[ind]

    inset_ax.scatter(x=x.map(x_to_num), y=y.map(y_to_num),
                     s=size * size_scale, c=corr['value'].apply(value_to_color),
                     marker='o', edgecolor='k', linewidth=0.75)
    inset_ax.set_xticks([x_to_num[v] for v in x_labels])
    inset_ax.set_xticklabels(x_labels, rotation=0)
    inset_ax.set_yticks([y_to_num[v] for v in y_labels])
    inset_ax.set_yticklabels(y_labels)
    inset_ax.xaxis.set_tick_params(labelsize=13)
    inset_ax.yaxis.set_tick_params(labelsize=13)
    inset_ax.set_xlim([-.66, max([v for v in x_to_num.values()]) + 0.5])
    inset_ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    inset_ax.tick_params(left=True, right=False, top=False,
                         labelleft=True, labelright=False, labeltop=False,
                         rotation=0)
    sns.despine(ax=inset_ax)
    axins = inset_axes(inset_ax, width="5%", height="110%", loc='right',
                       bbox_to_anchor=(0.2, 0.05, .875, 0.9),
                       bbox_transform=inset_ax.transAxes, borderpad=0)
    col_x = [0] * len(palette)
    bar_y = np.linspace(color_min, color_max, n_colors)
    bar_height = bar_y[1] - bar_y[0]
    axins.barh(y=bar_y, width=[5] * len(palette), left=col_x,
               height=bar_height, color=palette, linewidth=0)
    axins.set_ylim(bar_y.min(), bar_y.max())
    axins.set_xlim(1, 2)
    axins.grid(False)
    axins.yaxis.set_tick_params(labelsize=13)
    axins.set_facecolor('white')
    axins.set_xticks([])
    axins.set_yticks(np.linspace(min(bar_y), max(bar_y), 5))
    axins.yaxis.tick_right()
    axins.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
    for tick in inset_ax.get_xticklabels():
        tick.set_rotation(90)

    #    ax1.annotate('', xy=(1575, scalar_dict['ECON']),
    #                 xytext=(1450, scalar_dict['ECON']),
    #                 arrowprops=dict(arrowstyle='-|>', color='#ffb94e'))
    #    ax1.annotate('ECON ('+ str(round(scalar_dict['ECON'], 1)) +'%)',
    #                 xy=(1555, scalar_dict['ECON']+.025),
    #                 xytext=(1562, scalar_dict['ECON']+.025),
    #                 horizontalalignment='right',
    #                 verticalalignment='bottom',
    #                 fontsize=9)
    #
    #    ax1.annotate('', xy=(1575, scalar_dict['SOCI']),
    #                 xytext=(1450, scalar_dict['SOCI']),
    #                 arrowprops=dict(arrowstyle='-|>', color='#ffb94e'))
    #    ax1.annotate('SOCI ('+ str(round(scalar_dict['SOCI'], 1)) +'%)',
    #                 xy=(1555, scalar_dict['SOCI']+.025),
    #                 xytext=(1555, scalar_dict['SOCI']+.025),
    #                 horizontalalignment='right',
    #                 verticalalignment='bottom',
    #                 fontsize=9)
    #
    #    ax1.annotate('', xy=(1575, scalar_dict['BUSI']),
    #                 xytext=(1450, scalar_dict['BUSI']),
    #                 arrowprops=dict(arrowstyle='-|>', color='#ffb94e'))
    #    ax1.annotate('BUSI ('+ str(round(scalar_dict['BUSI'], 1)) +'%)',
    #                 xy=(1555, scalar_dict['BUSI']+.025),
    #                 xytext=(1555, scalar_dict['BUSI']+.025),
    #                 horizontalalignment='right',
    #                 verticalalignment='bottom',
    #                 fontsize=9)
    annot_fontsize = 14
    ax1.annotate("Hopfield (1982) popularizes\n      'Hopfield networks'",
                 xy=(201, comb_temporal.iloc[491]['pc_ML'] + .3), xycoords='data',
                 xytext=(201, comb_temporal.iloc[491]['pc_ML'] + .3),
                 fontsize=annot_fontsize, textcoords='data',
                 bbox=dict(boxstyle="round, pad=0.75", fc="w",
                           linewidth=.6, edgecolor=(0, 0, 0, 1)),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3, rad=-0.3",
                                 linewidth=0.5, edgecolor='w'))

    ax1.annotate("Leo Breiman (1996):\n'Bagging Predictors'",
                 xy=(650, comb_temporal.iloc[865]['pc_ML'] + .275), xycoords='data',
                 xytext=(650, comb_temporal.iloc[865]['pc_ML'] + .275),
                 fontsize=annot_fontsize, textcoords='data',
                 bbox=dict(boxstyle="round, pad=0.75", fc="w",
                           linewidth=.6, edgecolor=(0, 0, 0, 1)),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3, rad=-0.3",
                                 linewidth=0.5, edgecolor='w'))

    ax1.annotate("  Friedman et al. (2001): 'The\nElements of Statistical Learning'",
                 xy=(710, comb_temporal.iloc[978]['pc_ML'] + .6), xycoords='data',
                 xytext=(710, comb_temporal.iloc[978]['pc_ML'] + .6),
                 fontsize=annot_fontsize, textcoords='data',
                 bbox=dict(boxstyle="round, pad=0.75", fc="w",
                           linewidth=.6, edgecolor=(0, 0, 0, 1)),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3, rad=-0.3",
                                 linewidth=0.5, edgecolor='w'))

    ax1.annotate("   ImageNet improves\nvisual object recognition",
                 xy=(935, comb_temporal.iloc[1201]['pc_ML'] + .8), xycoords='data',
                 xytext=(935, comb_temporal.iloc[1201]['pc_ML'] + .8),
                 fontsize=annot_fontsize, textcoords='data',
                 bbox=dict(boxstyle="round, pad=0.75", fc="w",
                           linewidth=.6, edgecolor=(0, 0, 0, 1)),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3, rad=-0.3",
                                 linewidth=0.5, edgecolor='w'))

    ax1.annotate("   Nate Silver predicts\n50 states in US election",
                 xy=(1020, comb_temporal.iloc[1293]['pc_ML'] + 1.235), xycoords='data',
                 xytext=(1020, comb_temporal.iloc[1293]['pc_ML'] + 1.235),
                 fontsize=annot_fontsize, textcoords='data',
                 bbox=dict(boxstyle="round, pad=0.75", fc="w",
                           linewidth=.6, edgecolor='k'),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3, rad=-0.3",
                                 linewidth=0.5, edgecolor='w'))

    ax1.annotate("RSF launches Computational\n    Social Science initiative",
                 xy=(1040, comb_temporal.iloc[1356]['pc_ML'] + 1.7), xycoords='data',
                 xytext=(1040, comb_temporal.iloc[1356]['pc_ML'] + 1.7),
                 fontsize=annot_fontsize, textcoords='data',
                 bbox=dict(boxstyle="round, pad=0.75", fc="w",
                           linewidth=.6, edgecolor=(0, 0, 0, 1)),
                 arrowprops=dict(arrowstyle="->",
                                 connectionstyle="arc3, rad=-0.3",
                                 linewidth=0.5, edgecolor='w',
                                 linestyle='--'))

    ax1.plot(0, comb_temporal.iloc[0]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(491, comb_temporal.iloc[491]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(865, comb_temporal.iloc[865]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(978, comb_temporal.iloc[978]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(1201, comb_temporal.iloc[1201]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(1293, comb_temporal.iloc[1293]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(1356, comb_temporal.iloc[1356]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.plot(1500, comb_temporal.iloc[1500]['pc_ML'] + 0.01, marker='o',
             markersize=8, markerfacecolor='#f46d43', markeredgecolor='k')

    ax1.vlines(0, ax1.get_ylim()[0], comb_temporal.iloc[0]['pc_ML'],
               colors='k', linewidth=0.8, linestyle=(0, (5, 5)), color='#F47174')
    #    ax1.vlines(491, ax1.get_ylim()[0], comb_temporal.iloc[491]['pc_ML'],
    #               colors='k', linewidth=0.8, linestyle = (0, (5, 5)), color='#F47174')
    #    ax1.vlines(865, ax1.get_ylim()[0], comb_temporal.iloc[865]['pc_ML'],
    #               colors='k', linewidth=0.8, linestyle = (0, (5, 5)), color='#F47174')
    ax1.vlines(978, ax1.get_ylim()[0], comb_temporal.iloc[978]['pc_ML'],
               colors='k', linewidth=0.8, linestyle=(0, (5, 5)), color='#F47174')
    #    ax1.vlines(1201, ax1.get_ylim()[0], comb_temporal.iloc[1201]['pc_ML'],
    #               colors='k', linewidth=0.8, linestyle = (0, (5, 5)), color='#F47174')
    ax1.vlines(1293, ax1.get_ylim()[0], comb_temporal.iloc[1293]['pc_ML'],
               colors='k', linewidth=0.8, linestyle=(0, (5, 5)), color='#F47174')
    #    ax1.vlines(1370, ax1.get_ylim()[0], comb_temporal.iloc[1371]['pc_ML'],
    #               colors='k', linewidth=0.8, linestyle = (0, (5, 5)), color='#F47174')
    ax1.vlines(1501, ax1.get_ylim()[0], comb_temporal.iloc[1500]['pc_ML'],
               colors='k', linewidth=0.8, linestyle=(0, (5, 5)), color='#F47174')

    ax1.annotate('', xy=(1501, 0.155),
                 xytext=(1465, 0.155),
                 arrowprops=dict(arrowstyle='-|>', color='#ffb94e'))
    ax1.annotate('BUSI (' + str(round(busi_temporal.iloc[1500]['pc_ML'], 2)) + '%)',
                 xy=(1460, 0.195),
                 xytext=(1460, 0.195),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    ax1.annotate('SOCI (' + str(round(soci_temporal.iloc[1500]['pc_ML'], 2)) + '%)',
                 xy=(1460, 0.12),
                 xytext=(1460, 0.12),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    ax1.annotate('ECON (' + str(round(econ_temporal.iloc[1500]['pc_ML'], 2)) + '%)',
                 xy=(1460, 0.045),
                 xytext=(1460, 0.045),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)

    ax1.annotate('', xy=(1293, 0.155),
                 xytext=(1232, 0.155),
                 arrowprops=dict(arrowstyle='-|>', color='#ffb94e'))
    ax1.annotate('BUSI (' + str(round(busi_temporal.iloc[1292]['pc_ML'], 2)) + '%)',
                 xy=(1226, 0.195),
                 xytext=(1226, 0.195),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    ax1.annotate('SOCI (' + str(round(soci_temporal.iloc[1292]['pc_ML'], 2)) + '%)',
                 xy=(1226, 0.12),
                 xytext=(1226, 0.12),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    ax1.annotate('ECON (' + str(round(econ_temporal.iloc[1292]['pc_ML'], 2)) + '%)',
                 xy=(1226, 0.045),
                 xytext=(1226, 0.045),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)

    ax1.annotate('', xy=(978, 0.155),
                 xytext=(917, 0.155),
                 arrowprops=dict(arrowstyle='-|>', color='#ffb94e'))
    ax1.annotate('BUSI (' + str(round(busi_temporal.iloc[977]['pc_ML'], 2)) + '%)',
                 xy=(912, 0.195),
                 xytext=(912, 0.195),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    ax1.annotate('SOCI (' + str(round(soci_temporal.iloc[977]['pc_ML'], 2)) + '%)',
                 xy=(912, 0.12),
                 xytext=(912, 0.12),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    ax1.annotate('ECON (' + str(round(econ_temporal.iloc[977]['pc_ML'], 2)) + '%)',
                 xy=(912, 0.045),
                 xytext=(912, 0.045),
                 horizontalalignment='right',
                 verticalalignment='bottom',
                 fontsize=11)
    inset_ax.spines['left'].set_bounds(0, 7)
    inset_ax.spines['bottom'].set_bounds(0, 9)

    from matplotlib.patches import FancyArrowPatch
    myArrow = FancyArrowPatch(posA=(1293, comb_temporal.iloc[1293]['pc_ML'] + .035),
                              posB=(1293, comb_temporal.iloc[1293]['pc_ML'] + 1.2),
                              arrowstyle='<|-', linewidth=.6,
                              linestyle='-', edgecolor=(0, 0, 0, 1), facecolor='#f46d43',
                              mutation_scale=20)
    ax1.add_artist(myArrow)
    myArrow = FancyArrowPatch(posA=(1356, comb_temporal.iloc[1356]['pc_ML'] + .035),
                              posB=(1356, comb_temporal.iloc[1356]['pc_ML'] + 1.7),
                              arrowstyle='<|-', linewidth=.6,
                              linestyle='-', edgecolor=(0, 0, 0, 1), facecolor='#f46d43',
                              mutation_scale=20)
    ax1.add_artist(myArrow)

    myArrow = FancyArrowPatch(posA=(978, comb_temporal.iloc[978]['pc_ML'] + .035),
                              posB=(978, comb_temporal.iloc[978]['pc_ML'] + .6),
                              arrowstyle='<|-', linewidth=.6,
                              linestyle='-', edgecolor=(0, 0, 0, 1), facecolor='#f46d43',
                              mutation_scale=20)
    ax1.add_artist(myArrow)

    myArrow = FancyArrowPatch(posA=(1201, comb_temporal.iloc[1201]['pc_ML'] + .035),
                              posB=(1201, comb_temporal.iloc[1201]['pc_ML'] + .8),
                              arrowstyle='<|-', linewidth=.75,
                              linestyle='-', edgecolor=(0, 0, 0, 1), facecolor='#f46d43',
                              mutation_scale=20)
    ax1.add_artist(myArrow)

    myArrow = FancyArrowPatch(posA=(865, comb_temporal.iloc[865]['pc_ML'] + .035),
                              posB=(865, comb_temporal.iloc[865]['pc_ML'] + .275),
                              arrowstyle='<|-', linewidth=.6,
                              linestyle='-', edgecolor=(0, 0, 0, 1), facecolor='#f46d43',
                              mutation_scale=20)
    ax1.add_artist(myArrow)

    myArrow = FancyArrowPatch(posA=(491, comb_temporal.iloc[491]['pc_ML'] + .035),
                              posB=(491, comb_temporal.iloc[491]['pc_ML'] + .3),
                              arrowstyle='<|-', linewidth=.6,
                              linestyle='-', edgecolor=(0, 0, 0, 1), facecolor='#f46d43',
                              mutation_scale=20)
    ax1.add_artist(myArrow)

    sns.despine(ax=ax1, left=True, right=False, bottom=False)
    sns.despine(ax=inset_ax, left=False, right=True, top=True, bottom=False)
    figure_path = os.path.join(search_path, '..', '..', '..', 'figures')
    plt.savefig(os.path.join(figure_path, 'ML_Over_Time.png'), bbox_inches='tight', dpi=1400)
    plt.savefig(os.path.join(figure_path, 'ML_Over_Time.pdf'), bbox_inches='tight')
    plt.savefig(os.path.join(figure_path, 'ML_Over_Time.svg'), bbox_inches='tight')

if __name__ == "__main__":
    figure_plotter()

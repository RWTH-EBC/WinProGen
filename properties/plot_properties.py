# -*- coding: utf-8 -*-
from _lsprof import profiler_entry
from fileinput import filename
import pandas as pd
from pandas import Series, DataFrame, MultiIndex
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.gridspec as gridspec
import numpy as np
from src.layout import *
from src.utils import *
import os
import glob
import matplotlib.collections as collections
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
from pandas import Series, DataFrame, MultiIndex
import itertools
idx = pd.IndexSlice

sizeText=10
params = {'backend': 'wxAgg', 'lines.markersize' : 6,
          'axes.labelsize': sizeText, "mathtext.default":"regular",
          'text.fontsize': sizeText, 'axes.titlesize':sizeText, 'legend.fontsize': sizeText,
          'xtick.labelsize': sizeText, 'ytick.labelsize': sizeText}
plt.rcParams.update(params)


def delColLev(DataFrameIn, levels=[]):
    cols = DataFrameIn.columns.values
    cols = np.array(list(cols)).T
    # print cols, cols[0]
    counts = 0
    for level in range(len(cols)):
        if level not in levels:
            counts += 1
            if counts == 1:
                newCols = np.array([cols[level]])
            else:
                newCols = np.concatenate((newCols, [cols[level]]))
    DataFrameIn.columns = MultiIndex.from_arrays(newCols)
    return DataFrameIn


def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(100 * y))

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] == True:
        return s + r'$\%$'
    else:
        return s + '%'

def plotAll(dfs=[],level1="-",level2="-",level3="WP",level4="mean",title='Name',save2=os.getcwd() + "/Data/Plots/",inYear=' in 2012', showplot=False, savepng=True, savepdf=False, colors_set=rwth_main_colors, markers_set=wpg_markers, print_std=False, alphas=[]):

    colors=colors_set
    markerList=markers_set
    fig = plt.figure(figsize=(16./2.54, 8/2.54))
    fig.subplots_adjust(left=0.1)
    ax = fig.add_axes([0.09, 0.0, .89, .97])
    line_counter=0
    for index,df1 in enumerate(dfs):
        df1.sort_index(1, inplace=True)
        if level1!=[]:
            df1=df1.loc[idx[:],idx[:,level1,:,:]]
        if level2!=[]:
            df1=df1.loc[idx[:],idx[:,:,level2,:]]
        if level3!=[]:
            df1=df1.loc[idx[:],idx[:,:,:,level3]]
        if level4!=[]:
            df1error=df1.iloc[:,df1.columns.get_level_values(4)=="std"]
            df1=df1.iloc[:,df1.columns.get_level_values(4)==level4]

        if len(dfs)!=1:
            markerEdgeSizeList=np.ones(len(dfs))
            if alphas==[]: alphas=np.ones(len(dfs))
            line_counter+=1
            fbkF = {'edgecolor':colors[index], 'color':colors[index],'facecolor':colors[index]}
            no_markers=False
            if markerList==None:
                ax.plot(df1.index, df1[df1.columns.values[0]], color=colors[index], linewidth=1.0,label=df1.columns[0][0],marker=None,alpha=alphas[index])
            else:
                ax.plot(df1.index, df1[df1.columns.values[0]], color=colors[index], linewidth=1.0,label=df1.columns[0][0],marker=markerList[index],mew=markerEdgeSizeList[index],markevery=5,ms=7.,alpha=alphas[index])
            if print_std==True:
                ax.fill_between(df1.index, df1[df1.columns.values[0]]+df1error[df1error.columns.values[0]], df1[df1.columns.values[0]]-df1error[df1error.columns.values[0]],alpha=0.5,**fbkF)
        else:
            markerEdgeSizeList=np.ones(len(df1.columns.values))
            if alphas==[]: alphas=np.ones(len(df1.columns.values))
            for index_c,column in enumerate(df1.columns.values):
                fbkF = {'edgecolor':colors[index_c], 'color':colors[index_c],'facecolor':colors[index_c]}
                if level2=='-':
                    if markerList==[]:
                        ax.plot(df1.index, df1[df1.columns.values[index_c]], color=colors[index_c], linewidth=1.,label=df1.columns[index_c][1],marker=None,alpha=alphas[index_c])
                    else:
                        print(colors[index_c])
                        ax.plot(df1.index, df1[df1.columns.values[index_c]], color=colors[index_c], linewidth=1.,label=df1.columns[index_c][1],marker=markerList[index_c],mew=markerEdgeSizeList[index_c],markevery=5,ms=6.,alpha=alphas[index_c]) # bug: ,mec=colors[index_c]
                    if print_std==True:
                        ax.fill_between(df1.index, df1[df1.columns.values[index_c]]+df1error[df1error.columns.values[index_c]], df1[df1.columns.values[index_c]]-df1error[df1error.columns.values[index_c]],alpha=0.5*alphas[index_c],**fbkF)

                else:
                    if df1.columns[index_c][2] in roomnames_dict:
                        firstname= roomnames_dict[df1.columns[index_c][2]]
                    else: firstname=df1.columns[index_c][2]
                    label_conc=firstname+' '+df1.columns[index_c][3]
                    print(label_conc)
                    ax.plot(df1.index, df1[df1.columns.values[index_c]], color=colors[index_c], linewidth=1.,label=label_conc,marker=markerList[index],mew=markerEdgeSizeList[index_c],markevery=5,ms=6.) #bug: mec=colors[index_c]
                    if print_std==True:
                        ax.fill_between(df1.index, df1[df1.columns.values[index_c]]+df1error[df1error.columns.values[index_c]], df1[df1.columns.values[index_c]]-df1error[df1error.columns.values[index_c]],alpha=0.5*alphas[index_c],**fbkF)
                line_counter+=1

    ax.set_ylabel("Proportion of windows open"+inYear)
    ax.set_xlabel("Daily average outdoor temperature in $^\circ$C ")
    ax.yaxis.set_label_coords(-0.06, 0.48)
    plt.setp(ax.get_xticklabels())
    plt.setp(ax.get_yticklabels())
    ax.yaxis.grid(True)
    ax.xaxis.grid(False)
    ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='Gainsboro')
    ax.set_axisbelow(True)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ticks = ax.get_xticks()
    ax.set_ylim(0,1)
    ax.set_xlim(-15,30)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.3,box.width, box.height * 0.7])
    #ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 5))
    #ax.set_xticks(np.linspace(ticks[0], d.date2num(d.num2date(ticks[-1]) + dt.timedelta(hours=3)), 25), minor=True)

    if line_counter<=6:ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.21),frameon=False, ncol=3)
    elif line_counter<=8:ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.21),frameon=False, ncol=4)
    elif line_counter<=10:ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.21),frameon=False, ncol=5)
    else:ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.21),frameon=False, ncol=6)

    plt.text(0.5, 0.95,copyright+'RWTH AACHEN UNIVERSITY, generated with WinProGen, all right reserved',
             horizontalalignment='center', verticalalignment='center', transform = ax.transAxes,
             color=np.array([207., 209., 210.])/255, zorder=1)
    if savepdf==True:  plt.savefig(save2,figure=fig,  format='pdf')
    if savepng==True:  plt.savefig(save2,figure=fig,  format='png', transparent=False)
    if showplot==True: plt.show()

def plot_genpro(df,level0="B2E1",level1='A01',level2='Room_Bath',level3='WP1',savingFolder='',showplot=True, savepng=False, savepdf=False):
    font = {'family' : 'normal',
            'size'   : 10
            }


    print "Start progen plot..."

    level0=list(set(list(df.columns.levels[0])))
    level0=[a for a in level0 if a!='Weather' ][0]

    fig = plt.figure(figsize=(16. / 2.54, 8 / 2.54))
    ax = fig.add_axes([0.09, 0.0, 0.78, 0.92])
    ax2 = ax.twinx()
    ETR=['Weather', '-', '-', "AT Daily Average"]

    df.sort_index(1, inplace=True)

    match_timestamp = "12:00:00"
    ax2.plot(df.loc[df.index.strftime("%H:%M:%S") == match_timestamp, idx[ETR[0], ETR[1], ETR[2], ETR[3]]].index, df.loc[df.index.strftime("%H:%M:%S") == match_timestamp, idx[ETR[0], ETR[1], ETR[2], ETR[3]]], color= rwth_green ,alpha=0.2, linewidth=1,label='Daily average outdoor temperature')
    ax2.fill_between(df.loc[df.index.strftime("%H:%M:%S") == match_timestamp, idx[ETR[0], ETR[1], ETR[2], ETR[3]]].index, 0, df.loc[df.index.strftime("%H:%M:%S") == match_timestamp, idx[ETR[0], ETR[1], ETR[2], ETR[3]]], facecolor=rwth_maygreen,alpha=0.2, linewidth=0.01,label='_nolegend_')


    if level0!=None:
        df = df.loc[idx[:], idx[level0, :, :, :]]
    if level1!=None:
        df = df.loc[idx[:], idx[:, level1, :, :]]
    if level2!=None:
        df = df.loc[idx[:], idx[:, :, level2, :]]
    if level3!=None:
        df = df.loc[idx[:], idx[:, :, :, level3]]


    lab=level0+', '+level1+', '+level2+', '+level3[1]
    tit=level0+'_'+level1+'_'+level2+'_'+level3[1]
    lab=np.char.replace(lab,"AT Daily Average", 'DAT')

    plot_color=rwth_blue_50
    zorder_plot=10

    WSP=[level0, level1, level2, level3]

    ax.step(df.index, df.loc[idx[:], idx[WSP[0], WSP[1], WSP[2], WSP[3]]], color=plot_color, linewidth=1.0, label='_no_legend_', zorder=zorder_plot)
    ax.fill_between(df.index, df.loc[idx[:], idx[WSP[0], WSP[1], WSP[2], WSP[3]]], color=plot_color, linewidth=1.0, label=str(lab), zorder=zorder_plot, alpha=.5)

    # ax.xaxis.set_major_locator( HourLocator(np.arange(0,25,6)))
    # ax.xaxis.set_minor_locator( HourLocator(np.arange(0,25,1)))
    ax.xaxis.set_major_formatter( DateFormatter('%H:%M'))

    ax.set_ylim(0,1.2)
    ax2.set_ylim(-40,40)
    box = ax.get_position()
    if len(level0) > 3: plus_space=(len(level0)/2)*0.02
    else: plus_space=0
    ax.set_position([box.x0, box.y0 + box.height * 0.3 +plus_space,
                 box.width, box.height * 0.7 - plus_space])
    ax2.set_position([box.x0, box.y0 + box.height * 0.3 +plus_space,
                 box.width, box.height * 0.7 - plus_space])
    ax.legend(loc='upper center', bbox_to_anchor=(0.48, -0.2),frameon=False, ncol=2, prop=font)

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax2.yaxis.set_ticks_position('right')
    ax.xaxis.set_ticks_position('bottom')
    plt.setp(ax.get_xticklabels(),**font)
    plt.setp(ax.get_yticklabels(),**font)
    ax.set_ylabel("Window position", fontdict=font)
    ax.set_xlabel("Date and time", fontdict=font)
    ax.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")

    ax.yaxis.set_label_coords(-0.06, 0.43-plus_space)

    if savepng==True: plt.savefig(savingFolder,figure=fig,  format='png', transparent=False)
    if savepdf == True: plt.savefig(savingFolder,figure=fig,  format='pdf')
    if showplot==True: plt.show()

def plotDiurnal_RW(building="B2E1", level0=[],level1="Standard Diurnal",level2="B2E1",level3="A03",level4="Room_Sleeping",level5="WP1",savingFolder='',
                   set_temp_range='14 < AT Daily Average <= 18', color=rwth_maygreen, showplot=True, savepng=False, savepdf=False):

    if level1 == "Standard Diurnal":    diurnal_link = '_2012diurnals_MD.csv'
    else:  diurnal_link = '_2012_WWEdiurnals_MD.csv'

    if level1 == "Standard Diurnal":    diurnal_link = '_M1.csv'
    else:  diurnal_link = 'M2.csv'

    df = pd.read_csv(os.getcwd().split("\\properties")[0] + '/Data/diurnals/Diurnals_Original_data_' + building + diurnal_link, index_col=0, sep=';',header=[0, 1, 2, 4, 5, 6, 7], skiprows=[8, 9], parse_dates=True, low_memory=False)

    font = {'family' : 'normal',
            'size'   : 10
            }

    # checking for right color:
    t_ranges = list(set([a for a in df.columns.levels[0].values if a != "ATR"]))
    profile_type = list(set([a for a in df.columns.levels[1].values]))
    #print(profile_type)

    if level0=='all': level0=t_ranges
    #print(sorted(t_ranges, key=lambda t_ran: np.float(t_ran.split('<=')[1]) if '<=' in t_ran else np.float(t_ran.split('>')[1])))
    t_ranges = (sorted(t_ranges, key=lambda t_ran: np.float(t_ran.split('<=')[1]) if '<=' in t_ran else np.float(t_ran.split('>')[1])))
    cold_hot_color_dict = {t_range: rwth_cold_hot[index] for index, t_range in enumerate(t_ranges)}

    print "Start diurnal plot..."
    zorder_plot=0
    df.sort_index(1, inplace=True)
    level0=["ATR"]+level0

    if level0!=None:
        df = df.loc[idx[:], idx[level0, :, :, :, :, :, :]]
    if level1!=None:
        df = df.loc[idx[:], idx[:, level1, :, :, :, :, :]]
    # if level2!=None:
    #     df = df.loc[idx[:], idx[:, :, :, level2, :, :, :]]
    if level3!=None:
        df = df.loc[idx[:], idx[:, :, :, :, level3, :, :]]
    if level4!=None:
        df = df.loc[idx[:], idx[:, :, :, :, :, level4, :]]
    if level5!=None:
        df = df.loc[idx[:], idx[:, :, :, :, :, :, level5]]

    fig = plt.figure(figsize=(16./2.54, 8/2.54))
    ax = fig.add_axes([0.09, 0.0, .89, .92])

    for index,column in enumerate(df.columns.values):
        if column[0]=='ATR':
            zorder_plot=100
            plot_color=rwth_maygreen
        else:
            zorder_plot=3
            plot_color=cold_hot_color_dict[column[0]]
        lab=column[0]+', '+column[3]+', '+column[4]
        tit=column[3]+'_'+column[4]+'_'+column[0]
        if level1!="Standard Diurnal":
            print(tit, level1)
            tit+=level1
            lab=lab+' '+level1

        lab=np.char.replace(lab,"AT Daily Average", 'DAT')
        #lab = np.char.replace(lab, '<=', '$\leq$')

        print len(df.index),len(df[column])
        if level4 == 'Room_Kitchen': ax.plot(df.index, df[column], color=plot_color, linewidth=1.0,
                                         label=str(lab).split('Room Kitchen')[0]+', Kitchen', zorder=zorder_plot)
        if level4 == 'Room_Bath': ax.plot(df.index, df[column], color=plot_color, linewidth=1.0,
                                      label=str(lab).split('Room Bath')[0]+ 'Bath', zorder=zorder_plot)
        if level4 == 'Room_Sleeping': ax.plot(df.index, df[column], color=plot_color, linewidth=1.0,
                                          label=str(lab).split('Room Sleeping')[0]+', Bedroom', zorder=zorder_plot)
        if level4 == 'Room_Children': ax.plot(df.index, df[column], color=plot_color, linewidth=1.0,
                                          label=str(lab).split('Room Children')[0] +", Child's room", zorder=zorder_plot)
        if level4 == 'Room_Living': ax.plot(df.index, df[column], color=plot_color, linewidth=1.0,
                                        label=str(lab).split('Room Living')[0] +', Livingroom', zorder=zorder_plot)
        ax.fill_between(df.index, df[column], df[column]*0, facecolor=plot_color,alpha=0.2, linewidth=0.01,label='_nolegend_')


    ax.xaxis.set_major_locator( HourLocator(np.arange(0,25,6)))
    ax.xaxis.set_minor_locator( HourLocator(np.arange(0,25,1)))
    ax.xaxis.set_major_formatter( DateFormatter('%H:%M'))
    ax.set_xlim([df.index[0], df.index[-1]])

    ax.set_ylim(0,1)
    box = ax.get_position()
    if len(level0) > 3: plus_space=(len(level0)/2)*0.02
    else: plus_space=0
    ax.set_position([box.x0, box.y0 + box.height * 0.3 +plus_space,
                 box.width, box.height * 0.7 - plus_space])
    ax.legend(loc='upper center', bbox_to_anchor=(0.48, -0.2),frameon=False, ncol=2, prop=font)

    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    plt.setp(ax.get_xticklabels(),**font)
    plt.setp(ax.get_yticklabels(),**font)
    ax.set_ylabel("Probability for the window to be open", fontdict=font)
    ax.set_xlabel("Time of the day", fontdict=font)
    ax.yaxis.grid(True,zorder=0, color="Gainsboro", ls="-")
    tit=np.char.replace(tit,"=", '')
    tit=np.char.replace(tit,">", '')
    tit=np.char.replace(tit,"<", '')
    tit=np.char.replace(tit," ", '_')
    ax.yaxis.set_label_coords(-0.06, 0.43-plus_space)

    if savepng==True: plt.savefig(savingFolder,figure=fig,  format='png', transparent=False)
    if savepdf == True: plt.savefig(savingFolder,figure=fig,  format='pdf')
    if showplot==True: plt.show()

'''
TESTING OF CALCULATION METHODS


path='D:/git_repos/Python/WinProGen/Data/Position_on_AT/B2E1_PAT.csv'
path2='D:/git_repos/Python/WinProGen/Data/Position_on_AT/B2E2_PAT.csv'

dfAT=pd.read_csv(path, index_col=0, sep=';', header=[0,1,2,3,4],skiprows=[], low_memory=False)
dfAT2=pd.read_csv(path2, index_col=0, sep=';', header=[0,1,2,3,4],skiprows=[], low_memory=False)
dfAT=dfAT.iloc[:, dfAT.columns.get_level_values(0)!='Weather']
dfAT=dfAT.iloc[:, dfAT.columns.get_level_values(1)!='-']
dfAT=dfAT.iloc[:, dfAT.columns.get_level_values(2)!='-']
dfAT=dfAT.iloc[:, dfAT.columns.get_level_values(3)!='WP']
dfAT=dfAT.iloc[:, dfAT.columns.get_level_values(3)!='WP1+2']

dfAT2=dfAT2.iloc[:, dfAT2.columns.get_level_values(0)!='Weather']
dfAT2=dfAT2.iloc[:, dfAT2.columns.get_level_values(1)!='-']
dfAT2=dfAT2.iloc[:, dfAT2.columns.get_level_values(2)!='-']
dfAT2=dfAT2.iloc[:, dfAT2.columns.get_level_values(3)!='WP']
dfAT2=dfAT2.iloc[:, dfAT2.columns.get_level_values(3)!='WP1+2']

dataframes=[dfAT, dfAT2]
if len(dataframes)>1:
    for adf in dataframes:
        ### getting all columns except Ambient Temperature values
        adf_c0=list(set([a for a in adf.columns.levels[0].values if a!="Weather"]))
        adf_c1=list(set([a for a in adf.columns.levels[1].values if a!="-"]))
        adf_c2=list(set([a for a in adf.columns.levels[2].values if a!="-"]))
        adf_c3=list(set([a for a in adf.columns.levels[3].values if a!="AT"]))

        for ft in adf_c0:
            adf.sort(axis=1, inplace=True)
            adf[ft,'-','-','WP','mean']=adf.loc[idx[:],idx[ft,:,:,:,'mean']].mean(axis=1)
            #adfprov=adf.iloc[:, adf.columns.get_level_values(0)==ft]
            #adf[ft,'-','-','WP','mean']=adfprov.iloc[:, adfprov.columns.get_level_values(4)=='mean'].mean(axis=1)

plotAll(dfs=dataframes,level1="-",level2="-",level3="WP",level4="mean",title='Name',
        inYear=' in 2012', showplot=True, savepng=False, savepdf=False,
        colors_set=rwth_main_colors, markers_set=wpg_markers, print_std=True, alphas=[])
'''
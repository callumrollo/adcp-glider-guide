#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020-10-10

@author: Callum Rollo c.rollo@outlook.com
This script analyses snippet files from an AD2CP Seaglider
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob
import argparse
import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime,timedelta
plt.rcParams.update({'font.size': 16})


# pass the path to your adcp_tele files from the command line, defaults to working directory
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--working_directory", type=str)

args = parser.parse_args()
working_dir = args.working_directory

if not working_dir:
    print("no directory supplied, using current working directory:\n"+str(os.getcwd())+
          "\nspecify a working directory with: python tele_checker_mk2.py -p 'path/to/directory'")
    working_dir = os.getcwd()

# Or just hard code location of adcp_tele files here
# working_dir = 'example_data'

# Run the bash script to make neat files
return_stat = subprocess.run('bash tele_parser.sh', shell=True)

if return_stat.returncode !=0:
    print("uh-oh, shell script issues")
    exit(1)

# Make a sorted list of all the adcp_tele files
yos_list = glob.glob(working_dir+'/adcp_tele*.txt')
if not yos_list:
    sys.exit("no adcp_tele files found, exiting")
yos = np.sort(yos_list)

df_all = pd.DataFrame()

# Stats for each snippet file in multiple chunks
for yo_name in yos:
    df = pd.read_csv(yo_name, parse_dates=[['date', 'time']])
    df_all = pd.concat([df_all, df])

    # Divide the data into chunks of 180 records (12 samples of 15 cells) about 40 mins and plot the correlations.
    # Includes average return amplitudes
    
    chunks = np.arange(int(np.ceil(len(df['v1'])/180)))
    blobsize=400
    
    plt.close('all')
    
    for chunk in chunks:
        
        # Check for existing figures and do not remake them
        if Path(working_dir+'/tele_amp_'+yo_name[-8:-4]+'_'+str(chunk+1)+'.png').is_file():
            break
            
        df1 = df.loc[chunk*180:((chunk+1)*180)-1]
        fig,axs = plt.subplots(2,2,figsize=(22,10),sharex=True,sharey=True)
        fig.subplots_adjust(hspace = .05, wspace=.05)
        axs=axs.ravel()
        plot0 = axs[0].scatter(df1['cell_dist'],df1.date_time,c=df1['corr1'],vmin=0,vmax=100,s=blobsize,cmap='RdBu')
        axs[0].set(ylim=[df1.date_time.iloc[0]-timedelta(minutes=2),df1.date_time.iloc[-1]+timedelta(minutes=2)])
        axs[1].scatter(df1['cell_dist'],df1.date_time,c=df1['corr2'],vmin=0,vmax=100,s=blobsize,cmap='RdBu')
        axs[2].scatter(df1['cell_dist'],df1.date_time,c=df1['corr3'],vmin=0,vmax=100,s=blobsize,cmap='RdBu')
        axs[2].set(xlabel='distance from transducer (m)')
        axs[3].text(0.02,0.5,"Correlations for the three transducer heads. \nBlue color is good, expected out to 10-15 m",transform=axs[3].transAxes)
        fig.colorbar(plot0, ax=axs[3],label=r'correlation %',orientation='horizontal')
        axs[3].text(0.02,0.2,"Full range average amps {0:.1f}  {1:.1f}  {2:.1f} dB \nThree heads should be similar".format(df1['amp1'].mean(),df1['amp2'].mean(),df1['amp3'].mean()),transform=axs[3].transAxes)
        axs[3].text(0.02,0.9,'dive number {0} chunk number {1}'.format(yo_name[-8:-4],chunk+1),transform=axs[3].transAxes,color='r')
        plt.savefig(working_dir+'/tele_cor_'+yo_name[-8:-4]+'_'+str(chunk+1)+'.png')
        
        fig,axs = plt.subplots(2,2,figsize=(22,10),sharex=True,sharey=True)
        fig.subplots_adjust(hspace = .05, wspace=.05)
        axs=axs.ravel()
        plot0 = axs[0].scatter(df1['cell_dist'],df1.date_time,c=df1['amp1'],vmin=20,vmax=70,s=blobsize,cmap='viridis')
        axs[0].set(ylim=[df1.date_time.iloc[0]-timedelta(minutes=2),df1.date_time.iloc[-1]+timedelta(minutes=2)])
        axs[1].scatter(df1['cell_dist'],df1.date_time,c=df1['amp2'],vmin=20,vmax=70,s=blobsize,cmap='viridis')
        axs[2].scatter(df1['cell_dist'],df1.date_time,c=df1['amp3'],vmin=20,vmax=70,s=blobsize,cmap='viridis')
        axs[2].set(xlabel='distance from transducer (m)')
        axs[3].text(0.02,0.5,"Return amps for the three transducer heads. \nExpect to drop off rapidly",transform=axs[3].transAxes)
        fig.colorbar(plot0, ax=axs[3],label=r'return amp dB',orientation='horizontal')
        df_cell2 = df1.loc[df1['cell_no']==2]
        axs[3].text(0.02,0.2,"Full range average amps {0:.1f}  {1:.1f}  {2:.1f} dB \nCell 2 (3.3 m) average amps {3:.1f}  {4:.1f}  {5:.1f} dB \nThree heads should be similar".format(df1['amp1'].mean(),df1['amp2'].mean(),df1['amp3'].mean(),df_cell2['amp1'].mean(),df_cell2['amp2'].mean(),df_cell2['amp3'].mean()),transform=axs[3].transAxes)
        axs[3].text(0.02,0.9,'dive number {0} chunk number {1}'.format(yo_name[-8:-4],chunk+1),transform=axs[3].transAxes,color='r')
        plt.savefig(working_dir+'/tele_amp_'+yo_name[-8:-4]+'_'+str(chunk+1))

# Stats for all collected snippets

df1 = df_all.groupby('cell_no').mean()
df_cell2 = df1.loc[df1.index==2]
fig,axs = plt.subplots(figsize=(12,8),sharex=True,sharey=True)
fig.subplots_adjust(hspace = .05, wspace=.05)
plot0 = axs.scatter(df1['cell_dist'],np.ones(len(df1.v1)),c=df1['corr1'],vmin=0,vmax=100,s=blobsize,cmap='RdBu')
axs.scatter(df1['cell_dist'],2*np.ones(len(df1.v1)),c=df1['corr2'],vmin=0,vmax=100,s=blobsize,cmap='RdBu')
axs.scatter(df1['cell_dist'],3*np.ones(len(df1.v1)),c=df1['corr3'],vmin=0,vmax=100,s=blobsize,cmap='RdBu')
axs.set(xlabel='distance from transducer (m)')
axs.text(0.02,0.6,"Correlations for the three transducer heads. \nBlue color is good, expected out to 10-15 m",transform=axs.transAxes)
fig.colorbar(plot0, ax=axs,label=r'correlation %',orientation='horizontal')
axs.text(0.02,0.2,"Full range average correlation {0:.1f}  {1:.1f}  {2:.1f} % \nThree heads should be similar".format(df1['corr1'].mean(),df1['corr2'].mean(),df1['corr3'].mean()),transform=axs.transAxes)
axs.text(0.02,0.8,'Mean of all snippets',transform=axs.transAxes,color='r')
axs.set(yticks=[1,2,3], yticklabels=['beam 1', 'beam 2', 'beam3'])
plt.savefig(working_dir+'/mean_tele_cor')

fig,axs = plt.subplots(figsize=(12,8),sharex=True,sharey=True)
fig.subplots_adjust(hspace = .05, wspace=.05)
plot0 = axs.scatter(df1['cell_dist'],np.ones(len(df1.v1)),c=df1['amp1'],vmin=20,vmax=70,s=blobsize,cmap='viridis')
axs.scatter(df1['cell_dist'],2*np.ones(len(df1.v1)),c=df1['amp2'],vmin=20,vmax=70,s=blobsize,cmap='viridis')
axs.scatter(df1['cell_dist'],3*np.ones(len(df1.v1)),c=df1['amp3'],vmin=20,vmax=70,s=blobsize,cmap='viridis')
axs.set(xlabel='distance from transducer (m)')
axs.text(0.02,0.6,"Return amps for the three transducer heads. \nExpect to drop off rapidly",transform=axs.transAxes)
fig.colorbar(plot0, ax=axs,label=r'correlation %',orientation='horizontal')
axs.text(0.02,0.2,"Full range average amps {0:.1f}  {1:.1f}  {2:.1f} dB \nCell 2 (3.3 m) average amps {3:.1f}  {4:.1f}  {5:.1f} dB \nThree heads should be similar".format(df1['amp1'].mean(),df1['amp2'].mean(),df1['amp3'].mean(),df_cell2['amp1'].mean(),df_cell2['amp2'].mean(),df_cell2['amp3'].mean()),transform=axs.transAxes)
axs.text(0.02,0.8,'Mean of all snippets',transform=axs.transAxes,color='r')
axs.set(yticks=[1,2,3], yticklabels=['beam 1', 'beam 2', 'beam3'])
plt.savefig(working_dir+'/mean_tele_amp')

plt.close("all")

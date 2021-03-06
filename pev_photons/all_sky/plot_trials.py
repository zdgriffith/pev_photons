#!/usr/bin/env/python

########################################################################
# Plot background TS ensemble with observed TS
# for the hottest spot in the all sky scan.
########################################################################

import argparse
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

from pev_photons import utils

if __name__ == "__main__":
    p = argparse.ArgumentParser(
            description='plot scrambled trials',
            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--bin_width', type=float, default=0.5,
                   help='width of bin in TS space')
    p.add_argument('--use_original_trials', action='store_true', default=False,
                   help='Use the original background trials rather those you generated on your own.')
    args = p.parse_args()

    plt.style.use(utils.plot_style)
    colors = plt.rcParams['axes.color_cycle']

    hotspot = np.load(utils.prefix+'all_sky/hotspot.npy')['TS'][0]

    if args.use_original_trials:
        job_list = glob('/data/user/zgriffith/pev_photons/all_sky/all_sky_trials/full_*.npy')
    else:
        job_list = glob(utils.prefix+'all_sky/all_sky_trials/full_*.npy')

    bg_trials = []
    for job in job_list:
        job_ts = np.load(job)
        if not np.any(np.equal(job_ts,0)):
            bg_trials.extend(job_ts)

    Ntrials = float(len(bg_trials))

    plt.hist(bg_trials, bins=np.arange(0,100,args.bin_width),
             label='Background Trials', histtype='stepfilled',
             edgecolor='none', color='grey')

    #Plot the observed TS
    plt.axvline(x=hotspot, color=colors[2],
                label='Observed', lw=3)

    p_value = np.sum(np.greater(bg_trials, hotspot))/Ntrials
    print("p-value: %.4f" % p_value)

    plt.axvline(x=np.percentile(bg_trials,68), label='1 $\sigma$',
                ls='--', color='k')
    plt.axvline(x=np.percentile(bg_trials,95), label='2 $\sigma$',
                ls='-.', color='k')
    plt.axvline(x=np.percentile(bg_trials,99.7), label='3 $\sigma$',
                ls=':', color='k')

    plt.xlabel('Test Statistic')
    plt.ylabel('Trials')
    plt.yscale('log')
    l = plt.legend(loc=0)
    utils.plot_setter(plt.gca(), l)
    plt.xlim([0,50])
    plt.ylim([0.5,Ntrials])
    plt.tight_layout()
    plt.savefig(utils.fig_dir+'all_sky/all_sky_trials.png')
    plt.savefig(utils.fig_dir+'paper/all_sky_trials.pdf')
    plt.close()

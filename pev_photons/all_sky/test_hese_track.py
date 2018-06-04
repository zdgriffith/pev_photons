#!/usr/bin/env python

########################################################################
# Test the position of the HESE track
########################################################################

import argparse
import numpy as np
import healpy as hp
import pandas as pd

from pev_photons.utils.load_datasets import load_dataset
from pev_photons.utils.support import prefix, resource_dir

def bg_trials(ps_llh, ra, dec, n_trials=10):
    ps_llh.capscramble = True

    trials = ps_llh.do_trials(n_trials, src_ra=ra,
                              src_dec=dec)

    np.save(prefix+'all_sky/hese_track_trials.npy',
             trials['TS'])


def test_source(ps_llh, ra, dec):
    source = np.empty((1,),
                      dtype=[('ra', np.float), ('dec', np.float),
                             ('TS', np.float), ('nsources', np.float),
                             ('gamma', np.float)])

    fit = ps_llh.fit_source(ra, dec, scramble=False)

    source['ra'] = np.degrees(ra)
    source['dec'] = np.degrees(dec)
    source['TS'] = fit[0]
    source['nsources'] = fit[1]['nsources']
    source['gamma'] = fit[1]['gamma']

    pairs = [source.dtype.names[i]+': %0.2f' % val for i, val in enumerate(source[0])]
    for pair in pairs:
        print(pair)
    np.save(prefix+'all_sky/hese_track.npy', source)


if __name__ == "__main__":
    p = argparse.ArgumentParser(
            description='Test source',
            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--ncpu", type=int, default=1,
                    help="Number of cores to run on.")
    p.add_argument("--seed", type=int, default=1,
                   help='rng seed')
    p.add_argument("--n_trials", type=int, default=100,
                   help='Number of trials')
    args = p.parse_args()

    events = pd.read_hdf(resource_dir+'HESE.hdf5')
    events = events[~events['is_cascade']]
    ra = np.radians(events['ra'].values[0])
    dec = np.radians(events['dec'].values[0])

    ps_llh = load_dataset('point_source', ncpu=args.ncpu, seed=args.seed)
    if args.n_trials is not None:
        test_source(ps_llh, ra, dec, n_trials=args.n_trials)
    else:
        bg_trials(ps_llh, ra, dec)

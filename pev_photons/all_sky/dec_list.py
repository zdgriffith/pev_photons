#!/usr/bin/env python

########################################################################
# Create an array of unique declination values for a given Nside
########################################################################

import argparse
import numpy as np

import healpy as hp

from pev_photons import utils

if __name__ == "__main__":
    p = argparse.ArgumentParser(
            description='Create an array of unique declination values.',
            formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--nside", type=int, default=512,
                   help='nside of skymap')
    p.add_argument('--outFile', type=str,
                   default='all_sky/dec_values_512.npz',
                   help='The output file name.')
    args = p.parse_args()

    npix = hp.nside2npix(args.nside)
    pix = np.arange(npix)
    theta, phi = hp.pix2ang(args.nside, pix)
    dec_list = np.pi/2. - theta
    unique_decs = np.unique(dec_list)
    mask = (np.sin(unique_decs) < -0.8) & (np.degrees(unique_decs) > -85.)

    pix_list = []
    for dec in unique_decs[mask]:
        pix_list.append(pix[np.equal(dec_list,dec)])

    np.savez(utils.prefix+args.outFile,
             pix_list=pix_list,
             decs=unique_decs[mask])

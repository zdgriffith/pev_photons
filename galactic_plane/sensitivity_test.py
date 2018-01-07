#!/usr/bin/env python

########################################################################
# Test the sensitivity to a galactic plane flux template. 
########################################################################

import argparse as ap
import numpy as np

from skylab.sensitivity_utils import estimate_sensitivity
from skylab.template_injector import TemplateInjector

from pev_photons.load_datasets import load_gp_dataset
from pev_photons.support import get_fig_dir()

def mu2flux(inj, args):

    print('dN/dE = %s' % inj.mu2flux(args.mu))
    conv = (args.Enorm**2)*inj.mu2flux(args.mu)
    print('E^2dN/dE = %s' % conv)

if __name__ == "__main__":
    p = ap.ArgumentParser(description='Test galactic plane sensitivity.',
                          formatter_class=ap.RawDescriptionHelpFormatter)
    p.add_argument('--name', type=str, default='fermi_pi0',
                   help='The name of the template.')
    p.add_argument("--alpha", type=float, default=3.0,
                   help='Spectral index of signal.')
    p.add_argument("--Enorm", type=float, default=2*10**6,
                   help='normalization energy in GeV')
    p.add_argument("--mu", type=float, default=0.,
                   help='number of signal events')
    p.add_argument("--ncpu", type=int, default=1,
                    help="Number of cores to run on.")
    p.add_argument("--seed", type=int, default=1,
                   help='rng seed')
    args = p.parse_args()

    template_llh = load_gp_dataset(args)

    inj = TemplateInjector(template=template_llh.template,
                           gamma=args.alpha,
                           E0=args.Enorm,
                           Ecut=None,
                           seed=1)
    inj.fill(template_llh.exp, template_llh.mc, template_llh.livetime)

    if args.mu:
        mu2flux(inj, args)

    #Directory where plots will go
    path = (get_fig_dir()+args.name+'/')

    results = estimate_sensitivity(template_llh, inj,
                                   nstep=11, 
                                   ni_bounds=[0,2000], 
                                   nsample=100, 
                                   path=path)

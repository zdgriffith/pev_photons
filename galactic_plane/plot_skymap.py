#!/usr/bin/env python

########################################################################
# Plot a skymap projected with the South Pole at the center.
########################################################################

import argparse as ap
import healpy as hp
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, LogNorm
from matplotlib import cm

import sky
from mpl_toolkits.basemap import Basemap
from support_functions import get_fig_dir
from colormaps import cmaps

if __name__ == "__main__":
    p = ap.ArgumentParser(
            description='Plot a skymap with a south polar projection.',
            formatter_class=ap.RawDescriptionHelpFormatter)
    p.add_argument('--prefix', type = str,
                   default='/data/user/zgriffith/pev_photons/',
                   help='Base directory for file storing.')
    p.add_argument('--mapName', type = str,
                   default='fermi_pi0',
                   help='Name of the skymap to plot.')
    p.add_argument('--noPlane', action='store_true', default=False,
                   help='If True, do not draw galactic plane.')
    p.add_argument('--noGrid', action='store_true', default=False,
                   help='If True, do not draw grid lines.')
    args = p.parse_args()

    filename = args.prefix+'/galactic_plane/source_templates/'+args.mapName+'.npy'
    m = np.load(filename)
    m = hp.ud_grade(m,nside_out=512)
    nside = hp.npix2nside(len(m))
    npix  = hp.nside2npix(nside)
    DEC, RA = hp.pix2ang(nside, range(len(m)))

    #Conversion from galactic coords if needed
    DEC, RA = hp.Rotator(coord = ['G','C'], rot = [0, 0])(DEC, RA)

    f = plt.figure(num=1, figsize=(12,8))
    f.clf()
    ax=f.add_subplot(1,1,1,axisbg='white')
 
    # Define projection to be from the South Pole.
    map1=Basemap(projection='spstere',boundinglat=-50,lon_0=0)

    # Draw the grid lines and labels.
    print(max(m))
    if not args.noGrid:
        map1.drawmeridians(np.arange(0,360,15), linewidth=1,
                           labels=[1,0,0,1], labelstyle='+/-',
                           fontsize=16)
        map1.drawparallels(np.arange(-90,-45,5), linewidth=1,
                           labels=[0,0,0,0], labelstyle='+/-',
                           fontsize=16)

        x,y = map1(45,-80)
        plt.text(x, y, '-80$\degree$', fontsize=16)
        x,y = map1(45,-70)
        plt.text(x, y, '-70$\degree$', fontsize=16)
        x,y = map1(45,-60)
        plt.text(x, y, '-60$\degree$', fontsize=16)
        x,y = map1(45,-50)
        plt.text(x, y, '-50$\degree$', fontsize=16)

    # Draw the galactic plane.
    if not args.noPlane:
        tl = np.arange(-120,0,0.01)
        tb = np.zeros(np.size(tl))
        (tra,tdec) = sky.gal2eq(tl, tb)
        x,y = map1(tra, tdec)
        sc  = map1.plot(x, y, 'k--', linewidth=1, label='Galactic Plane')

        tb = 5*np.ones(np.size(tl))
        (tra,tdec) = sky.gal2eq(tl, tb)
        x,y = map1(tra, tdec)
        sc  = map1.plot(x, y, 'k-', linewidth=1)

        tb = -5*np.ones(np.size(tl))
        (tra,tdec) = sky.gal2eq(tl, tb)
        x,y = map1(tra, tdec)
        sc  = map1.plot(x, y, 'k-', linewidth=1)

    # Draw the map.
    x,y = map1(np.degrees(RA), 90-np.degrees(DEC))
    sc  = map1.scatter(x, y,
                       c=len(m)*m/np.sum(m),
                       norm=LogNorm(vmin=10**-3, vmax = 100),
                       cmap= cmaps['plasma'],
                       s=2**8, lw=0, zorder=0)
    clb = f.colorbar(sc, orientation='vertical')
    clb.set_label('Magnitude [A.U.]', fontsize=20)
    
    plt.legend()
    plt.savefig(get_fig_dir()+args.mapName+'.png',
                facecolor='none', dpi=300,
                bbox_inches='tight') 
    plt.close()
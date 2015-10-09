import numpy as np
import matplotlib.pylab as plt
import os
import time
import glob
import multiprocessing
from matplotlib import rcParams

sz = 60
rcParams['axes.labelsize'] = sz
rcParams['xtick.labelsize'] = sz
rcParams['ytick.labelsize'] = sz
rcParams['legend.fontsize'] = sz
rcParams['axes.titlesize'] = sz
rcParams['font.size'] = sz
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']

rcParams['xtick.major.size'] = 20
rcParams['xtick.major.width'] = 4
rcParams['ytick.major.size'] = 20
rcParams['ytick.major.width'] = 4
#rcParams['text.usetex'] = True

#ax.spines["right"].set_visible(False)
#ax.spines["top"].set_visible(False)
#ax.spines["left"].set_linewidth(2)
#ax.spines["bottom"].set_linewidth(2)
#
#ax.yaxis.set_ticks_position('left')
#ax.xaxis.set_ticks_position('bottom')
#xticks = ax.xaxis.get_major_ticks()
#xticks[0].tick1On = False
#xticks[-1].tick1On = False
#fig.tight_layout(pad=0.1)

from getSpacingandPhase import fitInterference, getPeaks

def n(l):
    #http://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson
    # assume l in nm, must convert to um
    l *=1e-3
    A = (0.6961663*l**2)/(l**2 - 0.0684043**2)
    B = (0.4079426*l**2)/(l**2-0.1162414**2)
    C = (0.8974794*l**2)/(l**2-9.896161**2)
    return np.sqrt(A+B+C+1)

def nair(l):
    # http://refractiveindex.info/?shelf=other&book=air&page=Ciddor
    # assume l in nm, must convert to um
    l *=1e-3
    A = (0.05792105*l**2)/(238.0185-l**2)
    B = (0.00167917*l**2)/(57.362-l**2)
    return A+B+1


def g(l, alph):
    return np.sqrt(n(l)**2 - np.sin(alph)**2)

def h(l, alph, eps):
    return np.sqrt( 1 -
            ((1-2*eps**2)*np.sin(alph) - 2 * g(l, alph)* eps)**2
        )

def invT(l, alph, eps):
    G = g(l, alph)
    H = h(l, alph, eps)
    t = 2 * H * np.tan(eps) * (np.sin(alph)-G * eps)
    b = G * H * np.tan(alph) - G * np.sin(alph) + 2 * eps * (G**2 - np.sin(alph)**2)
    return t/b

def dpda(l, alph, eps, th=None):
    if th is None:
        th = invT(l, alph, eps)
    G = g(l, alph)
    H = h(l, alph, eps)
    Nair = nair(l)
    o = 2 * Nair  * n(l)**2 * (1-eps**2) * np.cos(th) * np.tan(eps) / G
    ta = 2 * n(l)**2 * eps * (np.sin(alph) - 2 * G * eps)/ (G * H)
    tb = 1./H - 1./np.cos(alph)
    t = (ta + tb) * Nair * np.sin(th)
    return o+t

def e(l, alph, eps, a, e0):
    return e0 + a * np.cos(np.arctan(invT(l, alph, eps)))*np.tan(eps)


def S(l, alph, eps, a, S0):
    return S0 + a * np.sin(np.arctan(invT(l, alph, eps)))

def l12(l, alph, eps, a, S0, e0):
    G = g(l, alph)
    H = h(l, alph, eps)
    Nair = nair(l)
    Nir = n(l)
    Sa = S(l, alph, eps, a, S0)
    ea = e(l, alph, eps, a, e0)

    o = ea* 2 * Nir * (1-eps**2)/G
    t = Sa * 2 * Nir * eps * (np.sin(alph)-2 * G * eps)/(G*H)
    return o+t

def l34(l, alph, eps, a, S0, e0):
    G = g(l, alph)
    H = h(l, alph, eps)
    Nair = nair(l)
    Nir = n(l)
    Sa = S(l, alph, eps, a, S0)
    ea = e(l, alph, eps, a, e0)

    return Sa * (1./H - 1./np.cos(alph))

def m(l, alph, eps, a, S0, e0):
    G = g(l, alph)
    H = h(l, alph, eps)
    Nair = nair(l)
    Nir = n(l)
    Sa = S(l, alph, eps, a, S0)
    ea = e(l, alph, eps, a, e0)

    o = 2 * ea * (eps*G-np.sin(alph))/G

    tt = G*H * np.tan(alph) - G*(1-8*eps**2)*np.sin(alph) + 2*eps*(G**2-np.sin(alph)**2)

    return o + Sa*tt/(G*H)

def l5(l, alph, eps, a, S0, e0):
    return m(l, alph, eps, a, S0, e0)*np.sin(alph)



def p(l, alph=None, eps=None, a=None, S0=None, e0=None):
    if alph is None and len(l)>0:
        l, alph, eps, a, S0, e0 = l

    G = g(l, alph)
    H = h(l, alph, eps)
    Nair = nair(l)
    Nir = n(l)

    return Nair * (
            Nir*l12(l, alph, eps, a, S0, e0) + l34(l, alph, eps, a, S0, e0) + l5(l, alph, eps, a, S0, e0)
        )

def getWavelength(data, debugging=True):
        spacing, phase = fitInterference(data)
        if spacing<0:
            print "Bad spacing value!"
            return

        lEst0 = spacing * dpda(750, alph, eps)
        if debugging:
            print "\tInitial estimate:", lEst0

        lEst1 = spacing * dpda(lEst0, alph, eps)
        if debugging:
            print "\tSecondary estimate:", lEst1

        p0 = p(lEst1, alph, eps, 0, S0, e0)
        totalPhase = p0/lEst1 + phase

        if debugging:
            print "\tTotal phase:", totalPhase
        lEst2 = p0/(totalPhase - 0.5)
        if debugging:
            print "\tNext estimate:", lEst2



        lEst3 = spacing * dpda(lEst2, alph, eps)
        if debugging:
            print "\tInitial estimate:", lEst3

        lEst4 = spacing * dpda(lEst3, alph, eps)
        if debugging:
            print "\tSecondary estimate:", lEst4

        p0 = p(lEst4, alph, eps, 0, S0, e0)
        totalPhase = p0/lEst4 + phase
        
        if debugging:
            print "\tTotal phase:", totalPhase
        lEst5 = p0/(totalPhase - 0.5)
        if debugging:
            print "\tNext estimate:", lEst5

        return lEst5


if __name__ == '__main__':
    path = r'Z:\Darren\Data\2015\10-6 Wavemeter forms'

    blanklist = glob.glob(os.path.join(path, 'blank*.txt'))
    list461 = glob.glob(os.path.join(path, '460*.txt'))
    list632 = glob.glob(os.path.join(path, '632*.txt'))
    list671 = glob.glob(os.path.join(path, '670*.txt'))
    list689 = glob.glob(os.path.join(path, '689*.txt'))

    data = np.loadtxt(list632[0])


    alph = 45.147591956 * np.pi/180
    eps = 0.0239329726129 * np.pi/180
    e0 = 1.0e6
    S0 = 1.90e8

    l = []
    for f in list632:
        data = np.loadtxt(f)
        l.append(getWavelength(data, debugging=True))

    print np.std(l)





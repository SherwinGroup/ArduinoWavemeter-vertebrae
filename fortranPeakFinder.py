import numpy as np
import matplotlib.pylab as plt
import os
import glob
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

from getSpacingandPhase import fitInterference
from getSpacingandPhase import getPeaks as qdPeaks

def shaper(x, *p):
    f, mu, sig = p
    return (1+np.cos(x * 2* np.pi/f)) * np.exp(-(x-mu)**2/sig**2)

def sym(data, filter, z, x, n, polar):
    n1 = 1
    n4 = int(filter + 0.5)
    n2 = ((n4 + 1)/2)
    n3 = ((n4 + 2)/2)
    alldiff = []
    idif = 0
    alldiff.append(idif)
    for i in range(n1, n2):
        j = n3 + i - 1
        idif = idif + data[i] - data[j]
        alldiff.append(idif)
    n2 += 1 
    n4 += 1
    n = 0
    lstdif = idif
    for i in range(n4, len(data)):
        idif = idif - data[n1] + data[n2] +data[n3] - data[i]
        alldiff.append(idif)
        if (lstdif>0 and idif > 0) or (lstdif<=0 and idif <= 0):
            pass
        else:
            if n==0:
                polar = lstdif - idif
            n+=1
            x[0].append(n)
            z[0].append(
                    (n2+n3-1.)/2. + float(lstdif)/(lstdif-idif)
                )
        n1 += 1
        n2 += 1
        n3 += 1
        lstdif = idif
    return alldiff

def getPeaks(data, f=None, cutoff = -0.2):
    if f is None:
        f = 39.7870067478
    if len(data.shape) == 2:
        pixels = data[:,0]
        data = data[:,1]
    else:
        pixels = np.arange(len(data))
        pixels = np.polyval(
            [-5.06648862e-9,  1.834188e-5, 1, 0 ],
            # [-5.04124959e-9,  1.8279078e-5, 1, 0 ],
            pixels)

    if cutoff<0:
        cutoff = -cutoff * np.max(data)
    # else:
        # print "f:",f

    b = 0.742 * f/2
    symfilt = [0]*0 + [-1] * (int(b)) + [1] * (int(b))

    # plt.plot(symfilt*100)
    conv = np.convolve(data, symfilt, mode='same')[2:]
    # plt.figure()
    # plt.plot(data/max(data), label = 'raw', linewidth=3)
    # plt.plot(conv/max(conv), label = 'convolution', linewidth=3)
    # plt.legend(loc='best')
    # plt.xlabel('Pixels')
    # plt.show()

    # find negative crossings
    pos = conv > 0
    npos = ~pos
    pcrosses = np.logical_or(pos[1:], npos[:-1])
    # plt.plot([int(i) for i in pcrosses])

    # plt.plot(np.argwhere(~pcrosses), [0] * len(np.argwhere(~pcrosses)), 'b^', markersize=20)

    # find positive crossings
    neg = conv < 0
    nneg = ~neg
    ncrosses = np.logical_or(neg[1:], nneg[:-1])
    # plt.plot([int(i) for i in ncrosses])

    # plt.plot(np.argwhere(~ncrosses), [0] * len(np.argwhere(~ncrosses)), 'gv', markersize=20)

    # put them together
    crosses = np.logical_or(~pcrosses, ~ncrosses)

    # find their index, and shift by two 
    crs = np.argwhere(crosses)+1
    # plt.plot(crs, [0] * len(crs), 'rx', markersize=20)
    # plt.ylim(-1, 1)

    interp = [vv + (pixels[ii]-pixels[ii-1])*float(conv[ii-1])/ (conv[ii-1] - conv[ii]) for ii, vv in zip(crs[2:], pixels[crs[2:]])
        if data[ii]>cutoff]
    return np.array(interp).T[0]

def fitSpacingAndPhase(data, f, firstPeak = None, cutoff = -.2, smooth = False, debugging = False):
    extrema = getPeaks(data, f)
    if firstPeak is None:
        firstPeak = 0

    stIdx = np.argwhere(extrema>firstPeak)[0]
    if debugging:
        print "extrema:", extrema
        print "going to start at idx: {}, value: {}, corresponding to peak: {}".format(
            stIdx, extrema[stIdx], firstPeak)
    # extrema = extrema[stIdx:]
    extrema = extrema[stIdx::]
    # calibration factor for relinearizations, rescale by a cubic
    # extrema = np.polyval([-1.10956145e-9, -0.84978583e-5, 1, 0], extrema)
    # extrema = np.polyval([ 2.5688809e-9 ,  0.41668376e-5, 1, 0], extrema)

    peakNum = np.arange(0, 500, 1.0)[:len(extrema)*1:1]
    if debugging:
        print "extrema, peannum"
        print extrema, peakNum
        print "and shapes"
        print extrema.shape, peakNum.shape
    p = np.polyfit(peakNum, extrema, deg=1)
    startingPeakNum = int(min(extrema)/p[0])+1
    peakNum += startingPeakNum
    p = np.polyfit(peakNum, extrema, deg=1)

    if debugging:
        plt.figure('Fit')
        plt.plot(peakNum, extrema, '^-')
        plt.plot([0, peakNum[-1]], np.polyval(p, [0, peakNum[-1]] ), linewidth=2)
        # plt.show()

    # return the interference spacing, in nm
    # and the relative intercept
    return p[0]*14e3, -p[1]/p[0]



def fullGetSpacingAndPhase(data, f=None, firstPeak = None, cutoff = -.2, smooth = False, debugging = False):
    data = np.array(data-min(data))
    if f is None:
        f = fitInterference(data, cutoff=cutoff, smooth = smooth, debugging = debugging)[0]/14e3

    if f<0:
        return -1, -1
    if debugging:
        print "freq:",f
    if firstPeak is None:
        firstPeak = qdPeaks(data, cutoff=cutoff, smooth = smooth, debugging = False)[1]

    f = fitSpacingAndPhase(data, f, firstPeak = firstPeak, debugging = debugging)[0]/14e3

    return fitSpacingAndPhase(data, f, firstPeak = firstPeak, debugging = debugging)





if __name__ == '__main__':
    x = np.arange(1024)
    f = 33.456
    data = shaper(x, f, 400., 600.)

    path = r'Z:\Darren\Data\2015\10-6 Wavemeter forms'
    data = np.loadtxt(glob.glob(os.path.join(path, '460*.txt'))[0])
    data -= min(data)
    f = 37
    try:
        fullGetSpacingAndPhase(data, debugging = True)
    except:
        plt.show()
        raise



import numpy as np
import matplotlib.pylab as plt
import os
import glob
from matplotlib import rcParams
from hsganalysis.newhsganalysis import fft_filter
import warnings

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


def group_data(data):
    """
    Given a list of numbers, group them up based on where
    they're continuous
    """
    cutoff = 7 # gap between data sets
    groupedData = []
    curData = []
    for d in list(data):
        if curData:
            if np.abs(d-curData[-1])>cutoff:
                groupedData.append(curData)
                curData = [d]
            else:
                curData.append(d)
        else:
            curData.append(d)
    groupedData.append(curData)
    return groupedData



def fitInterference(data, cutoff = -.2, smooth = True, debugging = False):
    if smooth:
        # running average
        data = (np.cumsum(data)[2:] - np.cumsum(data)[:-2])/2
    data -= min(data)
    if cutoff < 0:
        cutoff = abs(cutoff) * max(data)
    if debugging:
        plt.plot(data)

    idxs = np.argwhere(data>cutoff)

    # weird issue with it returning a nx1, but I just want 1d
    idxs = idxs.reshape(len(idxs))

    # separate them by separation
    groupedIdxs = group_data(idxs)

    maxPositions = []
    firstObservedPeakPos = np.inf
    for group in groupedIdxs:
        # skip if the figure isn't there
        if not group:
            continue
        # plot the cutoff group for debugging
        if debugging:
            plt.plot(group, data[group], linewidth=5)

        # catch warnings to prevent weird behavior later
        # (and flooding the console)
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                p = np.polyfit(group, data[group], deg=2)

            except np.RankWarning:
                continue
            except RuntimeWarning:
                continue
        # positive concavity, not a correct fit
        if p[0]>0:
            continue
        # peaks fit is too broad to be real, skip it
        if np.abs(np.sqrt(p[1]**2-4*p[0]*p[2])/p[0])>100:
            continue
        # plot the fits for debugging
        if debugging:
            plt.plot(range(len(data)), np.polyval(p, range(len(data))))
        # valid peak found, add it to the list
        maxPositions.append(-p[1]/(2*p[0]))
        # get the first peak
        if np.mean(group)<firstObservedPeakPos:
            firstObservedPeakPos = maxPositions[-1]
    if not maxPositions:
        print "Error! Exposure is too low! Can't calibrate!"
        return -1, -1

    if debugging:
        print np.diff(maxPositions)
        print [np.abs(range(len(data))-ii).argmin() for ii in maxPositions]
        maxHeights = data[[np.abs(range(len(data))-ii).argmin() for ii in maxPositions]]
        plt.plot(maxPositions, maxHeights, 'o', markersize=20)
        plt.ylim(0, max(data))

    startPos = int(firstObservedPeakPos/np.mean(np.diff(maxPositions)))
    p = np.polyfit(range(startPos, startPos + len(maxPositions)), maxPositions, deg=1)
    if debugging:
        plt. figure()
        plt.plot(range(startPos, startPos + len(maxPositions)), maxPositions, 'o-')
        plt.plot([0, startPos + len(maxPositions)], 
            np.polyval(p, [0, startPos + len(maxPositions)]))

    if debugging:
        plt.show()

    # return the interference spacing, in nm
    # and the relative intercept
    return p[0]*14e3, p[1]/p[0]



def getPeaks(data, cutoff = -.2, smooth = True, debugging = False):
    if smooth:
        # running average
        data = (np.cumsum(data)[2:] - np.cumsum(data)[:-2])/2
    data -= min(data)
    if cutoff < 0:
        cutoff = abs(cutoff) * max(data)
    if debugging:
        plt.plot(data)

    idxs = np.argwhere(data>cutoff)

    # weird issue with it returning a nx1, but I just want 1d
    idxs = idxs.reshape(len(idxs))

    # separate them by separation
    groupedIdxs = group_data(idxs)

    maxPositions = []
    firstObservedPeakPos = np.inf
    for group in groupedIdxs:
        # skip if the figure isn't there
        if not group:
            continue
        # plot the cutoff group for debugging
        if debugging:
            plt.plot(group, data[group], linewidth=5)

        # catch warnings to prevent weird behavior later
        # (and flooding the console)
        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            try:
                p = np.polyfit(group, data[group], deg=2)

            except np.RankWarning:
                continue
            except RuntimeWarning:
                continue
        # positive concavity, not a correct fit
        if p[0]>0:
            continue
        # peaks fit is too broad to be real, skip it
        if np.abs(np.sqrt(p[1]**2-4*p[0]*p[2])/p[0])>100:
            continue
        # plot the fits for debugging
        if debugging:
            plt.plot(range(len(data)), np.polyval(p, range(len(data))))
        # valid peak found, add it to the list
        maxPositions.append(-p[1]/(2*p[0]))
        # get the first peak
        if np.mean(group)<firstObservedPeakPos:
            firstObservedPeakPos = maxPositions[-1]

    return maxPositions

if __name__ == '__main__':
    path = r'Z:\Darren\Data\2015\10-6 Wavemeter forms'

    blanklist = glob.glob(os.path.join(path, 'blank*.txt'))
    list461 = glob.glob(os.path.join(path, '460*.txt'))
    list632 = glob.glob(os.path.join(path, '632*.txt'))
    list671 = glob.glob(os.path.join(path, '670*.txt'))
    list689 = glob.glob(os.path.join(path, '689*.txt'))

    b1 = np.loadtxt(blanklist[0])
    l1 = np.loadtxt(list461[4])
    for f in list632:
        print fitInterference(np.loadtxt(f), debugging=False)

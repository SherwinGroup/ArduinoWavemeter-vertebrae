# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 15:06:30 2015

@author: Home
"""

from __future__ import absolute_import

import numpy as np
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.console as pgc
from InstsAndQt.Instruments import ArduinoWavemeter
from InstsAndQt.customQt import *
import copy
import os
import glob
import time
from arduinoWindow_ui import Ui_ArduinoWavemeter
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

import logging

log = logging.getLogger("ArduinoWavemeter")
log.setLevel(logging.DEBUG)
handler = logging.FileHandler("TheLog.log")
handler.setLevel(logging.DEBUG)
handler1 = logging.StreamHandler()
handler1.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)s - %(funcName)s()] - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler1.setFormatter(formatter)
log.addHandler(handler)
log.addHandler(handler1)

try:
    import visa
except:
    log.critical('GPIB VISA library not installed')
    raise

class ArduinoWavemeterWindow(QtGui.QMainWindow):
    thQueryingLoop = TempThread()
    sigUpdateGraphs = QtCore.pyqtSignal(object)
    def __init__(self, *arg, **kwargs):
        super(ArduinoWavemeterWindow, self).__init__(*arg, **kwargs)
        self.initUI()
        self.arduino = None
        self.doLoop = True
        self.arduinoData = [0]
        self.fftData = [0]

        self.ui.cGPIB.currentIndexChanged.connect(self.openArduino)
        self.openArduino()
        self.sigUpdateGraphs.connect(self.updateGraphs)

        self.thQueryingLoop.target = self.loopArduinoCalls
        self.thQueryingLoop.start()

    def initUI(self):
        self.ui = Ui_ArduinoWavemeter()
        self.ui.setupUi(self)

        self.ui.splitter_2.setStretchFactor(0, 10)
        self.ui.splitter_2.setStretchFactor(1, 1)

        resources = list(visa.ResourceManager().list_resources())
        resources.append('Fake')
        self.ui.cGPIB.addItems(resources)
        self.ui.cGPIB.setCurrentIndex(self.ui.cGPIB.findText('Fake'))

        self.pRealSpace = self.ui.gRealSpace.plot(pen='k')
        pi = self.ui.gRealSpace.plotItem
        pi.setTitle('Real Space Output')
        pi.setLabel('left', 'Signal')
        pi.setLabel('bottom', 'Pixel')

        self.pFFT = self.ui.gFFT.plot(pen='k')
        pi = self.ui.gFFT.plotItem
        pi.setTitle('Frequency Space Output')
        pi.setLabel('left', 'Mag')
        pi.setLabel('bottom', 'Pixel-1')
        pi.setLogMode(y=True)

        self.debugElements = [
            self.ui.gRealSpace,
            self.ui.gFFT,
            self.ui.bSave,
            self.ui.gbSaveName
        ]
        self.ui.mExtrasDebugmode.triggered.connect(self.toggleDebugFeatures)
        self.ui.bSave.clicked.connect(self.saveOutput)
        self.toggleDebugFeatures(False)

        self.show()


    def openArduino(self):
        try:
            self.doLoop = False
            self.thQueryingLoop.wait()
        except Exception as e:
            log.error("Error waiting for previous loop {}".format(e))
        try:
            self.arduino.close()
        except:
            pass

        try:
            self.arduino = ArduinoWavemeter(str(self.ui.cGPIB.currentText()))
        except:
            log.error("Error opening arduino")
            self.ui.cGPIB.currentIndexChanged.disconnect(self.openArduino)
            self.arduino = ArduinoWavemeter('Fake')
            self.ui.cGPIB.setCurrentIndex(self.ui.cGPIB.findText('Fake'))
            self.ui.cGPIB.currentIndexChanged.connect(self.openArduino)

        self.arduino.open()

        self.doLoop = True
        self.thQueryingLoop.start()

    def loopArduinoCalls(self):
        while self.doLoop:
            try:
                newData = self.arduino.read_values(self.ui.tExposure.value())
                if not newData:
                    self.sigUpdateGraphs.emit('r')
                    continue
                self.arduinoData = newData
                self.fftData = np.abs(np.fft.rfft(newData))

                self.sigUpdateGraphs.emit('k')
            except AttributeError:
                pass # happens before you open the resource
            time.sleep(0.5)

    def updateGraphs(self, pen='k'):
        if not self.ui.mExtrasDebugmode.isChecked():
            return
        try:
            self.pRealSpace.setData(self.arduinoData, pen=pen)
            self.pFFT.setData(self.fftData, pen=pen)
        except Exception as e:
            print self.arduinoData, type(self.arduinoData)

    def toggleDebugFeatures(self, b):
        for e in self.debugElements:
            e.setVisible(b)

    def saveOutput(self):
        try:
            baseText = str(self.ui.tSaveName.text())
            filelist = glob.glob('{}*.txt'.format(baseText))
            print "there are tehse files already,", filelist
            newname = '{}_{:03d}.txt'.format(baseText, len(filelist))
            np.savetxt(newname, self.arduinoData, fmt='%d')
        except Exception as e:
            print "error saving", e

    def closeEvent(self, *args, **kwargs):
        self.doLoop = False
        try:
            self.thQueryingLoop.wait()
        except Exception as e:
            log.error("Error waiting for thread to close {}".format(e))

        self.arduino.close()
        self.close()



































if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    ex = ArduinoWavemeterWindow()
    sys.exit(app.exec_())







# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\dvalovcin\Documents\GitHub\ArduinoWavemeter-vertebrae\arduinoWindow.ui'
#
# Created: Fri Sep 25 17:32:52 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ArduinoWavemeter(object):
    def setupUi(self, ArduinoWavemeter):
        ArduinoWavemeter.setObjectName(_fromUtf8("ArduinoWavemeter"))
        ArduinoWavemeter.resize(1093, 789)
        self.centralwidget = QtGui.QWidget(ArduinoWavemeter)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.gRealSpace = PlotWidget(self.splitter)
        self.gRealSpace.setObjectName(_fromUtf8("gRealSpace"))
        self.gFFT = PlotWidget(self.splitter)
        self.gFFT.setObjectName(_fromUtf8("gFFT"))
        self.gridLayoutWidget = QtGui.QWidget(self.splitter_2)
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(self.gridLayoutWidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tWavelengthnm = QtGui.QLineEdit(self.groupBox)
        self.tWavelengthnm.setReadOnly(True)
        self.tWavelengthnm.setObjectName(_fromUtf8("tWavelengthnm"))
        self.horizontalLayout.addWidget(self.tWavelengthnm)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 2, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.gridLayoutWidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tWavelengthcm = QtGui.QLineEdit(self.groupBox_2)
        self.tWavelengthcm.setReadOnly(True)
        self.tWavelengthcm.setObjectName(_fromUtf8("tWavelengthcm"))
        self.horizontalLayout_2.addWidget(self.tWavelengthcm)
        self.gridLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.gridLayoutWidget)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.cGPIB = QtGui.QComboBox(self.groupBox_4)
        self.cGPIB.setObjectName(_fromUtf8("cGPIB"))
        self.horizontalLayout_4.addWidget(self.cGPIB)
        self.gridLayout.addWidget(self.groupBox_4, 1, 1, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.gridLayoutWidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setContentsMargins(0, 10, 0, 0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tExposure = QFNumberEdit(self.groupBox_3)
        self.tExposure.setObjectName(_fromUtf8("tExposure"))
        self.horizontalLayout_3.addWidget(self.tExposure)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.horizontalLayout_5.addWidget(self.splitter_2)
        ArduinoWavemeter.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ArduinoWavemeter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        ArduinoWavemeter.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ArduinoWavemeter)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ArduinoWavemeter.setStatusBar(self.statusbar)

        self.retranslateUi(ArduinoWavemeter)
        QtCore.QMetaObject.connectSlotsByName(ArduinoWavemeter)

    def retranslateUi(self, ArduinoWavemeter):
        ArduinoWavemeter.setWindowTitle(_translate("ArduinoWavemeter", "Arduino Wavemeter", None))
        self.groupBox.setTitle(_translate("ArduinoWavemeter", "Wavelength (nm)", None))
        self.tWavelengthnm.setText(_translate("ArduinoWavemeter", "0", None))
        self.groupBox_2.setTitle(_translate("ArduinoWavemeter", "Wavelength (cm-1)", None))
        self.tWavelengthcm.setText(_translate("ArduinoWavemeter", "0", None))
        self.groupBox_4.setTitle(_translate("ArduinoWavemeter", "GPIB", None))
        self.groupBox_3.setTitle(_translate("ArduinoWavemeter", "Exposure (ms)", None))
        self.tExposure.setText(_translate("ArduinoWavemeter", "50", None))

from pyqtgraph import PlotWidget
from InstsAndQt.customQt import QFNumberEdit

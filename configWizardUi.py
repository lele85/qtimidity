# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../ui/configWizard.ui'
#
# Created: Sat Oct 10 11:44:19 2009
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(273, 197)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout2 = QtGui.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.downloadLabel = QtGui.QLabel(Dialog)
        self.downloadLabel.setEnabled(True)
        self.downloadLabel.setObjectName("downloadLabel")
        self.horizontalLayout2.addWidget(self.downloadLabel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout2.addItem(spacerItem1)
        self.okDownloadLabel = QtGui.QLabel(Dialog)
        self.okDownloadLabel.setObjectName("okDownloadLabel")
        self.horizontalLayout2.addWidget(self.okDownloadLabel)
        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.horizontalLayout1 = QtGui.QHBoxLayout()
        self.horizontalLayout1.setObjectName("horizontalLayout1")
        self.unzipLabel = QtGui.QLabel(Dialog)
        self.unzipLabel.setEnabled(True)
        self.unzipLabel.setObjectName("unzipLabel")
        self.horizontalLayout1.addWidget(self.unzipLabel)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout1.addItem(spacerItem2)
        self.okUnzipLabel = QtGui.QLabel(Dialog)
        self.okUnzipLabel.setObjectName("okUnzipLabel")
        self.horizontalLayout1.addWidget(self.okUnzipLabel)
        self.verticalLayout.addLayout(self.horizontalLayout1)
        self.horizontalLayout3 = QtGui.QHBoxLayout()
        self.horizontalLayout3.setObjectName("horizontalLayout3")
        self.decompressLabel = QtGui.QLabel(Dialog)
        self.decompressLabel.setEnabled(True)
        self.decompressLabel.setObjectName("decompressLabel")
        self.horizontalLayout3.addWidget(self.decompressLabel)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout3.addItem(spacerItem3)
        self.okDecompressLabel = QtGui.QLabel(Dialog)
        self.okDecompressLabel.setObjectName("okDecompressLabel")
        self.horizontalLayout3.addWidget(self.okDecompressLabel)
        self.verticalLayout.addLayout(self.horizontalLayout3)
        self.horizontalLayout5 = QtGui.QHBoxLayout()
        self.horizontalLayout5.setObjectName("horizontalLayout5")
        self.configLabel = QtGui.QLabel(Dialog)
        self.configLabel.setEnabled(True)
        self.configLabel.setObjectName("configLabel")
        self.horizontalLayout5.addWidget(self.configLabel)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout5.addItem(spacerItem4)
        self.okConfigLabel = QtGui.QLabel(Dialog)
        self.okConfigLabel.setObjectName("okConfigLabel")
        self.horizontalLayout5.addWidget(self.okConfigLabel)
        self.verticalLayout.addLayout(self.horizontalLayout5)
        spacerItem5 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.verticalLayout.addItem(spacerItem5)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout4 = QtGui.QHBoxLayout()
        self.horizontalLayout4.setObjectName("horizontalLayout4")
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout4.addItem(spacerItem6)
        self.okButton = QtGui.QToolButton(Dialog)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout4.addWidget(self.okButton)
        self.verticalLayout.addLayout(self.horizontalLayout4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.actionOk = QtGui.QAction(Dialog)
        self.actionOk.setObjectName("actionOk")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOk.setText(QtGui.QApplication.translate("Dialog", "ok", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())


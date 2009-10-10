import os,sys,shutil
from subprocess import *
# Import Qt modules
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
# Import the compiled UI module
from configWizardUi import Ui_Dialog
#Regular expressions
import re

BINDIR = os.path.dirname(os.path.realpath( __file__ ))
#FLUIDR_LINK = "http://sunsite.univie.ac.at/musicres/thammer/HammerSound/localfiles/soundfonts/FluidR3122501.zip"
FLUIDR_LINK = "http://localhost/fluidr3.zip"
CONFIG_FILE_NAME = "timidity.cfg"
COMPRESSED_SOUNDFONT_FILE_NAME = "FluidR3 GM.sfArk"
CONFIG_FILE_PATH = os.path.join(BINDIR, "config/", CONFIG_FILE_NAME)
CONFIG_DIR_DESTINATION_PATH = os.path.join(os.path.expanduser("~"),".qtimidity")
CONFIG_FILE_DESTINATION_PATH = os.path.join(CONFIG_DIR_DESTINATION_PATH, "timidity.cfg")
FLUIDR_FILE_DESTINATION_PATH = os.path.join(CONFIG_DIR_DESTINATION_PATH, "fluidr3.zip")
SOUNDFONT_FILE_ORIGINAL_PATH = os.path.join(CONFIG_DIR_DESTINATION_PATH, "FluidR3 GM.SF2")
SOUNDFONT_FILE_DESTINATION_PATH = os.path.join(CONFIG_DIR_DESTINATION_PATH, "fluidr3.sf2")
DELETE_FILENAMES = ["FluidR3 GM.sfArk", "FluidR3 GS.sfArk","Fluid R3- Readme.doc", "fluidr3.zip", "Frank's Custom Reverb.ea2"]
SFARXTC_COMMAND = "sfarkxtc"

class sfarkxtcThread(QThread):
    def __init__(self, parent=None):
	QThread.__init__(self, parent)
	self.decompress = None
	self.progress = 0
	
    def run(self):
	self.decompress = QProcess();
	self.connect(self.decompress, SIGNAL("readyReadStandardOutput()"), self.updateOutput)
	#self.decompress = Popen([SFARXTC_COMMAND, os.path.join(CONFIG_DIR_DESTINATION_PATH,COMPRESSED_SOUNDFONT_FILE_NAME)])
	self.decompress.start(SFARXTC_COMMAND, [os.path.join(CONFIG_DIR_DESTINATION_PATH,COMPRESSED_SOUNDFONT_FILE_NAME)])
	self.decompress.waitForFinished(-1)
	
    def updateOutput(self):
	bytes = self.decompress.readAllStandardOutput()
	progressList = re.findall('[0-9]+', str(bytes))
	self.progress = int((progressList[0]))
	self.emit(SIGNAL("progressChanged(int, int)"), self.progress,100)

	
class unzipThread(QThread):
    def __init__(self, parent=None):
	QThread.__init__(self, parent)
	
    def run(self):
	import zipfile
	z = zipfile.ZipFile(FLUIDR_FILE_DESTINATION_PATH)
	z.extractall(CONFIG_DIR_DESTINATION_PATH)
	z.close()
	
class configThread(QThread):
    def __init__(self, parent=None):
	QThread.__init__(self, parent)
	
    def run(self):
	shutil.move(SOUNDFONT_FILE_ORIGINAL_PATH, SOUNDFONT_FILE_DESTINATION_PATH)
	shutil.copy(CONFIG_FILE_PATH, CONFIG_FILE_DESTINATION_PATH)
	for filename in DELETE_FILENAMES:
	    os.remove(os.path.join(CONFIG_DIR_DESTINATION_PATH, filename))
	

class Form(QDialog):
    def __init__(self,parent=None):
	QDialog.__init__(self)
	# This is always the same
	self.ui = Ui_Dialog()
	self.ui.setupUi(self)
	#If conf dir doesn't exist create it
	if not os.path.isdir(CONFIG_DIR_DESTINATION_PATH):
	    os.mkdir(CONFIG_DIR_DESTINATION_PATH)
	#Done pixmap
	self.donePixmap = QPixmap(22,22)
	self.donePixmap.load(":/22x22/dialog-ok-apply.png")
	self.ui.okDownloadLabel.setPixmap(self.donePixmap)
	self.ui.okUnzipLabel.setPixmap(self.donePixmap)
	self.ui.okDecompressLabel.setPixmap(self.donePixmap)
	self.ui.okConfigLabel.setPixmap(self.donePixmap)
	self.ui.okDownloadLabel.setEnabled(False)
	self.ui.okUnzipLabel.setEnabled(False)
	self.ui.okDecompressLabel.setEnabled(False)
	self.ui.okConfigLabel.setEnabled(False)
	self.ui.downloadLabel.setText(self.tr("<b>Downloading File</b>"))
	self.ui.unzipLabel.setText(self.tr("Unzipping Archive"))
	self.ui.decompressLabel.setText(self.tr("Decompressing Soundfont"))
	self.ui.configLabel.setText(self.tr("Ultimating Configuration"))
	# Setup ok button
	self.ui.okButton.setDefaultAction(self.ui.actionOk)
	self.ui.okButton.setEnabled(False)
	self.connect(self.ui.actionOk, SIGNAL("triggered()"), self, SLOT("close()"));
	# Enable download label
	self.ui.downloadLabel.setEnabled(True)
        self.manager = QNetworkAccessManager(self)
	#Proxy settings
	#self.proxy = QNetworkProxy(QNetworkProxy.HttpProxy, '193.205.128.8', 3128)
	#self.manager.setProxy(self.proxy)
	#Start download
	url = QUrl(FLUIDR_LINK)
	self.reply = self.manager.get(QNetworkRequest(url))
	self.connect(self.reply,SIGNAL("readyRead()"), self.readyRead)
	self.connect(self.manager,SIGNAL("finished(QNetworkReply*)"), self.replyFinished)
	self.connect(self.reply, SIGNAL("downloadProgress(qint64, qint64)"), self.progress)
    
    def readyRead(self):
	zipFile = QFile(FLUIDR_FILE_DESTINATION_PATH)
	zipFile.open(QIODevice.WriteOnly | QIODevice.Append)
	zipFile.write(self.reply.readAll())
	zipFile.close()
	
	
    def replyFinished(self, reply):
	self.ui.okDownloadLabel.setEnabled(True)
	self.ui.downloadLabel.setText(self.tr("Downloading File"))
	self.ui.unzipLabel.setText(self.tr("<b>Unzipping Archive</b>"))
	self.progress(0,0)
	self.unzipThread = unzipThread()
	self.connect(self.unzipThread, SIGNAL("finished()"), self.unzipThreadDone)
	self.unzipThread.start()

    def unzipThreadDone(self):
	#self.progress(100,100)
	self.ui.unzipLabel.setText(self.tr("Unzipping Archive"))
	self.ui.okUnzipLabel.setEnabled(True)
	self.ui.decompressLabel.setText(self.tr("<b>Decompressing Soundfont</b>"))
	self.decompressThread = sfarkxtcThread()
	self.decompressThread.start()
	self.connect(self.decompressThread, SIGNAL("finished()"), self.decompressThreadDone)
	self.connect(self.decompressThread, SIGNAL("progressChanged(int, int)"), self.progress)

    def decompressThreadDone(self):
	self.progress(100,100)
	self.ui.decompressLabel.setText(self.tr("Decompressing Soundfonts"))
	self.ui.okDecompressLabel.setEnabled(True)
	self.configThread = configThread()
	self.configThread.start()
	self.connect(self.configThread, SIGNAL("finished()"), self.configThreadDone)

    def configThreadDone(self):
	self.progress(100,100)
	self.ui.configLabel.setText(self.tr("Ultimating Configuration"))
	self.ui.okConfigLabel.setEnabled(True)
	self.ui.okButton.setEnabled(True)
    
    def progress(self, read, total):
	self.ui.progressBar.setMinimum(0)
	self.ui.progressBar.setMaximum(total)
	self.ui.progressBar.setValue(read)

def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    app = QApplication(sys.argv)
    window=Form()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
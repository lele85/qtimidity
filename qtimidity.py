#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
# Import Qt modules
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
# Import the compiled UI module
from qtimidityUi import Ui_MainWindow

CONFIG_DIR_DESTINATION_PATH = os.path.join(os.path.expanduser("~"),".qtimidity")
CONFIG_FILE_DESTINATION_PATH = os.path.join(CONFIG_DIR_DESTINATION_PATH, "timidity.cfg")
SOUNDFONT_FILE_DESTINATION_PATH = os.path.join(CONFIG_DIR_DESTINATION_PATH, "fluidr3.sf2")
TIMIDITY_COMMAND = 'timidity'

class timidityThread(QThread):
    def __init__(self, playlistModel, nowPlayingLabel, parent=None):
	QThread.__init__(self, parent)
	self.play = []
	self.playlistModel = playlistModel
	self.playlist = self.playlistModel.fileInfoList[self.playlistModel.filePlaying - 1:self.playlistModel.rowCount()]
	self.nowPlayingLabel = nowPlayingLabel

    def run(self):
	while True:
	    try:
		song = self.playlist[0]
		fileName = self.playlistModel.fileInfoList[self.playlistModel.filePlaying - 1].fileName()
		self.nowPlayingLabel.setText(self.tr("Playing: <b>") + fileName + "</b>")
		self.play = QProcess();
		self.play.start(TIMIDITY_COMMAND, ["-c",CONFIG_FILE_DESTINATION_PATH, song.filePath()])
		self.play.waitForFinished(-1)
		self.playlistModel.setFilePlaying(self.playlistModel.filePlaying + 1)
		self.playlist = self.playlistModel.fileInfoList[self.playlistModel.filePlaying - 1 : self.playlistModel.rowCount()]
	    except IndexError:
		self.playlistModel.setFilePlaying(None)
		return

    def setPlaylist(self, playlist):
	self.playlist = playlist
    
    def emptyPlaylist(self):
	self.playlist = []
    
class PlayListModel(QAbstractTableModel): 
    def __init__(self, fileInfoList=[], parent=None): 
        """ fileInfoList: a QFileInfo List where each item is a row
        """
        QAbstractListModel.__init__(self, parent) 
        self.fileInfoList = fileInfoList
	self.filePlaying = None

    def filePlaying(self):
	return self.filePlaying
	
    def rowCount(self, index=QModelIndex()): 
        return len(self.fileInfoList) 
    
    def columnCount(self, index=QModelIndex()):
	return 1

    def data(self, index, role=Qt.DisplayRole): 
        if not index.isValid() or not  0 <= index.row() < len(self.fileInfoList):
            return QVariant()
	fileInfo = self.fileInfoList[index.row()]
	column = index.column()
	if role == Qt.DisplayRole:
	    return QVariant(fileInfo.fileName())
	elif role == Qt.FontRole:
	    if self.filePlaying == index.row() + 1:
		font = QFont()
		font.setBold(True)
		return QVariant(font)
	elif role == Qt.BackgroundColorRole:
	    if self.filePlaying == index.row() + 1:
		return QVariant(QColor(96, 148, 207))
	elif role == Qt.TextColorRole:
	    if self.filePlaying == index.row() + 1:
		return QVariant(QColor(255, 255, 255))

    
    def insertRows(self, row, count, fileInfo, parent=QModelIndex()):
	self.beginInsertRows(QModelIndex(), row, row + count - 1)
	self.fileInfoList.append(fileInfo)
	self.endInsertRows()
	return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
	self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
	if position == -1:return False
	if self.filePlaying == position + 1:
	    self.fileInfoList.pop(position)
	elif self.filePlaying < position + 1:
	    self.fileInfoList.pop(position)
	elif self.filePlaying > position + 1:
	    self.filePlaying = self.filePlaying - 1
	    self.fileInfoList.pop(position)
	self.endRemoveRows()
	return True
    
    def setFilePlaying(self,row):
	self.filePlaying = row
	self.reset()
	return
	

# Create a class for our main window
class Main(QMainWindow):
    def __init__(self):
	QMainWindow.__init__(self)
	# This is always the same
	self.ui = Ui_MainWindow()
	self.ui.setupUi(self)
	#Model View Playlist
	self.playlistModel = PlayListModel()
	self.ui.playtableView.setModel(self.playlistModel)
	self.ui.playtableView.horizontalHeader().setStretchLastSection(True)
	#NavigationModel
	self.navigationModel = QDirModel()
	self.navigationModel.setFilter(QDir.Files | QDir.AllDirs | QDir.NoSymLinks | QDir.NoDotAndDotDot)
	nameFilters = []
	nameFilters.append("*.mid")
	nameFilters.append("*.midi")
	self.navigationModel.setNameFilters(nameFilters)
	self.ui.navigationView.setModel(self.navigationModel)
	self.ui.navigationView.setRootIndex(self.navigationModel.index(QDir.currentPath()))
	#Associate Actions to buttons
	self.ui.nextButton.setDefaultAction(self.ui.actionNext)
	self.ui.prevButton.setDefaultAction(self.ui.actionPrev)
	self.ui.playButton.setDefaultAction(self.ui.actionPlay)
	self.ui.stopButton.setDefaultAction(self.ui.actionStop)
	self.ui.homeButton.setDefaultAction(self.ui.actionNavigationHome)
	self.ui.upButton.setDefaultAction(self.ui.actionNavigationUp)
	# If soundfonts are installed and configured disable configuration wizard
	if os.path.exists(SOUNDFONT_FILE_DESTINATION_PATH):
	    self.ui.actionConfWizard.setEnabled(False)
	# Connect actionQuick to default quit SLOT
	self.connect(self.ui.actionQuit, SIGNAL("triggered()"), self, SLOT("close()"));
	#File actually playing
	self.play = None
	#Statusbar nowplaying label
	self.nowPlayingLabel = QLabel()
	self.nowPlayingLabel.setText(self.tr("Playing: <b>Nothing</b>"))
	self.ui.statusbar.addWidget(self.nowPlayingLabel)
	# If a path is passed via commandline enquee the midi and play it
	try:
	    fileInfo = QFileInfo(sys.argv[1])
	    row = self.playlistModel.rowCount()
	    self.playlistModel.insertRows(row, 1, fileInfo)
	    self.ui.playtableView.resizeRowToContents(row)
	    self.ui.navigationView.setRootIndex(self.navigationModel.index(fileInfo.path()))
	    self.playlistModel.setFilePlaying(1)
	    self.ui.actionPlay.trigger()
	except IndexError:
	    pass
	#Empty thread
	self.thread = None
	
    def on_navigationView_doubleClicked(self,newIndex):
	''' On dir doubleclick set new directory in navigation view, on doubleclick on midi file enqueue it in playlist'''
	if (QDirModel.isDir(self.navigationModel,newIndex) == True):
	    self.ui.navigationView.setRootIndex(newIndex)
	else:
	    fileInfo = QDirModel.fileInfo(self.navigationModel, newIndex)
	    row = self.playlistModel.rowCount()
	    self.playlistModel.insertRows(row, 1, fileInfo)
	    self.ui.playtableView.resizeRowToContents(row)
	    
	    
    
    def on_playtableView_doubleClicked(self, playtableIndex):
	'''Play double clicked items in playlist'''
	self.playlistModel.setFilePlaying(playtableIndex.row() + 1)
	self.ui.actionPlay.trigger()
	
    def on_actionNext_triggered(self, checked=None):
	'''Play current item in playlistWidget'''
	if checked is None: return
	if (self.playlistModel.filePlaying == self.playlistModel.rowCount()):
	    return
	else:
	    self.playlistModel.setFilePlaying(self.playlistModel.filePlaying + 1)
	    self.ui.actionStop.trigger()
	    self.ui.actionPlay.trigger()
	    
    def on_actionPrev_triggered(self, checked=None):
	'''Play current item in playlistWidget'''
	if checked is None: return
	if (self.playlistModel.filePlaying == 1):
	    return
	else:
	    self.playlistModel.setFilePlaying(self.playlistModel.filePlaying - 1)
	    self.ui.actionStop.trigger()
	    self.ui.actionPlay.trigger()
    
    def on_actionRemove_triggered(self, checked=None):
	if checked is None: return
	if self.playlistModel.filePlaying == self.ui.playtableView.currentIndex().row() + 1:
	    self.playlistModel.removeRows(self.ui.playtableView.currentIndex().row())
	    self.ui.actionStop.trigger()
	    self.ui.actionPlay.trigger()
	else:
	    self.playlistModel.removeRows(self.ui.playtableView.currentIndex().row())

    def on_actionPlay_triggered(self, checked=None):
	if checked is None: return
	if not self.thread == None:
	    self.ui.actionStop.trigger()
	self.thread = timidityThread(self.playlistModel, self.nowPlayingLabel)
	self.thread.start()

	    
    def on_actionStop_triggered(self, checked=None):
	'''Stop current playing file '''
	if checked is None: return
	self.thread.emptyPlaylist()
	self.thread.terminate()
	self.thread.play.terminate()
	self.thread.play.kill()
	self.nowPlayingLabel.setText(self.tr("Playing: <b>Nothing</b>"))

    def closeEvent(self,event):
	'''Stop current playing song before exit app'''
	self.thread.terminate()
	self.thread.play.terminate()
	self.thread.play.kill()
    
    def on_actionNavigationUp_triggered(self, checked=None):
	if checked is None: return
	currentDir = QDir(self.navigationModel.filePath(self.ui.navigationView.rootIndex()))
	QDir.cdUp(currentDir)
	self.ui.navigationView.setRootIndex(self.navigationModel.index(currentDir.canonicalPath()))
	
    def on_actionNavigationHome_triggered(self, checked=None):
	if checked is None: return
	self.ui.navigationView.setRootIndex(self.navigationModel.index(QDir.homePath()))
	
    def on_actionConfWizard_triggered(self, checked=None):
	if checked is None: return
	import configWizard
	self.dialog = configWizard.Form(self)
	self.dialog.exec_()
	self.ui.actionConfWizard.setEnabled(False)

def main():
    # Again, this is boilerplate, it's going to be the same on
    # almost every app you write
    binDir = os.path.dirname(os.path.realpath( __file__ ))
    app = QApplication(sys.argv)
    app.setDesktopSettingsAware(False)
    #Internationalization
    translator = QTranslator()
    translator.load('qtimidity_' + QLocale.system().name(), binDir+'/translations')
    app.installTranslator(translator)
    window=Main()
    window.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

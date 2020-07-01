#!/usr/bin/env python3

# Filename: torrent_gui.py

import sys
import os
from functools import partial
import subprocess
import sqlite3

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import QFileDialog

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Models definition

# def evaluateExpression(expression):
#     """Evaluate an expression."""
#     try:
#         result = str(eval(expression, {}, {}))
#     except Exception:
#         result = ERROR_MSG

#     return result

# Create a subclass of QMainWindow to setup the calculator's GUI
class TorrentUI(QMainWindow):
    """ECOTorrent's View (GUI)."""

    def __init__(self):
        """View initializer."""
        super().__init__()
        self.currentTorrents = []
        print('python server\\tracker_server.py')
        subprocess.Popen('python server\\tracker_server.py')
        subprocess.Popen('python client\\file\\send_file.py')
        print(BASE_DIR + '\\client\\db\\files.db')
        conn = sqlite3.connect(BASE_DIR + '\\client\\db\\files.db')
        c = conn.cursor()

        try:
            c.execute('SELECT * FROM files')
            files = c.fetchall()
            for file in files:
                fileDict = {
                    'isSelected': False,
                    'file_name': file[2],
                    'bytes_downloaded': 0,
                    'total_size': int(file[3]),
                    'status': 0,
                    'speed': 0,
                }
                self.currentTorrents.append(fileDict)
        except Exception as e:
            print(e)

        conn.close()

        # Set some main window's properties
        self.setWindowTitle('ECOTorrent')
        self.setFixedSize(750, 600)
        # Set the central widget and the general layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Set Font
        font = QtGui.QFont()
        font.setFamily("Neufreit ExtraBold")
        font.setPointSize(15)
        self.setFont(font)
        # Set Icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui\gear.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        # Create basic components
        self._createTitle()
        self.componentsWidget = QWidget(self._centralWidget)
        self.componentsLayout = QtWidgets.QHBoxLayout()
        self.componentsWidget.setLayout(self.componentsLayout)
        self.generalLayout.addWidget(self.componentsWidget)
        self._createButtons()
        self._createDisplay()

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.onTimeout)
        timer.start(1000)

    def onTimeout(self):
        newTorrents = self.currentTorrents
        if newTorrents:
            newTorrents[0]['bytes_downloaded'] = newTorrents[0]['bytes_downloaded'] + 5
            self.updateTorrentComponents(newTorrents=newTorrents)

    def updateTorrentComponents(self, newTorrents):
        current = self.currentTorrents
        for i in range(len(self.currentTorrents)):
            self.updateSingleComponent(current[i], newTorrents[i])

    def createTorrentComponents(self):
        for i in range(len(self.currentTorrents)):
            newComponent = self.createSingleTorrentComponent(self.currentTorrents[i]['isSelected'], self.currentTorrents[i]['file_name'],
                                                             self.currentTorrents[i]['bytes_downloaded'], self.currentTorrents[i]['total_size'],
                                                             self.currentTorrents[i]['status'], self.currentTorrents[i]['speed'])
            self.currentTorrents[i]['component'] = newComponent
            self.verticalLayout.addWidget(newComponent)

    def createSingleTorrentComponent(self, isSelected, file_name, bytes_downloaded, total_size, status, speed):
        self.torrent_file = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.torrent_file.setMinimumSize(QtCore.QSize(0, 150))
        self.torrent_file.setMaximumSize(QtCore.QSize(16777215, 150))
        self.torrent_file.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.torrent_file.setObjectName("torrent_file")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.torrent_file)
        self.verticalLayout_11.setContentsMargins(7, 7, 7, 7)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.topLine = QtWidgets.QFrame(self.torrent_file)
        self.topLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.topLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.topLine.setObjectName("topLine")
        self.verticalLayout_11.addWidget(self.topLine)
        self.torrentFileInfo = QtWidgets.QWidget(self.torrent_file)
        self.torrentFileInfo.setObjectName("torrentFileInfo")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.torrentFileInfo)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox = QtWidgets.QCheckBox(self.torrentFileInfo)
        self.checkBox.setMinimumSize(QtCore.QSize(25, 25))
        self.checkBox.setMaximumSize(QtCore.QSize(25, 25))
        self.checkBox.setText("")
        self.checkBox.setChecked(isSelected)
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.toggled.connect(partial(self.onChecked, self.torrent_file))
        self.horizontalLayout_5.addWidget(self.checkBox)
        self.fileIcon = QtSvg.QSvgWidget('ui\documento.svg')  # add svg
        self.fileIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.fileIcon.setObjectName("fileIcon")
        self.horizontalLayout_5.addWidget(self.fileIcon)
        self.fileInfo = QtWidgets.QWidget(self.torrentFileInfo)
        self.fileInfo.setMinimumSize(QtCore.QSize(0, 50))
        self.fileInfo.setObjectName("fileInfo")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.fileInfo)
        self.verticalLayout_12.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_12.setSpacing(5)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.fileName = QtWidgets.QLabel(self.fileInfo)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.fileName.setFont(font)
        self.fileName.setObjectName("fileName")
        self.fileName.setText(file_name)
        self.verticalLayout_12.addWidget(self.fileName)
        self.fileProgress = QtWidgets.QLabel(self.fileInfo)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.fileProgress.setFont(font)
        self.fileProgress.setObjectName("fileProgress")
        self.fileProgress.setText(str(bytes_downloaded/1000) + "Kb de " + str(total_size/1000) + "Kb")
        self.verticalLayout_12.addWidget(self.fileProgress)
        self.horizontalLayout_5.addWidget(self.fileInfo)
        self.verticalLayout_11.addWidget(self.torrentFileInfo)
        self.progressBar = QtWidgets.QProgressBar(self.torrent_file)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", bytes_downloaded / total_size * 100)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_11.addWidget(self.progressBar)
        self.statusLabel = QtWidgets.QLabel(self.torrent_file)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.statusLabel.setFont(font)
        self.statusLabel.setObjectName("statusLabel")
        self.statusLabel.setText("Status: " + str(status) + " - Velocidade: " + str(speed) + " Mb/s")
        self.verticalLayout_11.addWidget(self.statusLabel)
        self.bottomLine = QtWidgets.QFrame(self.torrent_file)
        self.bottomLine.setFrameShadow(QtWidgets.QFrame.Plain)
        self.bottomLine.setLineWidth(1)
        self.bottomLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.bottomLine.setObjectName("bottomLine")
        self.verticalLayout_11.addWidget(self.bottomLine)
        return self.torrent_file

    def onChecked(self, torrent):
        for file in self.currentTorrents:
            if (file['component'] == torrent):
                file['isSelected'] = not file['isSelected']
                print(self.currentTorrents)

    def updateSingleComponent(self, item, newValues):
        item = self.currentTorrents[self.currentTorrents.index(item)]
        self.verticalLayout.removeWidget(item['component'])
        item['component'].deleteLater()
        item['isSelected'] = newValues['isSelected']
        item['file_name'] = newValues['file_name']
        item['bytes_downloaded'] = newValues['bytes_downloaded']
        item['total_size'] = newValues['total_size']
        item['status'] = newValues['status']
        item['speed'] = newValues['speed']
        newComponent = self.createSingleTorrentComponent(item['isSelected'], item['file_name'],
                                                         item['bytes_downloaded'], item['total_size'], item['status'],
                                                         item['speed'])
        item['component'] = newComponent
        self.verticalLayout.addWidget(newComponent)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(None, "Selecione um arquivo .torrent", "", "All Files (*)",
                                                  options=options)
        if fileName:
            print(fileName)
            return fileName

    def _createTitle(self):
        self.program_title = QtWidgets.QLabel()
        self.program_title.setText("ECOTorrent")
        font = QtGui.QFont()
        font.setPointSize(27)
        font.setBold(True)
        font.setWeight(75)
        self.program_title.setFont(font)
        self.generalLayout.addWidget(self.program_title)

    def _createButtons(self):
        self.verticalLayoutWidget_2 = QtWidgets.QWidget()
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 60, 161, 481))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.componentsLayout.addWidget(self.verticalLayoutWidget_2)
        self.buttonLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.buttonLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setSpacing(6)

        # Add Button
        self.add_button = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_button.sizePolicy().hasHeightForWidth())
        self.add_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Neufreit ExtraBold")
        self.add_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ui\\add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_button.setIcon(icon1)
        self.add_button.setIconSize(QtCore.QSize(100, 100))
        self.add_button.setObjectName("add_button")
        self.buttonLayout.addWidget(self.add_button)

        # Pause Button
        self.pause_button = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pause_button.sizePolicy().hasHeightForWidth())
        self.pause_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Neufreit ExtraBold")
        self.pause_button.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ui\pause.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pause_button.setIcon(icon2)
        self.pause_button.setIconSize(QtCore.QSize(75, 75))
        self.pause_button.setObjectName("pause_button")
        self.buttonLayout.addWidget(self.pause_button)

        # Continue Button
        self.continue_button = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.continue_button.sizePolicy().hasHeightForWidth())
        self.continue_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Neufreit ExtraBold")
        self.continue_button.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ui\continue.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.continue_button.setIcon(icon3)
        self.continue_button.setIconSize(QtCore.QSize(100, 75))
        self.continue_button.setObjectName("continue_button")
        self.buttonLayout.addWidget(self.continue_button)

        # Remove Button
        self.remove_button = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Neufreit ExtraBold")
        self.remove_button.setFont(font)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ui\delete.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.remove_button.setIcon(icon4)
        self.remove_button.setIconSize(QtCore.QSize(80, 70))
        self.remove_button.setObjectName("remove_button")
        self.buttonLayout.addWidget(self.remove_button)

        # About Button
        self.about_button = QtWidgets.QToolButton(self.verticalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.about_button.sizePolicy().hasHeightForWidth())
        self.about_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Neufreit ExtraBold")
        self.about_button.setFont(font)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ui\\about.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.about_button.setIcon(icon5)
        self.about_button.setIconSize(QtCore.QSize(100, 70))
        self.about_button.setObjectName("about_button")
        self.buttonLayout.addWidget(self.about_button)

    def _createDisplay(self):
        self.scrollArea_torrentFiles = QtWidgets.QScrollArea(self._centralWidget)
        self.scrollArea_torrentFiles.setGeometry(QtCore.QRect(170, 60, 631, 481))
        self.scrollArea_torrentFiles.setWidgetResizable(True)
        self.scrollArea_torrentFiles.setAlignment(QtCore.Qt.AlignTop)
        self.scrollArea_torrentFiles.setObjectName("scrollArea_torrentFiles")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -60, 612, 715))
        self.scrollAreaWidgetContents.setAcceptDrops(True)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.createTorrentComponents()

        self.scrollArea_torrentFiles.setWidget(self.scrollAreaWidgetContents)
        self.componentsLayout.addWidget(self.scrollArea_torrentFiles)


# Create a Controller class to connect the GUI and the model
class TorrentCtrl:
    """TorrentUI Controller class."""

    def __init__(self, view):
        """Controller initializer."""
        self._view = view
        # Connect signals and slots
        self._connectSignals()

    def _addTorrent(self):
        fileName = self._view.openFileNameDialog()
        if (fileName):
            os.system('python client\\file\\create_file.py ' + fileName + ' ' + os.path.basename(
                fileName) + '.ecot' + ' -ip localhost:5000')
            newFileDict = {
                'isSelected': True,
                'file_name': os.path.basename(fileName),
                'bytes_downloaded': 0,
                'total_size': 500,
                'status': 0,
                'speed': 0,
            }
            newFileDict['component'] = self._view.createSingleTorrentComponent(
                isSelected=newFileDict['isSelected'],
                file_name=newFileDict['file_name'],
                bytes_downloaded=newFileDict['bytes_downloaded'],
                total_size=newFileDict['total_size'],
                status=newFileDict['status'],
                speed=newFileDict['speed']
            )
            self._view.currentTorrents.append(
                newFileDict
            )
            self._view.verticalLayout.addWidget(
                newFileDict['component']
            )
            print(newFileDict)
            print(self._view.currentTorrents)

    def _pauseTorrent(self):
        for torrent in self._view.currentTorrents:
            if (torrent['isSelected']):
                print('if')
                oldItem = torrent
                torrent['status'] = 2
                torrent['isSelected'] = False
                self._view.updateSingleComponent(oldItem, torrent)

    def _continueTorrent(self):
        for torrent in self._view.currentTorrents:
            if (torrent['isSelected']):
                print('if')
                oldItem = torrent
                torrent['status'] = 1
                torrent['isSelected'] = False
                self._view.updateSingleComponent(oldItem, torrent)

    def _removeTorrent(self):
        for torrent in self._view.currentTorrents:
            print('for')
            if (torrent['isSelected']):
                print('if')
                self._view.currentTorrents.remove(torrent)
                self._view.verticalLayout.removeWidget(torrent['component'])
                torrent['component'].deleteLater()

    def _aboutWindow(self):
        fileName = self._view.openFileNameDialog()
        if (fileName):
            os.system('python client\\file\\create_file.py ' + fileName + ' ' + os.path.basename(
                fileName).strip() + '.ecot' + ' -ip localhost:5000')
            newFileDict = {
                'isSelected': True,
                'file_name': os.path.basename(fileName),
                'bytes_downloaded': 0,
                'total_size': 500,
                'status': 0,
                'speed': 0,
            }
            newFileDict['component'] = self._view.createSingleTorrentComponent(
                isSelected=newFileDict['isSelected'],
                file_name=newFileDict['file_name'],
                bytes_downloaded=newFileDict['bytes_downloaded'],
                total_size=newFileDict['total_size'],
                status=newFileDict['status'],
                speed=newFileDict['speed']
            )
            self._view.currentTorrents.append(
                newFileDict
            )
            self._view.verticalLayout.addWidget(
                newFileDict['component']
            )
            print(newFileDict)
            print(self._view.currentTorrents)

    def _connectSignals(self):
        """Connect signals and slots."""
        print('connecting')
        try:
            self._view.add_button.clicked.connect(self._addTorrent)
            self._view.pause_button.clicked.connect(self._pauseTorrent)
            self._view.continue_button.clicked.connect(self._continueTorrent)
            self._view.remove_button.clicked.connect(self._removeTorrent)
            self._view.about_button.clicked.connect(self._aboutWindow)
        except Exception:
            print(Exception)
        print('connected')


# Client code
def main():
    """Main function."""
    # Create an instance of QApplication
    ecotorrent = QApplication(sys.argv)
    # Show the torrent's GUI
    view = TorrentUI()
    file = open('ui/style.qss', 'r')
    # Set Style Sheet
    with file:
        qss = file.read()
        ecotorrent.setStyleSheet(qss)
    view.show()
    # Create instances of the model and the controller
    model = []
    # Create instances of the model and the controller
    ctrl = TorrentCtrl(view=view)
    # Execute the torrent's main loop
    sys.exit(ecotorrent.exec_())


if __name__ == '__main__':
    main()

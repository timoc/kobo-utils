#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Kobo Mini Chess utility editor
"""

import os
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui

# found a possibly applicable regular expression, from gnu chess
# need to look at PyChess http://code.google.com/p/pychess/w/list integration
# "(O-O(-O)?|(%s?)/?([a-h]?[1-8]?)([x-]?)([a-h][1-8])(=(%s))?)([#+])?"
class ChessValidatedItemDelegate(QtGui.QStyledItemDelegate):
    def createEditor(self, widget, option, index):
        if not index.isValid():
            return 0
        #only on the cells in the first column
        editor = QtGui.QLineEdit(widget)
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(""), editor)
        editor.setValidator(validator)
        return editor

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # initialise app
        QtGui.QMainWindow.__init__(self)

        # set to size of kobo screen
        # self.resize(800, 600)       

        # setup window title and status bar
        self.setWindowTitle('KoboChess')
        self.statusBar().showMessage('')
        
        # setup menubar with file menu
        menubar = self.menuBar()
        file = menubar.addMenu('&File')

        # add config file loader action
        aopen = QtGui.QAction('Load', self)
        aopen.setShortcut('Ctrl+O')
        aopen.setStatusTip('Open Kobo Config file')
        self.connect(aopen, QtCore.SIGNAL('triggered()'), self.loadConfigDialog)
        file.addAction(aopen)

        # add config file loader action
        asave = QtGui.QAction('Save', self)
        asave.setShortcut('Ctrl+S')
        asave.setStatusTip('Save Changes back to Kobo Config file')
        self.connect(asave, QtCore.SIGNAL('triggered()'), self.saveConfigAction)
        file.addAction(asave)
        
        # add exit action to menubar
        exit = QtGui.QAction('Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Exit')
        self.connect(exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        file.addAction(exit)
        
        # setup paths to config file
        self.eReaderPath="/media/KOBOEREADER"
        self.koboMiniConfig=os.path.join(self.eReaderPath,".kobo/Kobo/Kobo eReader.conf")
        self.koboMiniConfig=os.path.join("./", "Kobo/Kobo eReader.conf")
        self.settings=None

        # put table in application
        self.table = QtGui.QTableWidget(1,2,parent=self)
        self.setCentralWidget(self.table)
        self.table.setHorizontalHeaderLabels(("White", "Black"))
        
        # add a validator
        # tableview.setItemDelegate(ChessValidatedItemDelegate())
       

    def loadConfigDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open Config', self.koboMiniConfig)       

        self.filename = filename

        # load qsettings object to configure settings
        self.settings = QtCore.QSettings(filename,QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)
        
        self.hblack = self.settings.value("Chess/BlackIsHuman").toBool()
        self.hwhite = self.settings.value("Chess/WhiteIsHuman").toBool()
        self.hmovelist = self.settings.value("Chess/MoveList").toPyObject()

        # populate the table
        row = 0
        col = 0
        print "----Load----"
        for move in self.hmovelist:
            item = QtGui.QTableWidgetItem(move)
            item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.table.setItem(row,col,item)
            print "row:%s,col:%s Move:%s -> Item:%s" % (row,col,move,self.table.item(row,col).text())
            if col == 0: 
                col = 1
            else:
                col = 0
                row = row + 1
                self.table.insertRow(row)

        # insert 20 empty extra rows 
        row = row + 20
        self.table.setRowCount(row)

    def saveConfigAction(self):
        self.hmovelist = []
        # populate the stringlist for writing to settings
        maxrow = self.table.rowCount()
        print "----Save----"
        for row in range(0,maxrow):
            for col in (0,1):
                # stop at empty move
                if not self.table.item(row,col):
                    break
                if not self.table.item(row,col).text():
                    break
                move = self.table.item(row,col).text()
                self.hmovelist.append(move)
                print "row:%s,col:%s Move:%s -> Item:%s" % (row,col,move,self.table.item(row,col).text())
            # stop at empty move
            if not self.table.item(row,col):
                break
            if not self.table.item(row,col).text():
                break

        # write settings file back 
        self.settings.setValue("Chess/MoveList",self.hmovelist)
        self.settings.sync()

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())

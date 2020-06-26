import sys
import os
import datetime
import time
import re
import getpass
from subprocess import check_output
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

class Settings(QWidget): #Main menu
    def __init__(self, parent = None):
        
        super(Settings,self).__init__(parent)
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setWindowTitle('Settings')
        self.setGeometry(100,100,640,480)


        denshaSettings=QPushButton('Densha Settings',self)
        denshaSettings.setFixedSize(64,64)
        denshaSettings.setObjectName('Densha Settings')
        denshaSettingsLbl=QLabel('Densha Settings',self)
        denshaSettings.clicked.connect(self.openNewWindow)

        layout.addWidget(denshaSettings,0,0)
        layout.addWidget(denshaSettingsLbl,1,0)


        internetSettings=QPushButton('Internet Settings',self)
        internetSettings.setFixedSize(64,64)
        internetSettingsLbl=QLabel('Internet Settings',self)
        internetSettings.setObjectName('Internet Settings')
        internetSettings.clicked.connect(self.openNewWindow)
        layout.addWidget(internetSettings,0,1)
        layout.addWidget(internetSettingsLbl,1,1)

        layout.setHorizontalSpacing(64)

        
        self.setLayout(layout)


    def openNewWindow(self):
        print('Opening window...')
        if self.sender().objectName()=='Densha Settings':
            print("Densha Settings")
            self.denSet = DenshaSettings()
            self.denSet.show()
            self.hide()
        elif self.sender().objectName()=='Internet Settings':
            print("yes")



class DenshaSettings(QWidget): #DE Settings
    def __init__(self, parent = None):
        
        super(DenshaSettings,self).__init__(parent)
        
        layout = QGridLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setWindowTitle('Densha Settings')
        self.setGeometry(100,100,640,480)

        self.colorTextBox=QLineEdit(self)
        self.colorTextBox.setPlaceholderText('#FFFFFF')
        self.colorTextBox.setMaximumWidth(128)
        
        layout.addWidget(self.colorTextBox,0,0)

        colorTextBoxButton=QPushButton('Apply',self)
        colorTextBoxButton.setMaximumWidth(96)
        colorTextBoxButton.clicked.connect(self.setColor)
        layout.addWidget(colorTextBoxButton,0,1)
    
        self.setLayout(layout)
    
    def setColor(self):
        newColor = self.colorTextBox.text()
        with open(f'/home/{getpass.getuser()}/DenshaExec/DenshaSettings.config','r') as f:
            for line in f:
                if '::bgColor=' in line:
                    oldBgColor=line[10:]
        with open(f'/home/{getpass.getuser()}/DenshaExec/DenshaSettings.config','r+') as f:
            text = f.read()
            text = re.sub(oldBgColor,newColor,text)
            f.seek(0)
            f.write(text)
            f.truncate()
        
                


app = QApplication(sys.argv)
mainWin = Settings()
mainWin.show()

sys.exit(app.exec_())

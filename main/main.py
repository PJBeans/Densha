import sys
import os
import worker
import datetime
import time
import re
import getpass
from subprocess import check_output
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *

getRes = QApplication(sys.argv)
width = getRes.desktop().screenGeometry().width() #Get width of display
height = getRes.desktop().screenGeometry().height() #Get height of display
with open(f'/home/{getpass.getuser()}/DenshaExec/DenshaSettings.config','r') as f:
    for line in f:
        if '::bgColor=' in line:
            bgColor=line[10:]
panelBgColor = "#302f33" #Background for panels, without the semicolon

class SystemMenu(QWidget):
    def __init__(self, parent = None):
        
        super(SystemMenu,self).__init__(parent)
        
        self.setWindowTitle('System Menu')
        self.setGeometry(100,100,240,480)
        self.setStyleSheet(f"background-color: {bgColor};")
        self.setWindowOpacity(.9)
        centerWidth = (width/2)-120
        centerHeight = (height/2)-270
        self.move(centerWidth,centerHeight)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        
        print(width)
        print(height)
        layout = QVBoxLayout()

        label = QLabel('What would you like to do?',self)
        label.setStyleSheet("color: white;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label,False,Qt.AlignTop)
        
        shutdownButton = QPushButton('Shutdown',self)
        shutdownButton.setStyleSheet("color: white;")
        shutdownButton.clicked.connect(self.shutdown)
        layout.addWidget(shutdownButton, False, Qt.AlignCenter)

        restartButton = QPushButton('Restart',self)
        restartButton.setStyleSheet("color: white;")
        restartButton.clicked.connect(self.restart)
        layout.addWidget(restartButton, False, Qt.AlignCenter)

        logoutButton = QPushButton('Log Out',self)
        logoutButton.setStyleSheet("color: white;")
        logoutButton.clicked.connect(self.logout)
        layout.addWidget(logoutButton, False, Qt.AlignCenter)

        cancelButton = QPushButton('Cancel',self)
        cancelButton.setStyleSheet("color: white;")
        cancelButton.clicked.connect(self.closeWindow)
        layout.addWidget(cancelButton, False, Qt.AlignCenter)

        

        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

    def shutdown(self):
        print("Disabled.")
        os.system('shutdown -h now')
    def restart(self):
        print("Disabled.")
        os.system('reboot')
    def logout(self):
        os.system('openbox --exit')

    def closeWindow(self):
        self.close()
    
        

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)
        self.setAttribute(Qt.WA_X11NetWmWindowTypeDock)
        # Worker threads for app name and clock:
        self.obj = worker.Worker()
        self.thread = QThread()
        self.obj.intReady.connect(self.getTime) #Function
        self.obj.intReady.connect(self.getApplicationName)
        self.obj.moveToThread(self.thread)
        self.obj.finished.connect(self.thread.quit)
        self.thread.started.connect(self.obj.procCounter)
        self.thread.start()

        self.setWindowTitle('Densha Desktop')
        self.setGeometry(100,100,width,30)
        self.move(0,0)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setStyleSheet(f"background-color: {panelBgColor};")
        self.setMinimumSize(640,25)
        layout = QHBoxLayout()

        self.lastApp = 'No app'

        #System button
        systemButton= QPushButton('', self)
        systemButton.setIcon(QIcon(f'/usr/share/icons/Densha/64x64/UI/denshaLogo.png'))
        systemButton.setMaximumSize(30,30)
        systemButton.setStyleSheet("color: white;")
        layout.addWidget(systemButton)
        systemButton.clicked.connect(self.systemMenu)
        
        #Application Name
        self.applicationLabel = QPushButton('Application Name',self)
        self.applicationLabel.setMaximumWidth(640)
        self.applicationLabel.setStyleSheet('QPushButton { text-align: left; }')
        self.applicationLabel.setStyleSheet("color: white;")


        
        self.applicationLabel.setContextMenuPolicy(Qt.CustomContextMenu)
        self.applicationLabel.customContextMenuRequested.connect(self.showAppMenu)
        self.appMenu = QMenu(self)
        self.appMenu.setStyleSheet('color: white;')
        quitOption = QAction('Quit',self)
        self.appMenu.addAction(quitOption)
        quitOption.triggered.connect(self.closeApplication)


        self.applicationLabel.clicked.connect(self.showAppMenu)
        layout.addWidget(self.applicationLabel)


        
        #Clock
        
        self.clockLabel = QLabel('XX:XX',self) #Used by functions, hence "self".
        self.clockLabel.setStyleSheet("color: white;")
        self.clockLabel.setMaximumWidth(75)
        layout.addWidget(self.clockLabel,False,Qt.AlignRight)


        """
        self.minimizeButton = QPushButton('M',self)
        self.minimizeButton.setStyleSheet("color: white;")
        self.minimizeButton.setMaximumWidth(30)
        layout.addWidget(self.minimizeButton,False)
        #self.minimizeButton.hide()

        self.restoreButton = QPushButton('R',self)
        self.restoreButton.setStyleSheet("color: white;")
        self.restoreButton.setMaximumWidth(30)
        layout.addWidget(self.restoreButton,False)
        #self.restoreButton.hide()

        self.exitButton = QPushButton('X',self)
        self.exitButton.setStyleSheet("color: white;")
        self.exitButton.setMaximumWidth(30)
        self.exitButton.clicked.connect(self.exitButtonFunc)
        layout.addWidget(self.exitButton,False)
        #self.exitButton.hide()
        """


        layout.setSpacing(20)
        layout.setContentsMargins(0,0,20,0)
        
        self.setLayout(layout)

    def getTime(self):
        fullTime = datetime.datetime.now()
        hour = fullTime.hour
        minute = fullTime.minute
        timeStr = f"{hour}:{minute}"
        self.clockLabel.setText(timeStr)



    def getApplicationName(self):
        try:
            appName = str(check_output('xdotool getactivewindow getwindowname', shell=True))
            appName = appName[2:-3]
            if appName == 'Densha Desktop':
                #print('help')
                self.applicationLabel.setText(self.lastApp)
                self.applicationLabel.setMaximumWidth(len(self.lastApp)*10)
                self.applicationLabel.setStyleSheet('QPushButton { text-align: left; color: white; border: none;}')
            else:

                self.lastApp = appName
                self.applicationLabel.setText(appName)
                self.applicationLabel.setMaximumWidth(len(appName)*10)
                self.applicationLabel.setStyleSheet('QPushButton { text-align: left; color: white; border: none;}')
                #print(f'Last app was {self.lastApp}')
        except:
            print("Invalid app name!")
            self.applicationLabel.setText('Densha Desktop')
            self.applicationLabel.setMaximumWidth(len('Densha Desktop')*10)
            self.applicationLabel.setStyleSheet('QPushButton { text-align: left; color: white; border: none;}')
        
    def showAppMenu(self):
        self.appMenu.exec_(self.applicationLabel.mapToGlobal(QPoint(0,24)))
            
    
    def systemMenu(self):
        self.systemMenuWindow = SystemMenu()
        self.systemMenuWindow.show()

    def exitButtonFunc(self): #Broken
        os.system('xdotool getactivewindow windowclose')
        #Try finding ID after window is maximized, throw it out at restore/minimize, or use it to close window.
        #(Window maximizes....) xdotool getactivewindow windowid
    
    def closeApplication(self):
        try:
            windowID = str(check_output(f'xdotool search --name \'{self.lastApp}\'', shell=True))
            windowID= windowID[2:-3]
            os.system(f'xdotool windowclose {windowID}')
        except:
            print('No app!')
class DesktopWindow(QWidget):
    def __init__(self, parent= None):
        super(DesktopWindow,self).__init__(parent)
        self.move(0,0)
        self.setGeometry(100,100,width,height)
        self.setMaximumSize(width,height)
        self.setMaximumSize(width,height)
        self.setWindowFlag(Qt.WindowStaysOnBottomHint)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle("Densha Desktop")
        self.setAttribute(Qt.WA_TranslucentBackground)

app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())

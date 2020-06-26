#RETURN TO dock.py THIS DOCUMENT IS NOT FINAL

import sys
import os
import datetime
import time
import re
from subprocess import check_output, Popen
import subprocess
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import getpass

getRes = QApplication(sys.argv)
width = getRes.desktop().screenGeometry().width() #Get width of display
height = getRes.desktop().screenGeometry().height() #Get height of display

with open(f'/home/{getpass.getuser()}/DenshaExec/DenshaSettings.config','r') as f:
    for line in f:
        if '::bgColor=' in line:
            bgColor=line[10:]

#bgColor= "#302f33"
themeDir = 'Yaru' #Make this configurable


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow,self).__init__(parent)

        
        

        #QMainWindow.__init__(self)
        self.setAttribute(Qt.WA_X11NetWmWindowTypeDock)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle('Densha Desktop')
        self.setGeometry(100,100,width,64)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        centerWidth = (width/2)-320
        centerHeight = (height/2)-256
        self.move(0,height-64)
        self.setStyleSheet(f"background-color: {bgColor};")

        allApps = QPushButton('All Apps',self)
        allApps.setStyleSheet('color: white;')
        allApps.setFixedSize(64,64)
        allApps.clicked.connect(self.openAllAppsWindow)

    def openAllAppsWindow(self):
        self.allAppsWindow = ApplicationLauncher()
        self.allAppsWindow.show()




#"All Apps" screen.
#TODO:
# - Close window when clicked/tapped outside
# - Use icon for "Close"
# - Colors?
# - Remove unnecessary icons
# - Fix blank icons
class ApplicationLauncher(QScrollArea):
    def __init__(self, parent = None):
        super(ApplicationLauncher,self).__init__(parent)

        QMainWindow.__init__(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowTitle('Densha Desktop')
        self.setGeometry(100,100,(width/2),(height/2))
        centerWidth = (width/2)-(width/4)
        centerHeight = (height/2)-(height/4)
        self.move(centerWidth,centerHeight)
        self.setStyleSheet(f"background-color: {bgColor};")
        self.setWindowOpacity(0.9)
       


        

        self.uname = getpass.getuser()
        self.appDict = {}
        self.appLabels = {}
        self.appExecutions = {}

        #This should be changed sometimes to more flexibly add or remove directories.
        print("Finding applications...")
        appList = os.listdir('/usr/share/applications') #Most apps
        appList2 = os.listdir(f'/home/{self.uname}/.local/share/applications') #"User's" Apps
        appList3 = os.listdir('/var/lib/snapd/desktop/applications') #Snaps


        self.xLocation = 0
        self.yLocation = 1
        self.rows =0
        self.pages =0
        widget = QWidget()
        self.layout = QGridLayout(widget)
        self.layout.setHorizontalSpacing(45)
        self.layout.setAlignment(Qt.AlignCenter)
        exitButton=QPushButton('Close',self)
        exitButton.setStyleSheet('color: white;')
        exitButton.setMaximumSize(68,30)
        exitButton.clicked.connect(self.closeWindow)
        self.layout.addWidget(exitButton,0,4)
        noDisplayTag = False

        #/usr/share/applications
        for i in range (0,len(appList)):
            noDisplayTag = False
            if os.path.isfile(f'/usr/share/applications/{appList[i]}'):
                with open(f'/usr/share/applications/{appList[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Name=" in line:
                            line = line[5:]
                            #print(f"Name: {line}")
                            self.name=line
                            break
                with open(f'/usr/share/applications/{appList[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Exec=" in line:
                            line = line[5:]
                            #print(f"Exec: {line}")
                            self.execPath=line
                            break
                with open(f'/usr/share/applications/{appList[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Icon=" in line:
                            line = line[5:]
                            #print(f"Icon: {line}")
                            self.icon=line
                            break
                with open(f'/usr/share/applications/{appList[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "NotShowIn=" in line or "NoDisplay=" in line:
                            noDisplayTag=True
                            break
                
                
                if noDisplayTag==False:
                    self.createButton(i)
        #~/.local/share/applications
        for i in range (0,len(appList2)):
            noDisplayTag=False
            if os.path.isfile(f'/home/{self.uname}/.local/share/applications/{appList2[i]}'):
                with open(f'/home/{self.uname}/.local/share/applications/{appList2[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Name=" in line:
                            line = line[5:]
                            #print(f"Name: {line}")
                            self.name=line
                            break
                with open(f'/home/{self.uname}/.local/share/applications/{appList2[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Exec=" in line:
                            line = line[5:]
                            #print(f"Exec: {line}")
                            self.execPath=line
                            break
                with open(f'/home/{self.uname}/.local/share/applications/{appList2[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Icon=" in line:
                            line = line[5:]
                            #print(f"Icon: {line}")
                            self.icon=line
                            break
                with open(f'/home/{self.uname}/.local/share/applications/{appList2[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "NotShowIn=" in line or "NoDisplay=" in line:
                            noDisplayTag=True
                            break
                
                if noDisplayTag == False:
                    self.createButton(i)
        
        #/var/lib/snapd/desktop/applications  <<<Modified from first two algorithms>>>
        for i in range (0,len(appList3)):
            noDisplayTag=False
            if os.path.isfile(f'/var/lib/snapd/desktop/applications/{appList3[i]}'):
                with open(f'/var/lib/snapd/desktop/applications/{appList3[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if re.search('^Name=',line):
                            line = line[5:]
                            #print(f"Name: {line}")
                            self.name=line
                            break
                with open(f'/var/lib/snapd/desktop/applications/{appList3[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Exec=" in line:
                            truncate = re.search('/snap/bin',line)
                            truncate = truncate.start()
                            line = line[truncate:]
                            #print(f"Exec: {line}")
                            self.execPath=line
                            break
                with open(f'/var/lib/snapd/desktop/applications/{appList3[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "Icon=" in line:
                            line = line[5:]
                            #print(f"Icon: {line}")
                            self.icon=line
                            break
                with open(f'/var/lib/snapd/desktop/applications/{appList3[i]}','r') as f:
                    for line in f:
                        line = line.rstrip()
                        if "NotShowIn=" in line or "NoDisplay=" in line:
                            noDisplayTag=True
                            break
                
                if noDisplayTag == False:
                    self.createButton(i)
   
                    

                    


                    


        self.setWidget(widget)
        self.setWidgetResizable(True)
    def openProgram(self):
        args = ''

        cmd = self.appExecutions[self.sender().objectName()].rstrip()
        if "ec=" in cmd: #Remove prefix to launch some apps
            cmd=cmd[3:]
        if "%u" in cmd or "%U" in cmd or "%f" in cmd or "%F" in cmd: #Remove suffixes to launch some apps
            print("Found arg to remove")
            cmd=cmd[:-3]
        if ' ' in cmd: #Find launch arguments.
            argStart = re.search(' ', cmd)
            argStart = argStart.start()
            args = cmd[argStart:].strip()
            cmd = cmd[:argStart].strip()

        quoteCount=cmd.count('"') #Some .desktop files specify paths with quotes. Removes them.
        if quoteCount==2:
            cmd=cmd[1:-1]
        elif quoteCount ==1:
            if cmd[0] == '"':
                cmd=cmd[1:]
            elif cmd[-1] == '"':
                cmd=cmd[:-1]
        print([cmd,args])
        Popen([cmd,args])
        self.closeWindow()
        

    def closeWindow(self):
        print(self.appDict[30].objectName())
        self.close()
    
    def createButton(self,number):
        #Execution path
        self.appExecutions[self.name] = self.execPath
        self.appDict[number] = QPushButton('',self)
        self.appLabels[number] = QLabel(self.name,self)
        self.appLabels[number].setFont(QFont('Arial', 8.5))
        self.appLabels[number].setMaximumWidth(64)
        self.appLabels[number].setWordWrap(True)
        self.appLabels[number].setStyleSheet("color: white;")
        self.appLabels[number].setAlignment(Qt.AlignCenter)
        self.appLabels[number].adjustSize()
        self.appDict[number].setObjectName(self.name)
        self.appDict[number].setFixedSize(64,64)
        self.appDict[number].setMaximumSize(68,68)
        self.appDict[number].setStyleSheet('border: none;')
        if ".png" in self.icon and '/' not in self.icon[0]:
            print("Has .png!")
            self.icon = self.icon[:-4]
            print(f"Is now {self.icon}")
        elif ".svg" in self.icon:
            print("Has .svg!")
            self.icon = self.icon[:-4]
            print(f"Is now {self.icon}")


        #Searches the user's theme if possible, hicolor, pixmaps, and adwaita for icons.

        #User theme
        if os.path.isfile(f'{self.icon}'):
            self.appDict[number].setIcon(QIcon(f'{self.icon}'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/scalable/mimetypes/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/scalable/mimetypes/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/scalable/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/scalable/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/1024x1024/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/1024x1024/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/512x512/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/512x512/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/256x256/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/256x256/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/192x192/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/192x192/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/128x128/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/128x128/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/96x96/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/96x96/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/72x72/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/72x72/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/64x64/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/64x64/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/48x48/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/48x48/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/36x36/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/36x36/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/32x32/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/32x32/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/24x24/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/24x24/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/22x22/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/22x22/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/16x16/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/16x16/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/pixmaps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/pixmaps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/pixmaps/{self.icon}.xpm'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/pixmaps/{self.icon}.xpm'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/{themeDir}/symbolic/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/{themeDir}/symbolic/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")

        #Hicolor
        elif os.path.isfile(f'{self.icon}'):
            self.appDict[number].setIcon(QIcon(f'{self.icon}'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/scalable/mimetypes/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/scalable/mimetypes/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/scalable/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/scalable/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/1024x1024/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/1024x1024/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/512x512/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/512x512/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/256x256/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/256x256/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/192x192/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/192x192/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/128x128/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/128x128/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/96x96/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/96x96/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/72x72/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/72x72/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/64x64/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/64x64/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/48x48/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/48x48/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/36x36/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/36x36/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/32x32/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/32x32/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/24x24/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/24x24/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/22x22/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/22x22/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/16x16/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/16x16/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/pixmaps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/pixmaps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/pixmaps/{self.icon}.xpm'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/pixmaps/{self.icon}.xpm'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/hicolor/symbolic/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/hicolor/symbolic/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")

        #Adwatia - For GNOME Apps
        elif os.path.isfile(f'/usr/share/icons/gnome/scalable/mimetypes/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/scalable/mimetypes/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/scalable/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/scalable/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/512x512/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/512x512/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/256x256/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/256x256/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/192x192/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/192x192/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/128x128/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/128x128/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/96x96/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/96x96/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/72x72/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/72x72/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/64x64/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/64x64/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/48x48/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/48x48/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/36x36/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/36x36/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/32x32/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/32x32/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/24x24/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/24x24/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/22x22/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/22x22/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/16x16/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/16x16/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        
        #Adwatia - "Devices" icons
        elif os.path.isfile(f'/usr/share/icons/gnome/256x256/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/256x256/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/192x192/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/192x192/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/128x128/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/128x128/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/96x96/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/96x96/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/72x72/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/72x72/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/64x64/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/64x64/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/48x48/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/48x48/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/36x36/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/36x36/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/32x32/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/32x32/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/24x24/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/24x24/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/22x22/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/22x22/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/icons/gnome/16x16/devices/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/gnome/16x16/devices/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")

        #Hicolor .local icons:
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/scalable/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/scalable/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/1024x1024/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/1024x1024/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/512x512/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/512x512/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/256x256/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/256x256/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/192x192/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/192x192/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/128x128/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/128x128/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/96x96/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/96x96/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/72x72/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/72x72/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/64x64/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/64x64/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/48x48/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/48x48/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/36x36/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/36x36/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/32x32/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/32x32/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/24x24/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/24x24/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/22x22/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/22x22/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/16x16/apps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/16x16/apps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/pixmaps/{self.icon}.png'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/pixmaps/{self.icon}.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/usr/share/pixmaps/{self.icon}.xpm'):
            self.appDict[number].setIcon(QIcon(f'/usr/share/pixmaps/{self.icon}.xpm'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        elif os.path.isfile(f'/home/{self.uname}/.local/share/icons/hicolor/symbolic/apps/{self.icon}.svg'):
            self.appDict[number].setIcon(QIcon(f'/home/{self.uname}/.local/share/icons/hicolor/symbolic/apps/{self.icon}.svg'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"found {self.icon}")
        else:
            self.appDict[number].setIcon(QIcon(f'/usr/share/icons/Densha/64x64/UI/noIcon.png'))
            self.appDict[number].setIconSize(QSize(64,64))
            print(f"Coudln't find, {self.icon} using default.")


        self.layout.addWidget(self.appDict[number],self.yLocation,self.xLocation)
        self.layout.addWidget(self.appLabels[number],self.yLocation+1,self.xLocation)
        self.xLocation += 1
        
        if self.xLocation ==5:
            self.xLocation=0
            self.yLocation+=2
        self.appDict[number].clicked.connect(self.openProgram)

app = QApplication(sys.argv)
mainWin = MainWindow()
mainWin.show()
sys.exit(app.exec_())
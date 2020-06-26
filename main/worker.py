# worker.py
# Based on code by Raiden Core on Stackoverflow.
#Optimize so that clock is based on seconds/minute, and app names are instant
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)


    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        counter = 0
        while True:
            time.sleep(.1)
            counter += 1
            self.intReady.emit(counter)
            #print("yes")

        self.finished.emit()

#Stock code, for reference:
"""
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(int)


    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        for i in range(1, 100):
            time.sleep(1)
            self.intReady.emit(i)

        self.finished.emit()
"""
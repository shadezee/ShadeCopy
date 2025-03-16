from PyQt5.QtCore import QThread, pyqtSignal
from watchfiles import Change, watch
from shutil import copy2
from time import sleep
from os import path

class ShadeCopyWorker(QThread):
  statusSignal = pyqtSignal(str)
  errorSignal = pyqtSignal(str)

  def __init__(self, pathToMonitor, fileName, copyTo):
    super().__init__()
    self.pathToMonitor = pathToMonitor
    self.fileName = fileName
    self.copyTo = copyTo

  def run(self):
    i = 0
    try:
      for changes in watch(self.pathToMonitor):
        for changeType, file in changes:
          file = path.normpath(file)
          if not changeType == Change.deleted and path.basename(file) == self.fileName:
            sleep(2)
            i += 1
            copy2(file, self.copyTo)
            self.statusSignal.emit(f'{i}. {self.fileName} copied.\n')
    except Exception as e:
      self.errorSignal.emit(f'\n\nAn error occurred.\n{e}\n')

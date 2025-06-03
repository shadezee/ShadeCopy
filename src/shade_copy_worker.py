from shutil import copy2
from time import sleep
from os import path
from PyQt5.QtCore import QThread, pyqtSignal
from watchfiles import Change, watch


class ShadeCopyWorker(QThread):
  statusSignal = pyqtSignal(str)
  errorSignal = pyqtSignal(str)

  def __init__(self, pathToMonitor, fileName, copyTo):
    super().__init__()
    self.pathToMonitor = path.normpath(pathToMonitor)
    self.fileName = fileName
    self.copyTo = path.normpath(copyTo)

  def run(self):
    i = 0
    while True:
      try:
        if path.exists(self.pathToMonitor):
          for changes in watch(self.pathToMonitor):
            for changeType, file in changes:
              file = path.normpath(file)

              if self.copyTo in file:
                continue

              if not changeType == Change.deleted and path.basename(file) == self.fileName:
                sleep(2)
                i += 1
                copy2(path.join(self.pathToMonitor, self.fileName), self.copyTo)
                self.statusSignal.emit(f'{i}. {self.fileName} copied.\n')
      except FileNotFoundError:
        i -= 1
        self.statusSignal.emit(
          f'Cannot find {self.pathToMonitor}.\n'
          f'Resuming operations in 5 seconds if it is found again.\n\n'
        )
        sleep(5)
        continue
      except Exception as e:
        self.errorSignal.emit(f'\n\nAn error occurred.\n{str(e)}\n')

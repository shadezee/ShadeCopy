from PyQt5.QtWidgets import (
  QApplication,
  QMainWindow,
  QVBoxLayout,
  QWidget,
  QLabel,
  QPushButton,
  QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
from os import path
from watchfiles import Change, watch
from shutil import copy2
from time import sleep

class ShadeCopyWorker(QThread):
  statusSignal = pyqtSignal(str)
  errorSignal = pyqtSignal(str)

  def __init__(self, fileToMonitor, copyTo):
    super().__init__()
    self.fileToMonitor = fileToMonitor
    self.copyTo = copyTo
    print(f'Copying {fileToMonitor} to {copyTo}')

  def run(self):
    i = 0
    try:
      for changes in watch(self.fileToMonitor):
        for changeType, _ in changes:
          if changeType in (Change.added, Change.modified):
            sleep(2)
            i += 1
            copy2(self.fileToMonitor, self.copyTo)
            self.statusSignal.emit(f'{i}. {self.fileToMonitor} copied.')
    except Exception as e:
      self.errorSignal.emit(f'An error occurred.\n{e}')

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Shade Copy')
    iconPath = path.join(path.dirname(__file__), 'assets', 'icon.ico')
    self.setWindowIcon(QIcon(iconPath))
    self.setFixedSize(450, 250)

    layout = QVBoxLayout()

    self.fileLabel = QLabel('No file selected.')
    self.dirLabel = QLabel('No directory selected.')
    self.status = QLabel()

    self.fileButton = QPushButton('Select a file...')
    self.fileButton.clicked.connect(self.select_file)

    self.dirButton = QPushButton('Select a directory...')
    self.dirButton.clicked.connect(self.select_directory)

    self.startButton = QPushButton('Start')
    self.startButton.clicked.connect(self.begin)

    layout.addWidget(self.fileLabel)
    layout.addWidget(self.fileButton)
    layout.addWidget(self.dirLabel)
    layout.addWidget(self.dirButton)
    layout.addWidget(self.startButton)
    layout.addWidget(self.status)

    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

  def select_file(self):
    file, _ = QFileDialog.getOpenFileName(self, 'Select File')
    if file:
      self.fileToMonitor = file
      self.fileLabel.setText(f'Selected File: {path.basename(file)}')

  def select_directory(self):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.copyTo = folder
      self.dirLabel.setText(f'Destination Folder: {folder}')

  def reset_fields(self):
    self.fileLabel.setText('No file selected.')
    self.dirLabel.setText('No directory selected.')
    self.fileToMonitor = None
    self.copyTo = None

  def error_handler(self, message):
    self.status.setText(message)
    self.reset_fields()
    self.shade_watcher.terminate()

  def update_status(self, message):
    self.status.setText(message)

  def begin(self):
    if not self.fileToMonitor or not self.copyTo:
      return
    self.status.setText('Watching...')
    copyTo = f'{self.copyTo}/{path.basename(self.fileToMonitor)}'
    self.shade_watcher = ShadeCopyWorker(self.fileToMonitor, copyTo)
    self.shade_watcher.statusSignal.connect(self.update_status)
    self.shade_watcher.errorSignal.connect(self.error_handler)
    self.shade_watcher.start()

if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec()

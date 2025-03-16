from PyQt5 import uic
from PyQt5.QtWidgets import (
  QApplication,
  QMainWindow,
  QListWidgetItem,
  QFileDialog
)
from os import path, listdir
from shade_copy_worker import ShadeCopyWorker
from assets.shade_copy_ui import Ui_mainWindow

class MainWindow(QMainWindow, Ui_mainWindow):
  # buttons --> retainButton, recallButton, watchButton
  # labels acting as buttons --> selectFileDir, selectDirectory
  # display label --> display
  # List view --> fileListView

  def __init__(self):
    super().__init__()
    self.setupUi(self)

    self.selectFileDir.mousePressEvent = self.select_file_dir
    self.selectDirectory.mousePressEvent = self.select_directory
    self.watchButton.clicked.connect(self.begin)

    self.status = False
    self.copyTo = None
    self.pathToMonitor = None

  def select_file_dir(self, event):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.pathToMonitor = folder
      directoryFiles = listdir(folder)
      for file in directoryFiles:
        if not path.isfile(file):
          directoryFiles.remove(file)
      self.populate_file_selection(directoryFiles)

  def populate_file_selection(self, directoryFiles):
    self.fileListView.clear()
    for f in directoryFiles:
      QListWidgetItem(f, self.fileListView)
    self.fileListView.setCurrentRow(0)

  def reset_fields(self, error=False):
    if error:
      self.fileListView.clear()
      self.fileToMonitor = None
      self.copyTo = None
      self.selectDirectory.setText('Select Directory')

    self.status = False
    self.shade_watcher.terminate()
    self.update_status('\nTerminated watching...')

  def error_handler(self, message):
    self.display.setText(message)
    self.reset_fields(True)

  def select_directory(self, event):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.copyTo = folder
      folder_parts = folder.split('/')

      if len(folder_parts) > 3:
        path_str = "/".join(folder_parts[-3:])
        self.selectDirectory.setText(f'Destination Folder: {path_str}')
      else:
        self.selectDirectory.setText(f'Destination Folder: {folder}')

  def update_status(self, message):
    self.display.setText(f'{self.display.text()}{message}')

  def begin(self):
    if self.status:
      self.reset_fields()
      return

    fileItem = self.fileListView.currentItem()
    if not fileItem:
      return

    fileName = fileItem.text()
    if fileName and self.copyTo:
      self.display.setText(f'Watching {fileName}...')
      copyTo = f'{self.copyTo}/{fileName}'
      self.shade_watcher = ShadeCopyWorker(self.pathToMonitor, fileName, copyTo)
      self.shade_watcher.statusSignal.connect(self.update_status)
      self.shade_watcher.errorSignal.connect(self.error_handler)
      self.status = True
      self.shade_watcher.start()

if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec()

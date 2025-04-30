from os import path, listdir
from PyQt5.QtWidgets import (
  QApplication,
  QMainWindow,
  QListWidgetItem,
  QFileDialog
)
from PyQt5.QtCore import Qt
from src.storage import Storage
from src.shade_copy_worker import ShadeCopyWorker
from assets.shade_copy_ui import Ui_mainWindow

class MainWindow(QMainWindow, Ui_mainWindow):
  # buttons --> recallButton, retainButton, watchButton
  # labels acting as buttons --> selectFileDir, selectDirectory
  # display text edit --> display
  # list view --> fileListView

  def __init__(self):
    super().__init__()
    self.setupUi(self)

    self.selectFileDir.mousePressEvent = self.select_file_dir
    self.selectDirectory.mousePressEvent = self.select_directory
    self.watchButton.clicked.connect(self.begin)

    self.fileToMonitor = None
    self.shadeWatcher = None
    self.status = False
    self.copyTo = None
    self.pathToMonitor = None
    self.storage = Storage()

  # pylint: disable-next=unused-argument
  def select_file_dir(self, event):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.pathToMonitor = folder
      directoryFiles = listdir(folder)
      filteredFiles = []

      for file in directoryFiles:
        if path.isfile(path.join(folder, file)):
          filteredFiles.append(file)

      self.populate_file_selection(filteredFiles)

  def populate_file_selection(self, filteredFiles):
    self.fileListView.clear()
    for f in filteredFiles:
      QListWidgetItem(f, self.fileListView)
    self.fileListView.setCurrentRow(0)

  def reset_fields(self, error=False):
    if error:
      self.fileListView.clear()
      self.fileToMonitor = None
      self.copyTo = None
      self.selectDirectory.setText('Select Directory')

    self.status = False
    self.shadeWatcher.terminate()
    self.update_status('\nTerminated watching...\n')

  def error_handler(self, message):
    self.display.setText(message)
    self.reset_fields(True)

  # pylint: disable-next=unused-argument
  def select_directory(self, event):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.copyTo = folder
      folderParts = folder.split('/')

      if len(folderParts) > 3:
        pathStr = "/".join(folderParts[-3:])
        self.selectDirectory.setText(f'Destination Folder: {pathStr}')
      else:
        self.selectDirectory.setText(f'Destination Folder: {folder}')

  def update_status(self, message):
    self.display.setText(f'{self.display.toPlainText()}{message}')
    self.display.selectAll()
    self.display.setAlignment(Qt.AlignCenter)

  def begin(self):
    if self.status:
      self.reset_fields()
      return

    fileItem = self.fileListView.currentItem()
    if not fileItem:
      return

    fileName = fileItem.text()
    if fileName and self.copyTo:
      self.update_status(f'Watching {fileName}...\n\n')
      copyTo = f'{self.copyTo}/{fileName}'
      self.shadeWatcher = ShadeCopyWorker(self.pathToMonitor, fileName, copyTo)
      self.shadeWatcher.statusSignal.connect(self.update_status)
      self.shadeWatcher.errorSignal.connect(self.error_handler)
      self.status = True
      self.shadeWatcher.start()

if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec()

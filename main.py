from os import path, listdir
from PyQt5.QtWidgets import (
  QApplication,
  QMainWindow,
  QListWidgetItem,
  QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from src.storage import Storage
from src.shade_copy_worker import ShadeCopyWorker
from src.errors import Errors
from assets.shade_copy_ui import Ui_mainWindow
# pylint: disable-next=unused-import
import assets.resources


class MainWindow(QMainWindow, Ui_mainWindow):
  # buttons --> recallButton, retainButton, watchButton
  # labels acting as buttons --> selectFileDir, selectDirectory
  # display text edit --> display
  # list view --> fileListView

  def __init__(self):
    super().__init__()
    self.setupUi(self)
    self.setWindowIcon(QIcon(':/icon.ico'))

    self.selectFileDir.mousePressEvent = self.select_file_dir
    self.selectDirectory.mousePressEvent = self.select_directory
    self.watchButton.clicked.connect(self.begin)
    self.retainButton.clicked.connect(self.retain)
    self.recallButton.clicked.connect(self.recall)

    self.fileToMonitor = None
    self.shadeWatcher = None
    self.status = False
    self.copyTo = None
    self.pathToMonitor = None
    self.storage = Storage(parent=self)

  # pylint: disable-next=unused-argument
  def select_file_dir(self, event):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.set_fields(pathToMonitor=folder)
      self.populate_file_selection(self.pathToMonitor)

  def populate_file_selection(self, folder, fileName=None):
    self.fileListView.clear()
    directoryFiles = listdir(folder)
    filteredFiles = []

    for file in directoryFiles:
      if path.isfile(path.join(folder, file)):
        filteredFiles.append(file)
    for f in filteredFiles:
      QListWidgetItem(f, self.fileListView)
    if fileName:
      items = self.fileListView.findItems(fileName, Qt.MatchExactly)
      self.fileListView.setCurrentItem(items[0])
    else:
      self.fileListView.setCurrentRow(0)

  def set_fields(self,
                pathToMonitor=None,
                copyTo=None,
                fileName=None,
                refreshFileSelection=False
                ):
    if copyTo:
      self.copyTo = copyTo
      self.set_dir_label_path(copyTo)
    if pathToMonitor:
      self.pathToMonitor = pathToMonitor
    if refreshFileSelection:
      self.populate_file_selection(self.pathToMonitor, fileName)

  def reset_fields(self, error=False):
    if error:
      self.fileListView.clear()
      self.pathToMonitor = None
      self.copyTo = None
      self.selectDirectory.setText('Select Directory')

    self.status = False
    self.recallButton.setEnabled(True)
    self.retainButton.setEnabled(True)
    self.shadeWatcher.terminate()
    self.update_status('\nTerminated watching...\n')

  def error_handler(self, message):
    self.display.setText(message)
    self.reset_fields(True)

  # pylint: disable-next=unused-argument
  def select_directory(self, event):
    folder = QFileDialog.getExistingDirectory(self, 'Select Destination Folder')
    if folder:
      self.set_fields(copyTo=folder)
      self.set_dir_label_path(folder)

  def set_dir_label_path(self, folder):
    folderParts = folder.split('/')

    if len(folderParts) > 3:
      pathStr = "/".join(folderParts[-3:])
      self.selectDirectory.setText(f'Destination Folder: {pathStr}')
    else:
      self.selectDirectory.setText(f'Destination Folder: {folder}')

  def retain(self):
    fileItem = self.fileListView.currentItem()
    if self.copyTo and fileItem:
      self.storage.retain(self.pathToMonitor, fileItem.text(), self.copyTo)
    else:
      Errors.raise_error(self,
                        errorType='NOTHING_TO_RETAIN_ERROR',
                        errorLevel='INFORMATION'
                        )

  def recall(self):
    if not self.storage.display():
      Errors.raise_error(self,
                        errorType='EMPTY_STORAGE_ERROR',
                        errorLevel='INFORMATION'
                        )

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
      Errors.raise_error(self,
                        errorType='NO_FILE_SELECTED_ERROR',
                        errorLevel='INFORMATION'
                        )
      return

    fileName = fileItem.text()
    if not self.copyTo:
      Errors.raise_error(self,
                        errorType='NO_DESTINATION_FOLDER_ERROR',
                        errorLevel='INFORMATION'
                        )
      return

    if self.pathToMonitor == self.copyTo:
      Errors.raise_error(self,
                        errorType='SOURCE_AND_DESTINATION_SAME_ERROR',
                        errorLevel='INFORMATION'
                        )
      return

    self.update_status(f'Watching {fileName}...\n\n')
    copyTo = f'{self.copyTo}/{fileName}'
    self.shadeWatcher = ShadeCopyWorker(self.pathToMonitor, fileName, copyTo)
    self.shadeWatcher.statusSignal.connect(self.update_status)
    self.shadeWatcher.errorSignal.connect(self.error_handler)
    self.status = True
    self.recallButton.setEnabled(False)
    self.retainButton.setEnabled(False)
    self.shadeWatcher.start()

if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  window.show()
  app.exec()

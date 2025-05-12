from os import path
from PyQt5.QtWidgets import (
  QDialog,
  QHeaderView
)
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from assets.storage_ui import Ui_storageScreen
from src.db_ops import DbOps
# pylint: disable-next=unused-import
import assets.resources


class Storage(QDialog, Ui_storageScreen):
  # buttons --> recallButton, removeButton
  # display --> storageView, helperLabel

  def __init__(self, parent=None):
    super(Storage, self).__init__(parent)
    self.setupUi(self)
    self.setWindowIcon(QIcon(':/icon.ico'))

    self.model = QStandardItemModel(self.storageView)
    self.model.setHorizontalHeaderLabels(['File Path', 'Directory Path', 'File Name'])
    self.storageView.resizeColumnsToContents()
    self.storageView.entered.connect(self.update_helper_label)

    header = self.storageView.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Interactive)

    self.database = DbOps()
    self.recallButton.clicked.connect(self.recall)
    self.removeButton.clicked.connect(self.remove)

  def shorten_path(self, location):
    parts = location.split('/')
    return "/".join(parts[-3:]) if len(parts) > 3 else location

  def adjust_view(self):
    self.storageView.resizeColumnsToContents()
    for col in range(self.model.columnCount()):
      if self.storageView.columnWidth(col) > 300:
        self.storageView.setColumnWidth(col, 300)

    self.storageView.setWordWrap(False)
    self.storageView.setTextElideMode(Qt.ElideMiddle)
    self.storageView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.storageView.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    self.show()

  def update_helper_label(self, index):
    if index.isValid():
      item = self.model.itemFromIndex(index)
      data = item.data()
      if isinstance(data, dict):
        col = index.column()
        if col == 0:
          text = data.get('filePath', '')
        elif col == 1:
          text = data.get('directoryPath', '')
        elif col == 2:
          text = data.get('fileName', '')
        else:
          text = ''
        self.helperLabel.setText(text)
      else:
        self.helperLabel.setText(item.text())
    else:
      self.helperLabel.clear()

  def display(self):
    data = self.database.select()
    self.model.setRowCount(0)

    for row in data:
      dataId, filePath, directoryPath, fileName = row

      items = [
          QStandardItem(self.shorten_path(filePath)),
          QStandardItem(self.shorten_path(directoryPath)),
          QStandardItem(fileName)
      ]
      for item in items:
        item.setData({
          'dataId': dataId,
          'filePath': filePath,
          'directoryPath': directoryPath,
          'fileName': fileName
        })
      self.model.appendRow(items)

    self.storageView.setModel(self.model)
    self.adjust_view()

  def retain(self, filePath, fileName, directoryPath):
    success = self.database.save(filePath, fileName, directoryPath)
    if not success:
      # raise error in popup
      pass
    return success

  def recall(self):
    index = self.storageView.selectedIndexes()
    if index:
      item = self.model.itemFromIndex(index[0])
      dataId = item.data().get('dataId')
      pathToMonitor = item.data().get('filePath')
      directoryPath = item.data().get('directoryPath')
      fileName = item.data().get('fileName')

      if path.exists(directoryPath) and path.isfile(path.join(pathToMonitor, fileName)):
        self.parent().set_fields(pathToMonitor, directoryPath, fileName, True)
      else:
        success = self.database.delete(dataId)
        if success:
          self.display()
        # raise error in popup
      self.close()

  def remove(self):
    index = self.storageView.selectedIndexes()
    if index:
      item = self.model.itemFromIndex(index[0])
      dataId = item.data().get('dataId')
      success = self.database.delete(dataId)
      if success:
        self.display()

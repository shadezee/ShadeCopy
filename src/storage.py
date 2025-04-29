from PyQt5.QtWidgets import (
  QWidget,
)
from assets.storage_ui import Ui_storageScreen

class Storage(QWidget, Ui_storageScreen):
  def __init__(self, parent=None):
    super(Storage, self).__init__(parent)
    self.setupUi(self)

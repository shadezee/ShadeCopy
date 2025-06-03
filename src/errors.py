
from PyQt5.QtWidgets import (
  QMessageBox
)

class ErrorConstants:
  TITLES = {
    'STANDARD_ERROR_TITLE' : 'Error',
    'STORAGE_ERROR_TITLE' : 'Database Error'
  }

  MESSAGES = {
    'STANDARD_ERROR' : 'An error occurred.',
    'NO_FILE_SELECTED_ERROR' : 'No file selected.',
    'NO_DESTINATION_FOLDER_ERROR' : 'No destination folder selected.',
    'SOURCE_AND_DESTINATION_SAME_ERROR' : 'Source and destination folders must be different.',
    'NOTHING_TO_RECALL_ERROR' : 'No saved paths to recall.',
    'NOTHING_TO_RETAIN_ERROR' : 'Nothing selected to retain.',
    'STORAGE_ERROR' : 'Database could not be initialized.\nPlease restart.',
    'EMPTY_STORAGE_ERROR' : 'Nothing stored to recall.',
    'RETAIN_ERROR' : 'Error saving file-directory pair.',
    'RECALL_ERROR' : 'Selected paths do not exist anymore and will be deleted.',
    'SELECTION_ERROR' : 'Error selecting data.',
    'INSERTION_ERROR' : 'Error saving data.',
    'DELETION_ERROR' : 'Error deleting data.'
  }

class Errors:
  @staticmethod
  def raise_error(
                  parent,
                  title='STANDARD_ERROR_TITLE',
                  errorType='STANDARD_ERROR',
                  errorLevel='CRITICAL'
                  ):
    print(f'Error: {title} - {errorType}')
    title = ErrorConstants.TITLES.get(title)
    message = ErrorConstants.MESSAGES.get(errorType)

    if errorLevel == 'CRITICAL':
      QMessageBox.critical(parent, title, message)
    elif errorLevel == 'WARNING':
      QMessageBox.warning(parent, title, message)
    elif errorLevel == 'INFORMATION':
      QMessageBox.information(parent, title, message)

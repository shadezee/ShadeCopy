import sqlite3 as sql
from os import path, makedirs
from src.errors import Errors


class DbOps:
  def __init__(self):
    self.create_connection()
    self.connection = None
    self.cursor = None

    if not self.create_table():
      Errors.raise_error(self,
                        title='STORAGE_ERROR_TITLE',
                        errorType='STORAGE_ERROR'
                        )

  def create_connection(self):
    dbDirectory = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'storage')
    makedirs(dbDirectory, exist_ok=True)
    self.dbDirectory = path.join(dbDirectory, 'storage.db')

    self.connection = sql.connect(self.dbDirectory)
    self.cursor = self.connection.cursor()

  def close_connection(self):
    if self.connection:
      self.connection.close()
      self.cursor = None

  def save(self, filePath, fileName, directoryPath):
    try:
      self.create_connection()
      query = '''
                  INSERT OR
                  IGNORE INTO
                        data (
                              file_path,
                              file_name,
                              directory_path
                        )
                  VALUES (?, ?, ?)
      '''
      self.cursor.execute(query, (filePath, fileName, directoryPath))
      self.connection.commit()
    except Exception:
      Errors.raise_error(self,
                        title='STORAGE_ERROR_TITLE',
                        errorType='INSERTION_ERROR'
                        )
      return False
    return True

  def delete(self, dataId):
    try:
      self.create_connection()
      query = 'DELETE FROM data WHERE id = ?'
      self.cursor.execute(query, (dataId,))
      self.connection.commit()
    except Exception:
      Errors.raise_error(self,
                        title='STORAGE_ERROR_TITLE',
                        errorType='DELETION_ERROR'
                        )
      return False
    finally:
      self.close_connection()
    return True

  def select(self):
    rows = None
    try:
      self.create_connection()
      query = '''SELECT
                      id,
                      file_path,
                      directory_path,
                      file_name
                FROM data
              '''
      rows = self.cursor.execute(query).fetchall()
    except Exception:
      Errors.raise_error(self,
                        title='STORAGE_ERROR_TITLE',
                        errorType='SELECTION_ERROR'
                        )
      return None
    finally:
      self.close_connection()

    return rows

  def create_table(self):
    try:
      self.create_connection()
      query = '''
                CREATE TABLE
                IF NOT EXISTS
                      data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            file_path TEXT,
                            directory_path TEXT,
                            file_name TEXT,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            UNIQUE (file_path, directory_path, file_name)
                      );
              '''
      self.cursor.execute(query)
      self.connection.commit()
    except Exception:
      Errors.raise_error(self,
                        title='STORAGE_ERROR_TITLE',
                        errorType='STORAGE_ERROR'
                        )
      return False
    finally:
      self.close_connection()
    return True

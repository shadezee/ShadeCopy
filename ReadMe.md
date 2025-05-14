<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/shadezee/ShadeCopy">
    <img src="./assets/icon.ico" alt="Logo" width="250" height="250">
  </a>

  <h3 align="center">Shade Copy</h3>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project
A lightweight PyQt5-based desktop utility that monitors a selected file for changes and automatically copies updated versions to a destination folder. Designed for users who want to back up or track file changes in real-time with a simple, intuitive UI.

<br>

## Why it was built
While learning Java Servlets in VSCode, I found it tedious to manually copy the .war file to the deployment directory every time I rebuilt the project. So, I created Shade Copy to automate that task and help streamline the workflow.

### Built With
[![Python][Python.com]][Python-url] [![Qt][Qt.com]][Qt-url] [![SQLite][SQLite-badge]][SQLite-url]

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

- Python 3.7+
- pip installer
- Qt Designer *(optional, but recommended if you want to edit the UI)*

### Installation
  #### 1. Clone the repository
  ```
    git clone https://github.com/shadezee/ShadeCopy.git
  ```

  #### 2. Create a virtual environment
  ```
    python -m venv .venv
  ```

  #### 3. Activate the virtual environment
  ```
    # Windows
    python -m venv .venv

    # macOS/Linux
    source .venv/bin/activate
  ```

  #### 4. Install dependencies
  ```
    pip install -r requirements.txt
  ```

## Usage
  #### 1. Launch
  ```
    python main.py
  ```

  #### 2. UI Options
  - Select the directory to monitor and the destination folder.
  - Choose a file from the list and start watching.
  - Use `Retain` to save file-directory pairs.
  - Use `Recall` to reload saved paths.

  #### 3. Development tools
  - To convert modified .ui files into Python:
  ```
    python -m PyQt5.uic.pyuic ./assets/ui_file.ui -o ./assets/ui_file.py
  ```

  - To regenerate Qt resource files:
  ```
    pyrcc5 ./assets/resources.qrc -o ./assets/resources.py
  ```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better you can also simply open an issue with the tag `enhancement/relevant-name`.
Don't forget to give the project a star! Thanks again!

<!-- LICENSE -->
## License
This project is licensed under the MIT License — see the [LICENSE file](LICENSE)  for details.

<br>
<br>
<br>

<p align="right"><a href="#readme-top">back to top</a></p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python.com]: https://img.shields.io/badge/Python-ffffff?style=for-the-badge&logo=python
[Python-url]: https://python.com
[Qt.com]: https://img.shields.io/badge/PyQt-ffffff?style=for-the-badge&logo=qt
[Qt-url]: https://wiki.python.org/moin/PyQt
[SQLite-badge]: https://img.shields.io/badge/SQLite-ffffff?style=for-the-badge&logo=sqlite&logoColor=000000
[SQLite-url]: https://www.sqlite.org/

1. Create a virtual environment
python -m venv .venv

2. Activate the env
.venv\Scripts\activate

3. Install required packages
pip install -r requirements.txt

4. Run main.py

5. To change .ui files to .py files
python -m PyQt5.uic.pyuic ./assets/ui_file.ui -o ./assets/ui_file.py

6. To refresh resource files
pyrcc5 ./assets/resources.qrc -o ./assets/resources.py

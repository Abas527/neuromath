import os
import sys
import subprocess

def main():

    # launch GUI for neuromath
    app_path=os.path.join(os.path.dirname(__file__), 'app.py')
    subprocess.run([sys.executable,"-m","streamlit","run", app_path])
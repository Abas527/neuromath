import os
import sys
import subprocess

def main():

    app_path = os.path.join(os.path.dirname(__file__), 'app.py')

    
    env = os.environ.copy()
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    existing = env.get('PYTHONPATH', '')
    if pkg_root not in existing.split(os.pathsep):
        env['PYTHONPATH'] = pkg_root + (os.pathsep + existing if existing else '')

    subprocess.run([sys.executable, "-m", "streamlit", "run", app_path], env=env)
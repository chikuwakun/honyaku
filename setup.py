import sys
from cx_Freeze import setup, Executable

copyDependentFiles = True
silent = True
base = None
packages = []
includes = ['sys',
            'PySimpleGUI',
            're',
            'selenium',
            'time',
            'pdfminer',
            ]
excludes = []

if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "myPythonProgram",
version = "1.0",
options = {"build_exe": {"includes":includes, "excludes":excludes, "packages": packages}},
executables = [Executable("dappoukun.py",base=base)]
)
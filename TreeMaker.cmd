@echo off

REM Place this file alongside TreeMaker.py
REM Add the folder containing this file to the PATH!



REM Get the current working directory to create the Tree
set base_dir=%cd%

REM Look for the folder containing the TreeMaker.py file
cd %~dp0

REM Execute the Python file with the cwd and any args for CLI
python TreeMaker.py -d %base_dir% %*

REM Redirect to the base directory
cd %base_dir%
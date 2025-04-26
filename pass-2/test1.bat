@echo off
if not exist .\output_folder (
    mkdir .\output_folder
)
python pass2.py ..\pass-1\output_folder\intermediateFile1.txt .\output_folder\objectCode1.txt
pause

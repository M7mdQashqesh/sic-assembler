@echo off
if not exist .\output_folder (
    mkdir .\output_folder
)
python pass1.py .\testFiles\test1.asm .\output_folder\intermediateFile1.txt
pause

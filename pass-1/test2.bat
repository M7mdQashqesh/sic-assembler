@echo off
if not exist .\output_folder (
    mkdir .\output_folder
)
python pass1.py .\testFiles\test2.asm .\output_folder\intermediateFile2.txt
pause

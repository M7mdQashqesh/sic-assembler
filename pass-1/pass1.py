import sys
import os

sicFile = open(sys.argv[1], "r")  # Open assembly code file for reading
intermediateFile = open(sys.argv[2], "w")  # Open the mediator file for writing

OutputFile = open("Pass1_Output.py", "w")
os.system("cls")

SYBTAB = {}
lineNumber = 0
LOCCTR = "0" # HEX
isStart = 0
labelMap = {}
startAddress = "0" # HEX
isFirstLine = 0
startCounter = 0


def flagErrors(error, type, lineNumber):
    if type == "withLine":
        errorMessage = "At Line " + str(lineNumber) + " : " + error
    else:
        errorMessage = error
        print(errorMessage)
        exit()


for line in sicFile:
    isBYTE = 0
    isWORD = 0
    isRESB = 0
    isRESW = 0
    instructionSize = "3" # SIC
    lineNumber = lineNumber + 1

    # Remove empty lines and lines start with (.) this is comment lines
    if line.strip() == "":
        continue

    if line.strip()[0] == ".":
        continue

    else:
        # from letter #1 to letter #7 -> LABEL
        label = line[0:8]
        label = label.strip()
        if labelMap.get(label) != None:
            error = "Symbol " + str(label) + " already exist in symbol table\n"
            flagErrors(error, "withLine", lineNumber)
  
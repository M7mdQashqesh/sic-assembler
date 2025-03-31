import sys
import os
import math

sicFile = open(sys.argv[1], "r")  # Open assembly code file for reading
intermediateFile = open(sys.argv[2], "w")  # Open the mediator file for writing
OutputFile = open("Pass1_Output.py", "w")

os.system("cls")

SYBTAB = {}
lineNumber = 0
LOCCTR = "0"  # HEX
isSTART = False
labelMap = {}
startAddress = "0"  # HEX
isFirstLine = True
startCounter = 0


def flagErrors(error, errorType, lineNumber):
    if errorType == "withLine":
        errorMessage = "At line " + str(lineNumber) + " : " + error
    else:
        errorMessage = error
    print(errorMessage)
    exit()


for line in sicFile:
    isBYTE = False
    isWORD = False
    isRESB = False
    isRESW = False
    instructionSize = "3"  # SIC
    lineNumber += 1

    # Remove empty lines and lines start with (.) this is comment lines
    if line.strip() == "" or line.strip().startswith("."):
        continue

    else:
        # ? ========{LABEL}========
        # from 1 to 7 -> LABEL
        label = line[0:8].strip()
        if labelMap.get(label) != None:
            error = "Symbol " + str(label) + " already exist in symbol table\n"
            flagErrors(error, "withLine", lineNumber)
        # ? ========{LABEL}========

        # ? ========{OPCODE}========
        # from 10 to 15 -> opcode
        opCode = line[9:15].strip()
        if isFirstLine == True:
            isFirstLine = False
            if opCode != "START":
                error = "The program must begin with START directive"
                flagErrors(error, "withoutLine", lineNumber)
        if opCode == "START":
            isSTART = True
            startCounter += 1
        elif opCode == "BYTE":
            isBYTE = True
        elif opCode == "WORD":
            isWORD = True
        elif opCode == "RESB":
            isRESB = True
        elif opCode == "RESW":
            isRESW = True

        # write the line on list file
        intermediateFile.write(line)
        if opCode == "END":
            intermediateFile.write("\n")
        # ? ========{OPCODE}========

        # ? ========{OPERAND}========
        # from 18 to 35 -> operand
        operand = line[16:35].strip()
        if startCounter > 1:
            error = "The program must contain only one START directive"
            flagErrors(error, "withoutLine", lineNumber)
        # ? ========{OPERAND}========

        # ? ========{START directive}========
        if isSTART:
            startAddress = operand
            LOCCTR = startAddress
            PROGNAME = label
            isSTART = False
            continue
        # ? ========{START directive}========

        # ? ========{BYTE directive}========
        elif isBYTE:
            value = operand[2 : len(operand) - 1]
            # C' ' -> c' : [0] [1], this mean why start from 2
            convertedValue = ""
            if operand == "":
                error = "Directive " + opCode + " need an operand\n"
                flagErrors(error, "withLine", lineNumber)
            elif operand.startswith("C"):
                for ch in value:
                    convertedValue += hex(ord(ch)).lstrip("0x")
            elif operand.startswith("X"):
                convertedValue = value
            else:
                convertedValue = hex(int(operand, 16)).lstrip("0x")
            instructionSize = hex(math.ceil(len(convertedValue) / 2)).lstrip("0x")
        # ? ========{BYTE directive}========

        # ? ========{WORD directive}========
        elif isWORD:
            value = operand[2 : len(operand) - 1]
            convertedValue = ""
            if operand == "":
                error = "Directive " + opCode + " need an operand\n"
                flagErrors(error, "withLine", lineNumber)
            elif operand.startswith("C"):
                for ch in value:
                    convertedValue += hex(ord(ch)).lstrip("0x")
            elif operand.startswith("X"):
                convertedValue = value
            else:
                convertedValue = hex(int(operand, 16)).lstrip("0x")
            length = math.ceil(len(convertedValue) / 2)
            if length > 3:
                error = "Directive " + opCode + " can reserve only one word (3 BYTE)\n"
                flagErrors(error, "withLine", lineNumber)
            instructionSize = "3"
        # ? ========{WORD directive}========

        # ? ========{RESB directive}========
        elif isRESB:
            if operand == "":
                error = "Directive " + opCode + " need an operand\n"
                flagErrors(error, "withLine", lineNumber)
            instructionSize = hex(int(operand)).lstrip("0x")
        # ? ========{RESB directive}========

        # ? ========{RESW directive}========
        elif isRESW:
            if operand == "":
                error = "Directive " + opCode + " need an operand\n"
                flagErrors(error, "withLine", lineNumber)
            instructionSize = hex(int(operand) * 3).lstrip("0x")
        # ? ========{RESW directive}========
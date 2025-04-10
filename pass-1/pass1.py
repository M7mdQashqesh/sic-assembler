"""
Course Project -- Pass1

Name: Mohammed Qashqesh
id: 211014
"""

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
        # from 1 to 10 -> LABEL
        label = line[0:10].strip()
        if labelMap.get(label) != None:
            error = "Symbol " + str(label) + " already exists in the symbol table\n"
            flagErrors(error, "withLine", lineNumber)
        # ? ========{LABEL}========

        # ? ========{OPCODE}========
        # from 12 to 20 -> opcode
        opCode = line[11:20].strip()
        if isFirstLine == True:
            isFirstLine = False
            if opCode != "START":
                error = "The program must begin with the START directive"
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

        if opCode != "START":
            # ? ========{COMMENTS}========
            if len(line) > 39:
                comment = line[40:].strip()  # استخراج التعليق بعد المسافة
                line = line[:40].rstrip()  # إزالة التعليق، أخذ الجزء قبل 40
            else:
                comment = ""

            if comment:
                intermediateFile.write(f"{LOCCTR.zfill(4)} {line}\n")
            else:
                intermediateFile.write(f"{LOCCTR.zfill(4)} {line}")

            # ? ========{COMMENTS}========
        else:
            if len(line) > 39:
                comment = line[40:].strip()  # استخراج التعليق بعد المسافة
                line = line[:40].rstrip()  # إزالة التعليق، أخذ الجزء قبل 40
            else:
                comment = ""
            # Don't write LOCCTR for START
            if comment:
                intermediateFile.write("     " + line[:40] + "\n")
            else:
                intermediateFile.write("     " + line[:40])
        # ? ========{OPCODE}========

        # ? ========{OPERAND}========
        # from 22 to 39 -> operand
        operand = line[21:39].strip()
        if startCounter > 1:
            error = "The program must contain only one START directive"
            flagErrors(error, "withoutLine", lineNumber)
        # ? ========{OPERAND}========

        # ? ========{START directive}========
        if isSTART:
            startAddress = operand.upper()
            LOCCTR = startAddress
            PRGNAME = label
            isSTART = False
            continue
        # ? ========{START directive}========

        # ? ========{BYTE directive}========
        elif isBYTE:
            value = operand[2 : len(operand) - 1]
            convertedValue = ""
            if operand == "":
                error = "Directive " + opCode + " needs an operand\n"
                flagErrors(error, "withLine", lineNumber)
            elif operand.startswith("C"):
                for ch in value:
                    convertedValue += hex(ord(ch)).lstrip("0x").upper()
            elif operand.startswith("X"):
                convertedValue = value.upper()
            else:
                convertedValue = hex(int(operand, 16)).lstrip("0x").upper()
            instructionSize = (
                hex(math.ceil(len(convertedValue) / 2)).lstrip("0x").upper()
            )
        # ? ========{BYTE directive}========

        # ? ========{WORD directive}========
        elif isWORD:
            value = operand[2 : len(operand) - 1]
            convertedValue = ""
            if operand == "":
                error = "Directive " + opCode + " needs an operand\n"
                flagErrors(error, "withLine", lineNumber)
            elif operand.startswith("C"):
                for ch in value:
                    convertedValue += hex(ord(ch)).lstrip("0x").upper()
            elif operand.startswith("X"):
                convertedValue = value.upper()
            else:
                convertedValue = hex(int(operand, 16)).lstrip("0x").upper()
            length = math.ceil(len(convertedValue) / 2)
            if length > 3:
                error = "Directive " + opCode + " can reserve only one word (3 BYTE)\n"
                flagErrors(error, "withLine", lineNumber)
            instructionSize = "3"
        # ? ========{WORD directive}========

        # ? ========{RESB directive}========
        elif isRESB:
            if operand == "":
                error = "Directive " + opCode + " needs an operand\n"
                flagErrors(error, "withLine", lineNumber)
            instructionSize = hex(int(operand)).lstrip("0x").upper()
        # ? ========{RESB directive}========

        # ? ========{RESW directive}========
        elif isRESW:
            if operand == "":
                error = "Directive " + opCode + " needs an operand\n"
                flagErrors(error, "withLine", lineNumber)
            instructionSize = hex(int(operand) * 3).lstrip("0x").upper()
        # ? ========{RESW directive}========

        if label != "":
            temp = hex(int(LOCCTR, 16)).lstrip("0x").upper()
            SYBTAB[label] = ("0" * (4 - len(temp))) + temp
            labelMap[label] = 1
        LOCCTR = hex(int(LOCCTR, 16) + int(instructionSize, 16)).lstrip("0x").upper()

sicFile.close()
intermediateFile.close()

PRGLTH = hex(int(LOCCTR, 16) - int(startAddress, 16) - 3).lstrip("0x").upper()

whiteBold = "\033[1;37m"
blueLight = "\033[1;38;5;85m"
tableBorder = blueLight + "||" + whiteBold

print(whiteBold + "\n\tTHE PROGRAM PASSED PASS1 SUCCESSFULLY!!\n\n\tOUTPUT OF PASS 1:")

print("\t\t Program Name : " + blueLight + PRGNAME + whiteBold)
print("\t\t Program Length : " + blueLight + PRGLTH + whiteBold)
print("\t\t SYMBOL TABLE : ")
print(blueLight + "\t\t==================================================" + whiteBold)
sys.stdout.write(
    "\t\t"
    + "%-2s %-20s %-2s %-20s %-2s\n"
    % (tableBorder, "SYMBOL", tableBorder, "ADDRESS", tableBorder)
)

print(blueLight + "\t\t==================================================" + whiteBold)
for sym in SYBTAB:
    sys.stdout.write(
        "\t\t"
        + "%-2s %-20s %-2s %-20s %-2s\n"
        % (tableBorder, str(sym), tableBorder, str(SYBTAB[sym]), tableBorder)
    )
print(blueLight + "\t\t==================================================" + whiteBold)

OutputFile.write('ProgramName = "' + str(PRGNAME) + '"\n')
OutputFile.write('ProgramLength = "' + str(PRGLTH) + '"\n')
OutputFile.write('StartAddress = "' + str(startAddress) + '"\n')
OutputFile.write("SymbolTable = " + str(SYBTAB) + "\n")

OutputFile.close()

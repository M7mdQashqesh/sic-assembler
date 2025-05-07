"""
Course Project -- Pass2

Name: Mohammed Qashqesh
id: 211014
"""

import sys
import os
import math

from appendix import FORMAT3

# أضف مجلد pass-1 إلى sys.path
sys.path.append(os.path.abspath("../pass-1"))

# بعدها استورد بشكل عادي
from Pass1_Output import SymbolTable, ProgramLength, ProgramName, StartAddress

intermediateFile = open(sys.argv[1], "r")
objectFile = open(sys.argv[2], "w")

os.system("cls")

listingFile = open("listingfile.lst", "w")
lineNumber = 0
LOCCTR = "0"
objCode = []
endAddress = ""


def flagErrors(error, errorType, lineNumber):
    if errorType == "withLine":
        errorMessage = "At line " + str(lineNumber) + " : " + error
    else:
        errorMessage = error
    print(errorMessage)
    exit()


for line in intermediateFile:
    isBYTE = False
    isWORD = False
    isRESB = False
    isRESW = False
    isSTART = False
    isEND = False
    isINDEXED = False
    instructionSize = "3"  # SIC
    lineNumber += 1
    currentObjCode = ""

    if line.strip() == "":
        continue

    # ? ========{LABEL}========
    # from 5 to 15 -> LABEL
    label = line[5:15].strip()
    # ? ========{LABEL}========

    # ? ========{OPCODE}========
    # from 16 to 25 -> opcode
    opCode = line[16:25].strip()

    if opCode == "START":
        isSTART = True
    elif opCode == "BYTE":
        isBYTE = True
    elif opCode == "WORD":
        isWORD = True
    elif opCode == "RESB":
        isRESB = True
    elif opCode == "RESW":
        isRESW = True
    elif opCode == "END":
        isEND = True
    elif FORMAT3.get(opCode) == None:
        error = "opCode " + str(opCode) + " doesn't exists!\n"
        flagErrors(error, "withLine", lineNumber)
    # ? ========{OPCODE}========

    # ? ========{OPERAND}========
    operand = line[26:39].strip()

    if isRESW == 1:
        currentObjCode = "??????"
        instructionSize = hex(int(operand) * 3).lstrip("0x")
    elif isRESB == 1:
        currentObjCode = "??????"
        instructionSize = hex(int(operand)).lstrip("0x")
    elif isSTART:
        LOCCTR = StartAddress
        isSTART = 1
        LOCCTR = ("0" * (4 - len(LOCCTR))) + LOCCTR
        line = line.replace("\n", "")
        listingFile.write(line[0:35] + "\t" + "\n")
        continue
    elif isEND:
        endAddress = StartAddress
        LOCCTR = ("0" * (4 - len(LOCCTR))) + LOCCTR
        line = line.replace("\n", "")
        listingFile.write(line[0:35] + "\t" + "\n")
        continue
    elif isBYTE:
        value = operand[2 : len(operand) - 1]
        conv = ""
        if operand[0] == "C":
            for ch in value:
                conv += hex(ord(ch)).lstrip("0x")
        elif operand[0] == "X":
            conv = value
        else:
            conv = hex(int(operand)).lstrip("0x")
        currentObjCode = conv
        instructionSize = hex(math.ceil(len(conv) / 2)).lstrip("0x")
    elif isWORD:
        value = operand[2 : len(operand) - 1]
        conv = ""
        if operand[0] == "C":
            for ch in value:
                conv += hex(ord(ch)).lstrip("0x")
        elif operand[0] == "X":
            conv = value
        else:
            conv = hex(int(operand)).lstrip("0x")
        currentObjCode = conv
        instructionSize = "3"

    else:
        if operand == "":
            currentObjCode = FORMAT3[opCode] + "0000"
            objCode.append([currentObjCode, instructionSize, LOCCTR])
            LOCCTR = ("0" * (4 - len(LOCCTR))) + LOCCTR
            line = line.replace("\n", "")
            line = line[0:36] + (" " * (36 - len(line)))
            listingFile.write(LOCCTR + "\t" + line + currentObjCode + "\n")
            LOCCTR = hex(int(LOCCTR, 16) + int(instructionSize, 16)).lstrip("0x")
            continue
        elif operand.find(", X") != -1:
            operand = operand.replace(", X", "")
            isINDEXED = 1
        if SymbolTable.get(operand) == None:
            error = "operand " + str(operand) + " is not defined\n"
            flagErrors(error, "withLine", lineNumber)
        if SymbolTable.get(operand) != None:
            currentObjCode = str(FORMAT3[opCode]) + str(SymbolTable[operand])
        if isINDEXED:
            currentObjCode = hex(int(currentObjCode, 16) | int("008000", 16)).lstrip(
                "0x"
            )

    if not isBYTE:
        currentObjCode = ("0" * (6 - len(currentObjCode))) + currentObjCode
        objCode.append([currentObjCode, instructionSize, LOCCTR])
    else:
        objCode.append([currentObjCode, instructionSize, LOCCTR])

    LOCCTR = ("0" * (4 - len(LOCCTR))) + LOCCTR
    line = line.replace("\n", "")
    line = line + (" " * (35 - len(line)))

    if currentObjCode != "??????":
        listingFile.write(line[0:35] + "\t" + currentObjCode + "\n")
    else:
        listingFile.write(line[0:35] + "\t" + "\n")

    LOCCTR = hex(int(LOCCTR, 16) + int(instructionSize, 16)).lstrip("0x")

maxCapacity = int("1e", 16)
textRecordLen = "0"
currCapacity = 0
startRec = 0
ProgramName = ProgramName + (" " * (6 - len(ProgramName)))
currText = ""
StartAddress = ("0" * (6 - len(StartAddress))) + str(StartAddress)
ProgramName = ("0" * (6 - len(ProgramName))) + str(ProgramName)
prevRec = StartAddress

whiteBold = "\033[1;37m"
whiteLight = "\033[0;37m"
yellow = "\033[1;33m"
purple = "\033[1;36m"
blue = "\033[1;35m"

print(
    whiteBold
    + "H^"
    + yellow
    + ProgramName
    + whiteBold
    + "^"
    + purple
    + StartAddress
    + whiteBold
    + "^"
    + blue
    + ProgramLength
    + whiteBold
)

objectFile.write("H^" + ProgramName + "^" + StartAddress + "^" + ProgramLength + "\n")

for obj in objCode:
    if int(currCapacity) + int(obj[1], 16) <= maxCapacity and obj[0] != "??????":
        if currCapacity == 0:
            startRec = (obj[2]).upper()
        currCapacity = int(currCapacity) + int(obj[1], 16)
        currText = currText + "^" + obj[0].upper()
        textRecordLen = (
            hex(int(textRecordLen, 16) + int(obj[1], 16)).lstrip("0x")
        ).upper()

    elif currText != "":
        startRec = (("0" * (6 - len(startRec))) + str(startRec)).upper()
        textRecordLen = ("0" * (2 - len(textRecordLen))) + str(textRecordLen)
        print(
            "T^"
            + purple
            + startRec
            + whiteBold
            + "^"
            + blue
            + str(textRecordLen)
            + whiteBold
            + str(currText)
        )
        objectFile.write(
            "T^" + startRec + "^" + str(textRecordLen) + str(currText) + "\n"
        )
        prevRec = hex(int(obj[1], 16) + int(startRec, 16)).lstrip("0x")
        if int(currCapacity) + int(obj[1], 16) >= maxCapacity and obj[0] != "??????":
            currText = "^" + obj[0]
            textRecordLen = obj[1]
            currCapacity = obj[1]
            startRec = obj[2]
        else:
            currText = ""
            textRecordLen = "0"
            currCapacity = 0

    elif obj[0] == "??????":
        startRec = hex(int(obj[1], 16) + int(prevRec, 16)).lstrip("0x")

if currText != "":
    startRec = ("0" * (6 - len(startRec))) + str(startRec)
    textRecordLen = ("0" * (2 - len(textRecordLen))) + str(textRecordLen)
    print(
        "T^"
        + purple
        + startRec
        + whiteBold
        + "^"
        + blue
        + str(textRecordLen)
        + whiteBold
        + str(currText)
    )
    objectFile.write("T^" + startRec + "^" + str(textRecordLen) + str(currText) + "\n")

print("E^" + yellow + ("0" * (6 - len(endAddress))) + endAddress + whiteLight)
objectFile.write("E^" + ("0" * (6 - len(endAddress))) + endAddress + "\n")
objectFile.close()
listingFile.close()

COPY     START   1000               Start of the program
FIRST    STL     RETADR             Store return address
CLOOP    JSUB    RDREC              Jump to RDREC subroutine to read records
         LDA     LENGTH             Load the length of the record
         COMP    ZERO               Compare length with zero
         JEQ     ENDFIL             If length is zero, jump to ENDFIL
         JSUB    WRREC              Otherwise, jump to WRREC to write the record
         J       CLOOP              Jump back to CLOOP to repeat the process
ENDFIL   LDA     EOF                Load the EOF value
         STA     BUFFER             Store EOF in the buffer
         LDA     THREE              Load the value 3
         STA     LENGTH             Store 3 in LENGTH
         JSUB    WRREC              Call WRREC to write the EOF record
         LDL     RETADR             Load the return address
         RSUB                       Return from the subroutine
EOF      BYTE    C'EOF'             Define EOF as a string
THREE    WORD    3                  Define the constant 3
ZERO     WORD    0                  Define the constant 0
RETADR   RESW    1                  Reserve a word for the return address
LENGTH   RESW    1                  Reserve a word for the record length
BUFFER   RESB    4096               Reserve a 4096-byte buffer
.               
.        SUBROUTINE TO READ RECORD INTO BUFFER
.                
RDREC    LDX     ZERO                Load zero into index register X
         LDA     ZERO                Load zero into accumulator A
RLOOP    TD      INPUT               Test if input device is ready
         JEQ     RLOOP               If not ready, repeat the loop
         RD      INPUT               Read from the input device
         COMP    ZERO                Compare the read data with zero
         JEQ     EXIT                If zero, exit the loop
         STCH    BUFFER, X           Store character in buffer at index X
         TIX     MAXLEN              Increment index register X
         JLT     RLOOP               If less than MAXLEN, repeat the loop
EXIT     STX     LENGTH              Store the final index (length) in LENGTH
         RSUB                        Return from the subroutine
INPUT    BYTE    X'F1'               Define input device address
MAXLEN   WORD    4096                Define maximum length of record
.                  
.        SUBROUTINE TO WRITE RECORD FROM BUFFER
.                
WRREC    LDX     ZERO                Load zero into index register X
WLOOP    TD      OUTPUT              Test if output device is ready
         JEQ     WLOOP               If not ready, repeat the loop
         LDCH    BUFFER, X           Load character from buffer at index X
         WD      OUTPUT              Write character to the output device
         TIX     LENGTH              Increment index register X
         JLT     WLOOP               If less than LENGTH, repeat the loop
         RSUB                        Return from the subroutine
OUTPUT   BYTE    X'50'               Define output device address
         END     FIRST               End of the program
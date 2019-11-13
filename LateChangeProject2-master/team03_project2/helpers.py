
import sys

class SetUp:


    def __init__(self):
        pass

    @classmethod
    def get_input_filename(cls):
        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) - 1)):
                inputFileName = sys.argv[i + 1]
        return inputFileName

    @classmethod
    def import_data_file(cls):
        for i in range(len(sys.argv)):
            if (sys.argv[i] == '-i' and i < (len(sys.argv) -1)):
                inputFileName = sys.argv[i + 1]
        try:
            instructions = [line.rstrip() for line in open(inputFileName, 'r')]
        except IOError:
            print("Could not open input file, is path correct?")
        return instructions


    @classmethod
    def get_output_filename(cls):
        for i in range(len(sys.argv)):
            if(sys.argv[i] == '-o' and i < (len(sys.argv) -1)):
                outputFileName = sys.argv[i+1]
                #print("Raw output file name is: ", outputFileName)
        return outputFileName

    # Notice that  "imm_bit_to_32_bit_converter" does two things.
    # First it takes various length binaries and sign extends them to 32 bits
    #
    # Then it checks to see whether the number represents a negative or
    # positive number and returns the correct decimal version.  You use this when processing the
    # instructions.

    @classmethod
    def imm_bit_to_32_bit_converter(cls, num):
        negBits = '11111111111111111111111111111111'
        posBits = '00000000000000000000000000000000'
        extension = " "
        sigBit = num[0]

        if sigBit == '1':
            extension = negBits[:32 - len(num)]
            num = extension + num
            #return num
        else:
            extension = posBits[:32-len(num)]
            num = extension + num
        return num

    # No Op format instructions
    # Given by Lakomski
    @classmethod
    def bin2StringSpaced(cls,s):
        spacedStr = s[0:8] + " " + s[8:11] + " " + s[11:16] + " " + s[16:21] + " " + s[21:26] + " " + s[26:32]
        return spacedStr

    # D Format instructions
    # opcode        11 bits  0 - 11
    # address        9 bits 11 - 20
    # op2            2 bits 20 - 22
    # Rn             5 bits 22 - 27
    # Rt             5 bits 27 - 32
    @classmethod
    def bin2StringSpacedD(cls, s):
        spacedStrD = s[0:11] + " " + s[11:20] + " " + s[20:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStrD

    # IM Format instructions
    # field is unsigned value - is 16 bit pattern
    # opcode         9 bits  0 - 9
    # shift code     2 bits  9 - 11
    # field         16 bits 11 - 27
    # Rd             5 bits 27 - 32
    @classmethod
    def bin2StringSpacedIM(cls, s):
        spacedStrIM = s[0:9] + " " + s[9:11] + " " + s[11:27] + " " + s[27:32]
        return spacedStrIM

    # CB Format instructions
    #-- offset is signed value use twos compliment
    # opcode         8 bits  0 - 8
    # offset(w)     19 bits  8 - 27
    # conditional    5 bits 27 - 32
    @classmethod
    def bin2StringSpacedCB(cls, s):
        spacedStrCB = s[0:8] + " " + s[8:27] + " " + s[27:32]
        return spacedStrCB

    # I Format instructions
    # -- immediate is unsigned int
    # -- ADDI Rd = Rn + immediate
    # -- ADDI R3, R!, #Immed
    # opcode        10 bits  0 - 10
    # immediate     12 bits 10 - 22
    # Rn             5 bits 22 - 27
    # Rd             5 bits 27 - 32
    @classmethod
    def bin2StringSpacedI(cls, s):
        spacedStrI = s[0:10] + " " + s[10:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStrI

    # R Format instructions
    # -- SUB  Rd = Rn - Rm   SUB R3, R1, R2
    # -- ADD  Rd = Rm + Rn
    # -- AND  Rd = Rm & Rn
    # -- ORR  Rd = Rm | Rn
    # -- EOR Rd = Rm ^ Rn
    # -- LSL  Rd = Rn << Shamt
    # -- ASR  Rd = Rn >> Shamt  pad with sign bit <- PYTHON SYNTAX ISSUE!!!!!!
    # -- LSR Rd = Rn shifted Shamt right pad with zeros
    # opcode        11 bits  0 - 11
    # Rm             5 bits 11 - 16
    # Shamt          6 bits 16 - 22
    # Rn             5 bits 22 - 27
    # Rd             5 bits 27 - 32
    @classmethod
    def bin2StringSpacedR(cls, s):
        spacedStrR = s[0:11] + " " + s[11:16] + " " + s[16:22] + " " + s[22:27] + " " + s[27:32]
        return spacedStrR

    # B Format instructions
    #-- offset is signed value use twos compliment
    # opcode         6 bits  0 - 6
    # offset(w)     26 bits  6 - 32
    @classmethod
    def bin2StringSpacedB(cls, s):
        spacedStrB = s[0:6] + " " + s[6:32]
        return spacedStrB

  #  "imm_32_bit_unsigned_to_32_bit_signed_converter(cls,num): "
    # takes a 32 bit binary and returns the correct decimal representation.
    #
    # Given the above this should be extremely easy.
    # This is used to process the data strings since they are already 32 bit signed numbers.
    @classmethod
    def imm_32_bit_unsigned_to_32_bit_signed_converter(cls, num_str):
        #import sys
        bytes = 4
        num = int(num_str, 2)
        b = num.to_bytes(bytes, byteorder=sys.byteorder, signed=False)
        return int.from_bytes(b, byteorder=sys.byteorder, signed=True)

    @classmethod
    def decimalToBinary(cls, num):
        if(num <= 262144):
            return bin(num).replace("0b", "0")
        else:
            return bin(num).replace("0b", "1")

    @classmethod
    def binaryToDecimal(cls, binary):
        print("\n")
        print(int(binary, 2))

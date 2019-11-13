from helpers import SetUp
import os
import masking_constants as MASKs
import sys


class Disassembler:

    def __init__(self):

        self.bMask = MASKs.bMask
        self.jAddrMask = MASKs.jAddrMask
        self.specialMask = MASKs.specialMask
        self.rnMask = MASKs.rnMask
        self.rmMask = MASKs.rmMask
        self.rdMask = MASKs.rdMask
        self.imMask = MASKs.imMask
        self.shmtMask = MASKs.shmtMask
        self.addrMask = MASKs.addrMask
        self.addr2Mask = MASKs.addr2Mask
        self.imsftMask = MASKs.imsftMask
        self.imdataMask = MASKs.imdataMask



    opcodeStr = []
    instrSpaced = []
    arg1 = []
    arg2 = []
    arg3 = []
    tempArg = 0
    arg1Str = []
    arg2Str = []
    arg3Str = []
    rawData = []
    dataVal = []
    address = []
    numInstructions = 0

    def printDis(self):
        outFile = open(SetUp.get_output_filename() + "_dis.txt", 'w')
        #print("number of instructions " + str(self.numInstructions))
        for i in range(self.numInstructions):
            outFile.write(str(self.instrSpaced[i]) + '\t' + str(self.address[i]) + '\t'
                          + str(self.opcodeStr[i]) + str(self.arg1Str[i]) + str(self.arg2Str[i]) + str(self.arg3Str[i]) + '\n')
        index = self.numInstructions
        for index in range (len(self.dataVal)):
            outFile.write(str(self.rawData[index]) + '\t' + str(self.address[index + self.numInstructions]) + '\t' + str(self.dataVal[index]) + '\n')

        outFile.close()
    def run(self):

        pass

        instructions = []
        instructions = SetUp.import_data_file()

        outputFilename = SetUp.get_output_filename()

        # print(hex(MASKs.bMask))
        # print(bin(MASKs.bMask))
        # print(f'{MASKs.bMask:32b}')

        # create an address list
        for i in range(len(instructions)):
            self.address.append(96 + (i * 4))

        opcode = []

        # create an opcode list
        for z in instructions:
            opcode.append(int(z, base=2) >> 21)

        # decode and dissect

        for i in range(len(opcode)):
            self.numInstructions = self.numInstructions + 1
            # NOP type
            if opcode[i] == 0:
                self.instrSpaced.append(SetUp.bin2StringSpaced(instructions[i]))
                self.opcodeStr.append("NOP")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")

            # B type
            elif 160 <= opcode[i] <= 191:  # B type
                self.instrSpaced.append(SetUp.bin2StringSpacedB(instructions[i]))
                self.opcodeStr.append("B")
                self.arg1.append((int(instructions[i], base=2) & self.bMask) >> 0)
                self.tempArg = self.arg1[i]
                self.tempArg = str(SetUp.decimalToBinary(self.tempArg))
                self.tempArg = SetUp.imm_bit_to_32_bit_converter(self.tempArg)
                self.tempArg = SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(self.tempArg)
                self.arg1[i] = self.tempArg
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("\t#" + str(self.arg1[i]))
                self.arg2Str.append("")
                self.arg3Str.append("")

            # AND type
            elif opcode[i] == 1104:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("AND")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

            # ADD
            elif opcode[i] == 1112:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ADD")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

            # ADDI
            elif 1160 <= opcode[i] <= 1161:
                self.instrSpaced.append(SetUp.bin2StringSpacedI(instructions[i]))
                self.opcodeStr.append("ADDI")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.imMask) >> 10)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))

            # ORR
            elif opcode[i] == 1360:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ORR")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

            # CBZ signed
            elif 1440 <= opcode[i] <= 1447:
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(instructions[i]))
                self.opcodeStr.append("CBZ")
                self.arg1.append((int(instructions[i], base=2) & self.addr2Mask) >> 5)
                self.tempArg = self.arg1[i]
                self.tempArg = str(SetUp.decimalToBinary(self.tempArg))
                self.tempArg = SetUp.imm_bit_to_32_bit_converter(self.tempArg)
                self.tempArg = SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(self.tempArg)
                self.arg1[i] = self.tempArg
                self.arg2.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg3.append(0)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", #" + str(self.arg1[i]))
                self.arg3Str.append("")

            # CBNZ signed
            elif 1448 <= opcode[i] <= 1455:
                self.instrSpaced.append(SetUp.bin2StringSpacedCB(instructions[i]))
                self.opcodeStr.append("CBNZ")
                self.arg1.append((int(instructions[i], base=2) & self.addr2Mask) >> 5)
                self.tempArg = self.arg1[i]
                self.tempArg = str(SetUp.decimalToBinary(self.tempArg))
                self.tempArg = SetUp.imm_bit_to_32_bit_converter(self.tempArg)
                self.tempArg = SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(self.tempArg)
                self.arg1[i] = self.tempArg
                self.arg2.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg3.append(0)
                self.arg1Str.append("\tR" + str(self.arg2[i]))
                self.arg2Str.append(", #" + str(self.arg1[i]))
                self.arg3Str.append("")

            # SUB
            elif opcode[i] == 1624:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("SUB")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

            # SUBI
            elif 1672 <= opcode[i] <= 1673:
                self.instrSpaced.append(SetUp.bin2StringSpacedI(instructions[i]))
                self.opcodeStr.append("SUBI")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.imMask) >> 10)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))

            # MOVZ
            elif 1684 <= opcode[i] <= 1687:
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(instructions[i]))
                self.opcodeStr.append("MOVZ")
                self.arg1.append((int(instructions[i], base=2) & self.imdataMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.imsftMask) >> 17)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", " + str(self.arg1[i]))
                self.arg3Str.append(", LSL " + str(self.arg2[i]))

            # LSR
            elif opcode[i] == 1690:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("LSR")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.shmtMask) >> 10)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))

            # LSL
            elif opcode[i] == 1691:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("LSL")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.shmtMask) >> 10)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))

            # ASR
            elif opcode[i] == 1692:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("ASR")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.shmtMask) >> 10)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]))

            # EOR
            elif opcode[i] == 1872:
                self.instrSpaced.append(SetUp.bin2StringSpacedR(instructions[i]))
                self.opcodeStr.append("EOR")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.rmMask) >> 16)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", R" + str(self.arg1[i]))
                self.arg3Str.append(", R" + str(self.arg2[i]))

            # MOVK
            elif 1940 <= opcode[i] <= 1943:
                self.instrSpaced.append(SetUp.bin2StringSpacedIM(instructions[i]))
                self.opcodeStr.append("MOVK")
                self.arg1.append((int(instructions[i], base=2) & self.imdataMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.imsftMask) >> 17)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", " + str(self.arg1[i]))
                self.arg3Str.append(", LSL " + str(self.arg2[i]))

            # STUR
            elif opcode[i] == 1984:
                self.instrSpaced.append(SetUp.bin2StringSpacedD(instructions[i]))
                self.opcodeStr.append("STUR")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.addrMask) >> 12)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", [R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]) + "]")

            # LDUR
            elif opcode[i] == 1986:
                self.instrSpaced.append(SetUp.bin2StringSpacedD(instructions[i]))
                self.opcodeStr.append("LDUR")
                self.arg1.append((int(instructions[i], base=2) & self.rnMask) >> 5)
                self.arg2.append((int(instructions[i], base=2) & self.addrMask) >> 12)
                self.arg3.append((int(instructions[i], base=2) & self.rdMask) >> 0)
                self.arg1Str.append("\tR" + str(self.arg3[i]))
                self.arg2Str.append(", [R" + str(self.arg1[i]))
                self.arg3Str.append(", #" + str(self.arg2[i]) + "]")

            # BREAK
            elif opcode[i] == 2038 and (int(instructions[i], base=2) & self.specialMask) == 2031591:
                self.instrSpaced.append(SetUp.bin2StringSpaced(instructions[i]))
                self.opcodeStr.append("BREAK")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print
                "breaking"
                break

            # NOT A TYPE
            else:
                self.opcodeStr.append("unkown")
                self.arg1.append(0)
                self.arg2.append(0)
                self.arg3.append(0)
                self.arg1Str.append("")
                self.arg2Str.append("")
                self.arg3Str.append("")
                print("i=:  " + str(i))
                print("opcode =: " + str(opcode[i]))
                sys.exit("You have found an unknown instruction, investigate NOW")

        # Now read the memory lines
        #index = 15 #self.numInstructions

        for index in range (self.numInstructions, len(instructions)):
            self.rawData.append(instructions[index])
            self.dataVal.append(SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(self.rawData[index - self.numInstructions]))

        return {#"intructions":instructions
            "opcode": opcode,
            "opcodeStr" : self.opcodeStr,
            "arg1": self.arg1,
            "arg1Str": self.arg1Str,
            "arg2": self.arg2,
            "arg2Str": self.arg2Str,
            "arg3": self.arg3,
            "arg3Str": self.arg3Str,
            "dataVal" :self.dataVal,
            "address": self.address,
            "numInstructions": self.numInstructions}



       # while(self.numInstructions <= index <= len(instructions)):


            #self.rawData.append(instructions[index])
            #self.dataVal.append(SetUp.imm_32_bit_unsigned_to_32_bit_signed_converter(self.rawData[index]))
             #print(instructions[self.numInstructions], end="\t")
             #print(self.address[self.numInstructions], end=" ")
             #print(self.dataVal[self.numInstructions])

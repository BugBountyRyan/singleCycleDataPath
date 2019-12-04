import sys
from helpers import SetUp
import masking_constants as MASKs


class State():
    dataVal = []
    PC = 96
    cycle = 1
    R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self, opcode, opcodeStr, arg1, arg1Str, arg2, arg2Str, arg3, arg3Str, dataVal, address,
                 numInstructions):
        self.opcode = opcode
        self.opcodeStr = opcodeStr
        self.arg1 = arg1
        self.arg1Str = arg1Str
        self.arg2 = arg2
        self.arg2Str = arg2Str
        self.arg3 = arg3
        self.arg3Str = arg3Str
        self.dataVal = dataVal
        self.address = address
        self.numInstructions = numInstructions

    def getIndexOfMemAddress(self, curAddr):
        try:
            return self.address.index(curAddr)
        except ValueError:
            return -1

    def incrementPC(self):
        self.PC = self.PC + 4

    def printState(self):
        outputFileName = SetUp.get_output_filename()

        with open(outputFileName + "_sim.txt", 'a') as outFile:

            i = self.getIndexOfMemAddress(self.PC)
            outFile.write("=====================\n")
            outFile.write(
                "cycle:" + str(self.cycle) + "\t" + str(self.PC) + "\t" + self.opcodeStr[i] + self.arg1Str[i] +
                self.arg2Str[i] +
                self.arg3Str[i] + "\n")
            outFile.write("\n")
            outFile.write("registers:\n")
            outStr = "r00:"

            for i in range(0, 8):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r08:"

            for i in range(8, 16):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r16:"

            for i in range(16, 24):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outStr = "r24:"

            for i in range(24, 32):
                outStr = outStr + "\t" + str(self.R[i])
            outFile.write(outStr + "\n")
            outFile.write("\ndata:\n")
            outStr = "\n"
            for i in range(len(self.dataVal)):

                if (i % 8 == 0 and i != 0 or i == len(self.dataVal)):
                    outFile.write(outStr + "\n")

                if (i % 8 == 0):

                    outStr = str(self.address[i + self.numInstructions]) + ":" + str(self.dataVal[i])

                if (i % 8 != 0):
                    outStr = outStr + "\t" + str(self.dataVal[i])

            outFile.write(outStr + "\n")
            outFile.close()


class Simulator():

    def __init__(self, opcode, opcodeStr, arg1, arg1Str, arg2, arg2Str, arg3, arg3Str, dataVal, address,
                 numInstructions):
        self.opcode = opcode
        self.opcodeStr = opcodeStr
        self.arg1 = arg1
        self.arg1Str = arg1Str
        self.arg2 = arg2
        self.arg2Str = arg2Str
        self.arg3 = arg3
        self.arg3Str = arg3Str
        self.dataVal = dataVal
        self.address = address
        self.numInstructions = numInstructions
        self.specialMask = MASKs.specialMask

    def run(self):
        foundBreak = False
        armState = State(self.opcode, self.opcodeStr, self.arg1, self.arg1Str, self.arg2, self.arg2Str, self.arg3,
                         self.arg3Str,
                         self.dataVal, self.address, self.numInstructions)
        nonUpdatedDataValLength = len(self.dataVal)

        while (foundBreak == False):
            jumpAddr = armState.PC
            i = armState.getIndexOfMemAddress(armState.PC)

            # NOP: No Operation.
            if (self.opcode[i] == 0):
                armState.printState()
                armState.incrementPC()
                armState.cycle += 1
                continue

            # B: Extends and shifts (multipies by 4) the 26 bit argument (words) in offset and adds the
            # value to the PC.
            elif (160 <= self.opcode[i] <= 191):
                jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)

            # AND: Rn register & Rm  register result into Rd register.
            elif self.opcode[i] == 1104:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] & armState.R[self.arg1[i]]

            # ADD: Rn register + Rm  register result into Rd register.
            elif self.opcode[i] == 1112:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] + armState.R[self.arg1[i]]

            # ADDI Adds extended immediate value to the value in Rn register
            # and puts value in Rd  register. Immediate is positive.
            if 1160 <= self.opcode[i] <= 1161:
                armState.R[self.arg3[i]] = self.arg2[i] + armState.R[self.arg1[i]]

            # ORR: Rn register or Rm  register result into Rd register.
            elif self.opcode[i] == 1360:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] | armState.R[self.arg1[i]]

            # CBZ: Does comparison against zero of condition register and if condition met adds extended
            # and shifted offset to the PC. Offset can be positive or negative.  Offset in words.
            elif 1440 <= self.opcode[i] <= 1447:
                if self.arg2[i] == 0:
                    jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)

            # CBNZ: Does comparison against zero of condition register and if condition met adds extended
            # and shifted offset to the PC. Offset can be positive or negative.  Offset in words.
            elif 1448 <= self.opcode[i] <= 1455:
                if self.arg2[i] != 0:
                    jumpAddr = jumpAddr + ((self.arg1[i] * 4) - 4)

            # SUB:  Rn register - Rm  register result into Rd register.
            elif self.opcode[i] == 1624:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] - armState.R[self.arg1[i]]

            # SUBI: Subtracts extended immediate value from the value in Rn register and puts value in
            # Rd register. Immediate is positive.
            elif 1672 <= self.opcode[i] <= 1673:
                armState.R[self.arg3[i]] = self.arg2[i] - armState.R[self.arg1[i]]


            # MOVZ: 16 bit pattern in field register shifted left by either 0,16,32,48 positions determined
            # by 2 bit shift code value and written into zeroed Rd register.
            elif 1684 <= self.opcode[i] <= 1687:
                armState.R[self.arg2[i]] = 0
                armState.R[self.arg2[i]] = armState.R[self.arg3[i]] << armState.R[self.arg1[i]]

            # LSR: This is a pattern shift. Whatever is in register is shifted right with zero fill.
            elif self.opcode[i] == 1690:
                # armState.R[self.arg3[i]] = armState.R[self.arg2[i]] / 2 ** armState.R[self.arg1[i]]
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] % (1 << 32) >> self.arg1[i]
            # LSL: Shift left arg2 positions adding zeros on the right.
            elif self.opcode[i] == 1691:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] << armState.R[self.arg1[i]]

            # ASR: This is  ">>" will divide by 2.
            elif self.opcode[i] == 1692:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] >> armState.R[self.arg1[i]]

            # EOR: Rn register ^ Rm  register result into Rd register.
            elif self.opcode[i] == 1872:
                armState.R[self.arg3[i]] = armState.R[self.arg2[i]] ^ armState.R[self.arg1[i]]

            # MOVK: 16 bit pattern in field  register shifted left by either 0,16,32,48 positions determined by
            # 2 bit shift code value and written into  a register leaving all other bits intact.
            elif 1940 <= self.opcode[i] <= 1943:
                armState.R[self.arg2[i]] = armState.R[self.arg3[i]] << armState.R[self.arg1[i]]

            # STUR: get data from register RT and store that data in memory
            elif self.opcode[i] == 1984:
                targetAddress = (armState.R[self.arg1[i]] + (self.arg2[i] * 4))
                while armState.getIndexOfMemAddress(targetAddress) == -1:
                    self.dataVal.append(0)
                    self.address.append(max(self.address) + 4)
                self.dataVal[armState.getIndexOfMemAddress(targetAddress)-self.numInstructions+nonUpdatedDataValLength] = armState.R[self.arg3[i]]

            # LDUR: get data from memory and store in Register RT
            elif self.opcode[i] == 1986:
                targetAddress = (armState.R[self.arg1[i]] + (self.arg2[i] * 4))
                while armState.getIndexOfMemAddress(targetAddress) == -1:
                    self.dataVal.append(0)
                    self.address.append(max(self.address) + 4)
                armState.R[self.arg3[i]] = self.dataVal[armState.getIndexOfMemAddress(targetAddress)-self.numInstructions+nonUpdatedDataValLength]

            # BREAK:
            elif self.opcode[i] == 2038:
                foundBreak = True

            else:
                print("IN SIM -- UNKNOWN INSTRUCTION---------!!!!!")

            # For feng shui of output
            while len(self.address[self.numInstructions:]) % 8 != 0:
                for j in range(len(self.address[self.numInstructions:]) % 8):
                    self.dataVal.append(0)
                    self.address.append(max(self.address) + 4)
            armState.printState()
            armState.PC = jumpAddr
            armState.incrementPC()
            armState.cycle += 1

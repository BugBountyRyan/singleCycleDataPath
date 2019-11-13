import Disassembler
import simulator

mydis = Disassembler.Disassembler()
output = {}
output = mydis.run()
mydis.printDis()

#mydis.printDis()
mysim = simulator.Simulator(**output)
mysim.run()
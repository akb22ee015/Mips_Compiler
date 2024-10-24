class MIPS_Simulator:
    def __init__(self):
        self.registers = [0] * 32
        self.memory = [0] * 256
        self.pc = 0
        self.instruction_memory = []

    def load_instructions(self, instruction_binaries):
        self.instruction_memory = instruction_binaries

    def fetch(self):
        if self.pc < len(self.instruction_memory):
            instruction = self.instruction_memory[self.pc]
            self.pc += 1
            return instruction
        return None

    def decode(self, instruction):
        opcode = int(instruction[0:6], 2)
        rs = int(instruction[6:11], 2)
        rt = int(instruction[11:16], 2)
        rd = int(instruction[16:21], 2)
        shamt = int(instruction[21:26], 2)
        funct = int(instruction[26:32], 2)
        immediate = int(instruction[16:], 2) if opcode != 2 else None
        return opcode, rs, rt, rd, shamt, funct, immediate

    def execute(self, opcode, rs, rt, rd, shamt, funct, immediate):
        if opcode == 0:
            if funct == 32:
                result = self.registers[rs] + self.registers[rt]
                return result, True
            elif funct == 34:
                result = self.registers[rs] - self.registers[rt]
                return result, True
            elif funct == 36:
                result = self.registers[rs] & self.registers[rt]
                return result, True
            elif funct == 37:
                result = self.registers[rs] | self.registers[rt]
                return result, True
            elif funct == 42:
                result = 1 if self.registers[rs] < self.registers[rt] else 0
                return result, True
        elif opcode == 8:
            result = self.registers[rs] + immediate
            return result, True
        elif opcode == 35:
            address = self.registers[rs] + immediate
            data = self.memory[address]
            return data, False
        elif opcode == 43:
            address = self.registers[rs] + immediate
            self.memory_access(address, self.registers[rt], write=True)
            return None, False
        elif opcode == 4:
            if self.registers[rs] == self.registers[rt]:
                return immediate, 'branch'
            else:
                return None, False
        return None, False

    def memory_access(self, address, data=None, write=False):
        if write:
            self.memory[address] = data
        else:
            return self.memory[address]

    def write_back(self, rd, result):
        if rd != 0:
            self.registers[rd] = result

    def run(self):
        while True:
            instruction = self.fetch()
            if instruction is None:
                print("No more instructions to execute.")
                break

            opcode, rs, rt, rd, shamt, funct, immediate = self.decode(instruction)
            print(f"Fetched instruction: {instruction} (PC={self.pc-1})")
            print(f"Decoded: opcode={opcode}, rs={rs}, rt={rt}, rd={rd}, funct={funct}, immediate={immediate}")

            result, action = self.execute(opcode, rs, rt, rd, shamt, funct, immediate)
            if action == 'branch':
                self.pc += result
                continue
            elif action:
                self.write_back(rd, result)
            elif opcode == 35:
                self.write_back(rt, result)
            elif opcode == 43:
                self.memory_access(self.registers[rs] + immediate, result, write=True)

            print("Registers:", self.registers)

from Model.compiler_simulator import *

if __name__ == "__main__":
    simulator = MIPS_Simulator()

    data_segment, text_segment, label_address_map = parse_asm_file('B22EE015_B22CS096_test4.asm')
    print("Data Segment:", data_segment)
    instruction_binaries = []
    for index, instr in enumerate(text_segment):
        binary_instr = parse_instruction(instr, data_segment, label_address_map, index)
        instruction_binaries.append(binary_instr)
        if binary_instr is not None:
            print(f'{instr}: {binary_instr}')

    simulator.load_instructions(instruction_binaries)

    for k,v in data_segment.items():
        simulator.memory[v] = v

    simulator.run()

    print("Final state of registers:")
    for i, reg in enumerate(simulator.registers):
        print(f"$r{i}: {reg}\n", end=" ")

    print("\nFinal state of memory:")
    for i in range(64):
        print(f"Memory[{i}]: {simulator.memory[i]}\n", end=" ")

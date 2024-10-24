# MIPS Compiler and Simulator

## Overview

This project implements a MIPS assembly compiler and a MIPS instruction simulator. The compiler translates MIPS assembly instructions into binary machine code, and the simulator mimics the execution of these instructions on a MIPS processor. It simulates the instruction cycle, including instruction fetching, decoding, execution, memory access, and write-back.

## Features

- **Instruction Compilation:** Converts MIPS assembly instructions to binary machine code.
- **Instruction Simulation:** Simulates the execution of MIPS instructions using a virtual processor.
- **Supports R, I, and J type instructions:** Handles a wide range of instructions, including arithmetic, logic, memory access, and branching operations.
- **Registers and Memory:** The simulator features 32 registers and a memory array of 256 words.
- **Branching:** Simulates conditional and unconditional branching instructions.

## File Structure

- `compiler_simulator.py`: Contains the core functionality for compiling and simulating MIPS instructions.
- `OPCODE_MAP`, `FUNCTION_MAP`, and `REGISTER_MAP`: Define mappings for MIPS instruction opcodes, function codes, and registers.
- `MIPS_Simulator`: A class representing a simulated MIPS processor, which can execute compiled instructions and handle various operations.

## How It Works

### 1. Compiler
The MIPS compiler reads a MIPS assembly file, parses the instructions, and converts them into their corresponding binary format. It supports label resolution for branch and jump instructions.

### 2. Simulator
The simulator fetches, decodes, and executes instructions in the compiled binary format. It supports:

- **Arithmetic Operations:** `add`, `sub`, `and`, `or`, `slt`, etc.
- **Immediate Instructions:** `addi`, `andi`, etc.
- **Memory Access Instructions:** `lw`, `sw`
- **Branching Instructions:** `beq`, `bne`
- **Jump Instructions:** `j`, `jal`

### 3. Example
You can test the compiler and simulator by loading a MIPS assembly file and running it through the simulation process.

```python
from compiler_simulator import MIPS_Simulator, parse_asm_file

# Initialize simulator
simulator = MIPS_Simulator()

# Parse the ASM file and load instructions
data_segment, text_segment, label_address_map = parse_asm_file('Test_File/test_1.asm')
binary_instructions = [parse_instruction(instr, data_segment, label_address_map, i) for i, instr in enumerate(text_segment)]

# Load compiled instructions into the simulator
simulator.load_instructions(binary_instructions)

# Run the simulation
simulator.run()
```

## Instruction Set Support
The compiler and simulator support the following MIPS instructions:

- **R-type**: `add`, `sub`, `and`, `or`, `slt`, etc.
- **I-type**: `addi`, `andi`, `lw`, `sw`, `beq`, `bne`, etc.
- **J-type**: `j`, `jal`

## Getting Started

### Prerequisites
- Python 3.x

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/akb22ee015/MIPS_Compiler.git
    ```

2. Navigate to the project directory:

    ```bash
    cd MIPS_Compiler
    ```

3. Run the compiler and simulator:

    ```bash
    python compiler_simulator.py
    ```

### Input File Format
The input MIPS assembly file should be structured with `.data` and `.text` sections. Labels can be used for branch and jump instructions. Here’s an example of a simple MIPS program:

```asm
.data
array: .word 5

.text
main:
    lw $t0, array
    add $t1, $t0, $t0
    sw $t1, array
    j main


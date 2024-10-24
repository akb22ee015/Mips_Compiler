import re

OPCODE_MAP = {
    'add': '000000',
    'addu': '000000',
    'sub': '000000',
    'subu': '000000',
    'and': '000000',
    'andi': '001100',
    'or': '000000',
    'ori': '001101',
    'xor': '000000',
    'xori': '001110',
    'nor': '000000',
    'slt': '000000',
    'slti': '001010',
    'sltu': '000000',
    'sltiu': '001011',
    'addi': '001000',
    'addiu': '001001',
    'lui': '001111',
    'sll': '000000',
    'srl': '000000',
    'sra': '000000',
    'div': '000000',
    'divu': '000000',
    'mult': '000000',
    'multu': '000000',
    'mfhi': '000000',
    'mflo': '000000',
    'mthi': '000000',
    'mtlo': '000000',
    'beq': '000100',
    'bne': '000101',
    'bgez': '000001',
    'bgtz': '000111',
    'blez': '000110',
    'bltz': '000001',
    'j': '000010',
    'jal': '000011',
    'jr': '000000',
    'jalr': '000000',
    'lw': '100011',
    'sw': '101011',
    'lb': '100000',
    'lbu': '100100',
    'lh': '100001',
    'lhu': '100101',
    'sb': '101000',
    'sh': '101001',
    'syscall': '000000',
    'break': '000000'
}

FUNCTION_MAP = {
    'add': '100000',
    'addu': '100001',
    'sub': '100010',
    'subu': '100011',
    'and': '100100',
    'or': '100101',
    'nor': '100111',
    'slt': '101010',
    'sltu': '101011',
    'xor': '100110',
    'mult': '011000',
    'multu': '011001',
    'div': '011010',
    'divu': '011011',
    'mfhi': '010000',
    'mflo': '010010',
    'mthi': '010001',
    'mtlo': '010011',
    'sll': '000000',
    'srl': '000010',
    'sra': '000011',
}

instruction_type_map = {
    'add': 'R',
    'sub': 'R',
    'and': 'R',
    'or': 'R',
    'slt': 'R',
    'sll': 'R',
    'srl': 'R',
    'jr': 'R',
    'addi': 'I',
    'andi': 'I',
    'ori': 'I',
    'lw': 'I',
    'sw': 'I',
    'beq': 'I',
    'bne': 'I',
    'lui': 'I',
    'j': 'J',
    'jal': 'J',
}

REGISTER_MAP = {
    '$zero': 0, '$at': 1, '$v0': 2, '$v1': 3,
    '$a0': 4, '$a1': 5, '$a2': 6, '$a3': 7,
    '$t0': 8, '$t1': 9, '$t2': 10, '$t3': 11,
    '$t4': 12, '$t5': 13, '$t6': 14, '$t7': 15,
    '$s0': 16, '$s1': 17, '$s2': 18, '$s3': 19,
    '$s4': 20, '$s5': 21, '$s6': 22, '$s7': 23,
    '$t8': 24, '$t9': 25, '$k0': 26, '$k1': 27,
    '$gp': 28, '$sp': 29, '$fp': 30, '$ra': 31
}

def get_register_number(register_str):
    if register_str in REGISTER_MAP:
        return REGISTER_MAP[register_str]
    elif register_str.startswith('$'):
        try:
            reg_num = int(register_str[1:])
            if 0 <= reg_num <= 31:
                return reg_num
            else:
                raise ValueError(f"Invalid register number: {register_str}")
        except ValueError:
            raise ValueError(f"Invalid register format: {register_str}")
    else:
        raise ValueError(f"Invalid register format: {register_str}")

def parse_i_instruction(parts, data_segment):
    rt = parts[0]
    base_register = parts[1]
    imm = 0

    if len(parts) == 3:
        imm = int(parts[2])
        rs = base_register
    elif '(' in parts[1]:
        offset, base_reg = parts[1].replace(')', '').split('(')
        imm = int(offset)
        rs = base_reg
    else:
        if base_register in data_segment:
            imm = data_segment[base_register]
            rs = '$zero'
        else:
            rs = base_register

    return rt, rs, imm

def parse_instruction(instr, data_segment, label_address_map, index):
    machine_code = ''
    parts = instr.replace(',', '').split()
    instr_type = instruction_type_map[parts[0]]
    opcode = OPCODE_MAP[parts[0]]

    if instr_type == 'R':
        rd = format(get_register_number(parts[1]), '05b')
        rs = format(get_register_number(parts[2]), '05b')
        rt = format(get_register_number(parts[3]), '05b')
        funct = FUNCTION_MAP[parts[0]]
        shamt = '00000'
        machine_code += opcode + rs + rt + rd + shamt + funct

    elif instr_type == 'I':
        if parts[0] in ['beq', 'bne']:
            rt = parts[1]
            rs = parts[2]
            label = parts[3]
            target_address = label_address_map[label]
            offset = target_address - (index + 1)
            imm_bin = format(offset & 0xFFFF, '016b')
            machine_code += opcode + format(get_register_number(rs), '05b') + format(get_register_number(rt), '05b') + imm_bin
        else:
            rt, base_register, imm = parse_i_instruction(parts[1:], data_segment)
            rs = format(get_register_number(base_register), '05b') if base_register in REGISTER_MAP else '00000'
            rt = format(get_register_number(rt), '05b')
            imm_bin = format(imm & 0xFFFF, '016b')
            machine_code += opcode + rs + rt + imm_bin

    elif instr_type == 'J':
        label = parts[1]
        target_address = label_address_map[label]
        machine_code += opcode + format(target_address, '026b')

    return machine_code

def parse_asm_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data_segment = {}
    text_segment = []
    label_address_map = {}
    current_segment = None

    for line in lines:
        line = line.strip()
        if line.startswith('.data'):
            current_segment = 'data'
            continue
        elif line.startswith('.text'):
            current_segment = 'text'
            continue
        elif current_segment == 'data' and line:
            label, value = line.split(':')
            data_segment[label.strip()] = int(value.split()[1])
        elif current_segment == 'text':
            if ':' in line:
                label = line.split(':')[0].strip()
                label_address_map[label] = len(text_segment)
                line = line.split(':', 1)[1].strip()
            if line:
                text_segment.append(line)

    return data_segment, text_segment, label_address_map

if __name__ == '__main__':
    data_segment, text_segment, label_address_map = parse_asm_file('Test_File\\test_1.asm')
    print("Data Segment:", data_segment)

    for index, instr in enumerate(text_segment):
        binary_instr = parse_instruction(instr, data_segment, label_address_map, index)
        if binary_instr is not None:
            print(f'{instr}: {binary_instr}')

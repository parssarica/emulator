#!/usr/bin/python3

import sys
import ast

instruction_pointer = 0
z_flag = False
registers = {"rax": 0,
             "rbx": 0,
             "rcx": 0,
             "rdx": 0,
             "rsi": 0,
             "rdi": 0,
             "rbp": 0,
             "rsp": 0}

memory = []
stack = []
heap = b""
heap_address_registers = {"rax": False,
                          "rbx": False,
                          "rcx": False,
                          "rdx": False,
                          "rsi": False,
                          "rdi": False}


class Function:
    def __init__(self, name, instruction_address):
        self.name = name
        self.instruction_address = instruction_address
        self.instructions = []

for i in range(64):
    memory.append(0)

def set_register_value(register_id, value):
    global registers
    registers[register_id] = value
    if len(registers) != 8:
        del registers[register_id]
    
def get_register_value(register_id):
    try:
        return registers[register_id]
    except:
        return None

def show_registers():
    print("instruction:", instructions[instruction_pointer])
    print("rax:", get_register_value("rax"))
    print("rbx:", get_register_value("rbx"))
    print("rcx:", get_register_value("rcx"))
    print("rdx:", get_register_value("rdx"))
    print("rsi:", get_register_value("rsi"))
    print("rdi:", get_register_value("rdi"))
    print("rbp:", get_register_value("rbp"))
    print("rsp:", get_register_value("rsp"))
    print("instruction pointer:", instruction_pointer)
    if z_flag:
        print("z_flag:", 1)
    else:
        print("z_flag:", 0)
    k = 0
    for i in range(8):
        for i in range(8):
            print(f"{memory[k]}", end="")
            k += 1
        print()
    for s in stack:
        print(s)

    input()

def alu(operation, register_one, register_two):
    val_one = register_one
    val_two = register_two
    if register_one not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
        return None
        
    if register_two not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
        val_two = int(register_two)
    
    match(operation):
        case "+":
            # print(val_one)
            # print(val_two)
            set_register_value(register_one, get_register_value(val_one) + get_register_value(val_two))
        case "-":
            set_register_value(register_one, get_register_value(val_one) - get_register_value(val_two))
        case "*":
            set_register_value(register_one, get_register_value(val_one) * get_register_value(val_two))
        case "/":
            set_register_value(register_one, get_register_value(val_one) / get_register_value(val_two))
        case "AND":
            set_register_value(register_one, get_register_value(val_one) and get_register_value(val_two))
        case "OR":
            set_register_value(register_one, get_register_value(val_one) or get_register_value(val_two))
        case "XOR":
            set_register_value(register_one, get_register_value(val_one) ^ get_register_value(val_two))
        case "NAND":
            if not (get_register_value(val_one) and get_register_value(val_two)):
                set_register_value(register_one, 1)
            else:
                set_register_value(register_one, 1)
        case "NOR":
            if not (get_register_value(val_one) or get_register_value(val_two)):
                set_register_value(register_one, 1)
            else:
                set_register_value(register_one, 1)
        case "NXOR":
            if not (get_register_value(val_one) ^ get_register_value(val_two)):
                set_register_value(register_one, 1)
            else:
                set_register_value(register_one, 1)

    return 1

instructions = []

debug_mode = False
file_index = 1
try:
    if sys.argv[1] == "-d":
        debug_mode = True
        file_index = 2
    if sys.argv[2] == "-d":
        debug_mode = True
except:
    pass

try:
    with open(sys.argv[file_index], "rt") as f:
        instructions = f.readlines()
except:
    print(f"Usage: {sys.argv[0]} <FILE>")
    instructions.append("halt")

j = 0
for i in instructions:
    instructions[j] = i.strip().replace(",", "")
    j += 1

functions = []
instruction_pointer = 0
function = False

while instructions[instruction_pointer] != "halt":
    if function:
        functions[-1].instructions.append(instructions[instruction_pointer])
        instruction_pointer += 1
        if instructions[instruction_pointer].split(" ")[0] == "ret":
            function = False
            instruction_pointer += 1
        continue
    try:
        ins = instructions[instruction_pointer].split(" ")[0]
        arg_1 = instructions[instruction_pointer].split(" ")[1]
        arg_2 = instructions[instruction_pointer].split(" ")[2]
        if arg_1.startswith("0x"):
            arg_1 = str(int(arg_1, 16))
        if arg_2.startswith("0x"):
            arg_2 = str(int(arg_2, 16))
    except:
        pass

    match(ins):
        case "mov":
            if arg_1 not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                print("Instruction pointer:", str(instruction_pointer) + "\nWrong use of instruction \"mov\"")
                break
            if arg_2 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                set_register_value(arg_1, get_register_value(arg_2))
            else:
                filtered = arg_2
                if "[" in arg_2 and "]" in arg_2:
                    filtered = arg_2.replace("[", "").replace("]", "")
                    heap_address_registers[arg_1] = True
                set_register_value(arg_1, int(filtered))
        case "add":
            if alu("+", arg_1, arg_2) == None:
                print("Wrong use of instruction add\nInstruction pointer:", instruction_pointer)
                break
        case "sub":
            if alu("-", arg_1, arg_2) == None:
                print("Wrong use of instruction sub\nInstruction pointer:", instruction_pointer)
                break
        case "mul":
            if alu("*", arg_1, arg_2) == None:
                print("Wrong use of instruction mul\nInstruction pointer:", instruction_pointer)
                break
        case "div":
            if alu("/", arg_1, arg_2) == None:
                print("Wrong use of instruction div\nInstruction pointer:", instruction_pointer)
                break
        case "and":
            if alu("AND", arg_1, arg_2) == None:
                print("Wrong use of instruction and\nInstruction pointer:", instruction_pointer)
                break
        case "or":
            if alu("OR", arg_1, arg_2) == None:
                print("Wrong use of instruction or\nInstruction pointer:", instruction_pointer)
                break
        case "xor":
            if alu("XOR", arg_1, arg_2) == None:
                print("Wrong use of instruction xor\nInstruction pointer:", instruction_pointer)
                break
        case "not":
            if alu("NOT", arg_1, arg_2) == None:
                print("Wrong use of instruction not\nInstruction pointer:", instruction_pointer)
                break
        case "nand":
            if alu("NAND", arg_1, arg_2) == None:
                print("Wrong use of instruction nand\nInstruction pointer:", instruction_pointer)
                break
        case "nor":
            if alu("NOR", arg_1, arg_2) == None:
                print("Wrong use of instruction nor\nInstruction pointer:", instruction_pointer)
                break
        case "nxor":
            if alu("NXOR", arg_1, arg_2) == None:
                print("Wrong use of instruction nxor\nInstruction pointer:", instruction_pointer)
                break
        case "jmp":
            if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                instruction_pointer = get_register_value(arg_1)
            else:
                instruction_pointer = int(arg_1)
            if debug_mode:
                show_registers()
            continue
        case "cmp":
            if arg_1 not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"] or arg_2 not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                print("Instruction pointer:", str(instruction_pointer) + "\nWrong use of instruction \"cmp\"")
                break
            if get_register_value(arg_1) == get_register_value(arg_2):
                z_flag = True
            else:
                z_flag = False
        case "je":
            if z_flag:
                if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                    instruction_pointer = get_register_value(arg_1)
                else:
                    instruction_pointer = int(arg_1)
                if debug_mode:
                    show_registers()
                continue
        case "jne":
            if not z_flag:
                if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                    instruction_pointer = get_register_value(arg_1)
                else:
                    instruction_pointer = int(arg_1)
                if debug_mode:
                    show_registers()
                continue
        case "inc":
            set_register_value(arg_1, get_register_value(arg_1) + 1)
        case "dec":
            set_register_value(arg_1, get_register_value(arg_1) - 1)
        case "tgl":
            if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                if memory[get_register_value(arg_1)] == 0:
                    memory[get_register_value(arg_1)] = 1
                else:
                    memory[get_register_value(arg_1)] = 0
            else:
                if memory[int(arg_1)] == 0:
                    memory[int(arg_1)] = 1
                else:
                    memory[int(arg_1)] = 0
        case "imp":
            set_register_value("rax", memory[int(arg_1)])
        case "fnc":
            function = True
            functions.append(Function(arg_1, instruction_pointer))
        case "call":
            # stack.append(instruction_pointer - 1)
            stack.append(instruction_pointer)
            set_register_value("rsp", get_register_value("rsp") + 1)
            stack.append(get_register_value("rbp"))
            set_register_value("rsp", get_register_value("rsp") + 1)
            set_register_value("rbp", get_register_value("rsp"))
            for fnc in functions:
                if fnc.name == arg_1:
                    fnc_calling = fnc
                    instruction_pointer = fnc_calling.instruction_address
                    break
        case "ret":
            if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                set_register_value("rax", get_register_value(arg_1))
            else:
                set_register_value("rax", int(arg_1))
            while True:
                if len(stack) > (get_register_value("rbp") + 1):
                    stack.pop()
                else:
                    break
            set_register_value("rsp", get_register_value("rbp"))
            set_register_value("rbp", stack.pop())
            instruction_pointer = stack.pop() + 1
            set_register_value("rsp", get_register_value("rsp") - 2)
        case "push":
            stack.append(get_register_value(arg_1))
            set_register_value("rsp", get_register_value("rsp") + 1)
        case "pop":
            set_register_value(arg_1, stack.pop(get_register_value("rsp") - 1))
            set_register_value("rsp", get_register_value("rsp") - 1)
        case "gip":
            set_register_value("rax", instruction_pointer)
        case "int":
            if arg_1 != "80":
                print("Instruction pointer:", str(instruction_pointer) + "\nWrong use of instruction \"int\"")
            if get_register_value("rax") == 4:
                count = get_register_value("rcx")
                msg = b""
                try:
                    while True:
                        msg = msg + bytes([heap[count]])
                        count += 1
                except:
                    pass

                msg = msg[:get_register_value("rdx")]
                for i in msg:
                    sys.stdout.write(chr(i))
                    sys.stdout.flush()
            elif get_register_value("rax") == 3:
                line = ""
                for i in sys.stdin:
                    line += i
                    if i[-1] == '\n':
                        break
                line = line.rstrip()[:get_register_value("rdx")]
                counter = get_register_value("rcx")
                for i in line:
                    heap = heap[:counter] + bytes([ord(i)]) + heap[counter+1:]
                    counter += 1
        case ".store":
            heap += ast.literal_eval("b" + arg_1)
        case _:
            if ins != "nop":
                print("Instruction pointer:", str(instruction_pointer) + "\nUnknown instruction:", ins)
    if debug_mode:
        show_registers()
    instruction_pointer += 1
    if ins == "halt" or instruction_pointer == len(instructions):
        break

#!/usr/bin/python3

import sys
import ast

z_flag = False
registers = {"A":  0,
             "X":  0,
             "Y":  0,
             "SP": 0,
             "PC": 0,
             "P":  0x00000000}

flags = {"N": False,
         "V": False,
         "-": False,
         "B": False,
         "D": False,
         "I": False,
         "Z": False,
         "C": False}

memory = b"\x00" * (65535)

class Function:
    def __init__(self, name, instruction_address):
        self.name = name
        self.instruction_address = instruction_address
        self.instructions = []

def set_register_value(register_id, value):
    global registers
    registers[register_id] = value
    if len(registers) != 6:
        del registers[register_id]
    
def get_register_value(register_id):
    try:
        return registers[register_id]
    except:
        return None

def modify_status_register():
    converted = 0
    converted += 0x80 if flags["N"] else 0
    converted += 0x40 if flags["V"] else 0
    converted += 0x20 if flags["-"] else 0
    converted += 0x10 if flags["B"] else 0
    converted += 0x08 if flags["D"] else 0
    converted += 0x04 if flags["I"] else 0
    converted += 0x02 if flags["Z"] else 0
    converted += 0x01 if flags["C"] else 0
    set_register_value("P", converted)

def show_registers():
    print("instruction:", instructions[get_register_value("PC") - 1])
    print("A:", get_register_value("A"), hex(get_register_value("A")))
    print("X:", get_register_value("X"), hex(get_register_value("X")))
    print("Y:", get_register_value("Y"), hex(get_register_value("Y")))
    print("SP:", get_register_value("SP"), hex(get_register_value("SP")))
    print("PC:", get_register_value("PC"), hex(get_register_value("PC")))
    print("P:", get_register_value("P"), hex(get_register_value("P")))
    if flags["N"]:
        print("n_flag:", 1)
    else:
        print("n_flag:", 0)
    if flags["V"]:
        print("v_flag:", 1)
    else:
        print("v_flag:", 0)
    if flags["-"]:
        print("-_flag:", 1)
    else:
        print("-_flag:", 0)
    if flags["B"]:
        print("b_flag:", 1)
    else:
        print("b_flag:", 0)
    if flags["D"]:
        print("d_flag:", 1)
    else:
        print("d_flag:", 0)
    if flags["I"]:
        print("i_flag:", 1)
    else:
        print("i_flag:", 0)
    if flags["Z"]:
        print("z_flag:", 1)
    else:
        print("z_flag:", 0)
    if flags["C"]:
        print("c_flag:", 1)
    else:
        print("c_flag:", 0)

    print("stack:")
    i = 0x0100
    while i < (0x0100 + get_register_value("SP")):
        print(memory[i], hex(memory[i]))
        i += 1
    input()

def alu(operation, register_one, register_two):
    val_one = register_one
    val_two = register_two
    if register_one not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
        return None
        
    if register_two not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
        match(operation):
            case "+":
                # print(val_one)
                # print(val_two)
                set_register_value(register_one, get_register_value(val_one) + val_two)
            case "-":
                set_register_value(register_one, get_register_value(val_one) - val_two)
            case "*":
                set_register_value("rax", get_register_value("rax") * val_two)
            case "/":
                set_register_value("rax", (get_register_value(val_one) - (get_register_value(val_one) % val_two)) / val_two)
                set_register_value("rdx", get_register_value(val_one) % val_two)
            case "AND":
                set_register_value(register_one, get_register_value(val_one) and val_two)
            case "OR":
                set_register_value(register_one, get_register_value(val_one) or val_two)
            case "XOR":
                set_register_value(register_one, get_register_value(val_one) ^ val_two)
            case "NAND":
                if not (get_register_value(val_one) and val_two):
                    set_register_value(register_one, 1)
                else:
                    set_register_value(register_one, 0)
            case "NOR":
                if not (get_register_value(val_one) or val_two):
                    set_register_value(register_one, 1)
                else:
                    set_register_value(register_one, 0)
            case "NXOR":
                if not (get_register_value(val_one) ^ val_two):
                    set_register_value(register_one, 1)
                else:
                    set_register_value(register_one, 0)
    else:    
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
                set_register_value("rax", (get_register_value(val_one) - (get_register_value(val_one) % get_register_value(val_two))) / get_register_value(val_two))
                set_register_value("rdx", get_register_value(val_one) % get_register_value(val_two))
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
                    set_register_value(register_one, 0)
            case "NOR":
                if not (get_register_value(val_one) or get_register_value(val_two)):
                    set_register_value(register_one, 1)
                else:
                    set_register_value(register_one, 0)
            case "NXOR":
                if not (get_register_value(val_one) ^ get_register_value(val_two)):
                    set_register_value(register_one, 1)
                else:
                    set_register_value(register_one, 0)

    return 1

def set_flags():
    converted = get_register_value("P")
    flags["N"] = 1 if get_register_value("P") & 0x80 else 0
    flags["V"] = 1 if get_register_value("P") & 0x40 else 0
    flags["-"] = 1 if get_register_value("P") & 0x20 else 0
    flags["B"] = 1 if get_register_value("P") & 0x10 else 0
    flags["D"] = 1 if get_register_value("P") & 0x08 else 0
    flags["I"] = 1 if get_register_value("P") & 0x04 else 0
    flags["Z"] = 1 if get_register_value("P") & 0x02 else 0
    flags["C"] = 1 if get_register_value("P") & 0x01 else 0
    set_register_value("P", converted)

def push_stack(accumulator):
    global memory
    if accumulator:
        data = get_register_value("A")
    else:
        flags["B"] = True
    memorylist = list(memory)
    if 0x100 + get_register_value("SP") >= 0x1ff:
        stack_end = 0x0100
    modify_status_register()
    if not accumulator:
        data = get_register_value("P")
    memorylist[0x0100 + get_register_value("SP")] = int(data)
    set_register_value("SP", get_register_value("SP") + 1)
    memory = bytes(memorylist)
    
def pop_stack(accumulator):
    global memory
    modify_status_register()
    memory_list = list(memory)
    if accumulator:
        set_register_value("A", memory_list[0x0ff + get_register_value("SP")])
    else:
        set_register_value("P", memory_list[0x0ff + get_register_value("SP")])
        set_flags()
    memory_list[0x0100 + get_register_value("SP")] = 0
    set_register_value("SP", get_register_value("SP") - 1)

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

entry_point = 0
j = entry_point
for i in instructions:
    instructions[j] = i.strip().replace(",", "").lower()
    j += 1

functions = []
set_register_value("PC", entry_point)
function = False
ins = ""


while instructions[get_register_value("PC")] != "halt":
    if function:
        functions[-1].instructions.append(memory[get_register_value("PC")])
        set_register_value("PC", get_register_value("PC") + 1)
        if memory[get_register_value("PC")].split(" ")[0] == "ret":
            function = False
            set_register_value("PC", get_register_value("PC") + 1)
        continue
    try:
        arg_1 = ""
        arg_2 = ""
        ins_split_len = len(instructions[get_register_value("PC")].split(" "))
        ins = instructions[get_register_value("PC")].split(" ")[0]
        if ins_split_len > 1:
            arg_1 = instructions[get_register_value("PC")].split(" ")[1]
            org_arg1 = arg_1
        if ins_split_len > 2:
            arg_2 = instructions[get_register_value("PC")].split(" ")[2]
            org_arg2 = arg_2
        if arg_1.startswith("#$"):
            arg_1 = str(int("0x" + arg_1.replace("#$", ""), 16))
        elif arg_1.startswith("$"):
            arg_1 = str(memory[int("0x" + arg_1.replace("$", ""), 16)])
        elif arg_1 == "":
            pass
        elif arg_1 in ["A", "X", "Y"]:
            pass
        else:
            print(f"Program counter {get_register_value("PC")}\nInstruction: {ins}\nError: Instruction cannot take that type argument")
            break
        if arg_2.startswith("#$"):
            arg_2 = str(int("0x" + arg_2.replace("#$", ""), 16))
        elif arg_2.startswith("$"):
            arg_2 = str(memory[int("0x" + arg_2.replace("$", ""), 16)])
        elif arg_2 == "":
            pass
        elif arg_2 in ["A", "X", "Y"]:
            pass
        else:
            print(f"Program counter {get_register_value("PC")}\nInstruction: {ins}\nError: Instruction cannot take that type argument")
            break
            
    except:
        pass

    match(ins):
        case "lda":
            set_register_value("A", int(arg_1))
        case "ldx":
            set_register_value("X", int(arg_1))
        case "ldy":
            set_register_value("Y", int(arg_1))
        case "tax":
            set_register_value("X", get_register_value("A"))
        case "txa":
            set_register_value("A", get_register_value("X"))
        case "tay":
            set_register_value("Y", get_register_value("A"))
        case "tya":
            set_register_value("A", get_register_value("Y"))
        case "sta":
            if int(org_arg1.replace("$", "0x"), 16) > 32768:
                print(f"Program counter {get_register_value("PC")}\nError: Instruction \"STA\" cannot take memory address greater than 0x8000")
                break
            memory_list = list(memory)
            memory_list[int(org_arg1.replace("$", "0x"), 16)] = get_register_value("A")
            memory = bytes(memory_list)
        case "stx":
            if int(org_arg1.replace("$", "0x"), 16) > 32768:
                print(f"Program counter {get_register_value("PC")}\nError: Instruction \"STA\" cannot take memory address greater than 0x8000")
                break
            memory_list = list(memory)
            memory_list[int(org_arg1.replace("$", "0x"), 16)] = get_register_value("X")
            memory = bytes(memory_list)
        case "sty":
            if int(org_arg1.replace("$", "0x"), 16) > 32768:
                print(f"Program counter {get_register_value("PC")}\nError: Instruction \"STA\" cannot take memory address greater than 0x8000")
                break
            memory_list = list(memory)
            memory_list[int(org_arg1.replace("$", "0x"), 16)] = get_register_value("Y")
            memory = bytes(memory_list)
        case "pha":
            push_stack(True)
        case "pla":
            pop_stack(True)
        case "php":
            push_stack(False)
        case "plp":
            pop_stack(False)
        case "inc":
            set_register_value("A", get_register_value("A") + 1)
        case "inx":
            set_register_value("X", get_register_value("X") + 1)
        case "iny":
            set_register_value("Y", get_register_value("Y") + 1)
        case "dec":
            set_register_value("A", get_register_value("A") - 1)
        case "dex":
            set_register_value("X", get_register_value("X") - 1)
        case "dey":
            set_register_value("Y", get_register_value("Y") - 1)
        case "clc":
            flags["C"] = False
        case "sec":
            flags["C"] = True
        case "cld":
            flags["D"] = False
        case "sed":
            flags["D"] = True
        case "cli":
            flags["I"] = False
        case "sei":
            flags["I"] = True
        case "clv":
            flags["V"] = False
        case "add":
            if alu("+", arg_1, arg_2) == None:
                print("Wrong use of instruction add\nInstruction pointer:", get_register_value("PC"))
                break
        case "sub":
            if alu("-", arg_1, arg_2) == None:
                print("Wrong use of instruction sub\nInstruction pointer:", get_register_value("PC"))
                break
        case "mul":
            if alu("*", arg_1, arg_2) == None:
                print("Wrong use of instruction mul\nInstruction pointer:", get_register_value("PC"))
                break
        case "div":
            if alu("/", arg_1, arg_2) == None:
                print("Wrong use of instruction div\nInstruction pointer:", get_register_value("PC"))
                break
        case "and":
            if alu("AND", arg_1, arg_2) == None:
                print("Wrong use of instruction and\nInstruction pointer:", get_register_value("PC"))
                break
        case "or":
            if alu("OR", arg_1, arg_2) == None:
                print("Wrong use of instruction or\nInstruction pointer:", get_register_value("PC"))
                break
        case "xor":
            if alu("XOR", arg_1, arg_2) == None:
                print("Wrong use of instruction xor\nInstruction pointer:", get_register_value("PC"))
                break
        case "not":
            if alu("NOT", arg_1, arg_2) == None:
                print("Wrong use of instruction not\nInstruction pointer:", get_register_value("PC"))
                break
        case "nand":
            if alu("NAND", arg_1, arg_2) == None:
                print("Wrong use of instruction nand\nInstruction pointer:", get_register_value("PC"))
                break
        case "nor":
            if alu("NOR", arg_1, arg_2) == None:
                print("Wrong use of instruction nor\nInstruction pointer:", get_register_value("PC"))
                break
        case "nxor":
            if alu("NXOR", arg_1, arg_2) == None:
                print("Wrong use of instruction nxor\nInstruction pointer:", get_register_value("PC"))
                break
        case "jmp":
            if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                set_register_value("PC", get_register_value(arg_1))
            else:
                set_register_value("PC", int(arg_1))
            if debug_mode:
                show_registers()
            continue
        case "cmp":
            if arg_1 not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"] or arg_2 not in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                print("Instruction pointer:", str(get_register_value("PC")) + "\nWrong use of instruction \"cmp\"")
                break
            if get_register_value(arg_1) == get_register_value(arg_2):
                z_flag = True
            else:
                z_flag = False
        case "je":
            if z_flag:
                if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                    set_register_value("PC", get_register_value(arg_1))
                else:
                    set_register_value("PC", int(arg_1))
                if debug_mode:
                    show_registers()
                continue
        case "jne":
            if not z_flag:
                if arg_1 in ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp"]:
                    set_register_value("PC", get_register_value(arg_1))
                else:
                    set_register_value("PC", int(arg_1))
                if debug_mode:
                    show_registers()
                continue
        case "inc":
            set_register_value(arg_1, get_register_value(arg_1) + 1)
        case "dec":
            set_register_value(arg_1, get_register_value(arg_1) - 1)
        case "fnc":
            function = True
            functions.append(Function(arg_1, instruction_pointer))
        case "call":
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
            push_stack(get_register_value(arg_1))
        case "pop":
            set_register_value(arg_1, pop_stack())
        case "gip":
            set_register_value("rax", instruction_pointer)
        case "int":
            if arg_1 != "80":
                print("Instruction pointer:", str(instruction_pointer) + "\nWrong use of instruction \"int\"")
            if get_register_value("rax") == 4:
                count = get_register_value("rcx")
                msg = b""
                try:
                    while count < (get_register_value("rcx") + get_register_value("rdx")):
                        msg = msg + bytes([memory[count]])
                        count += 1
                except:
                    pass

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
                    memory = memory[:counter] + bytes([ord(i)]) + memory[counter+1:]
                    counter += 1
            elif get_register_value("rax") == 1:
                sys.exit(get_register_value("rbx"))
        case ".store":
            mem_list = list(memory)
            bytes_to_store = ast.literal_eval("b" + arg_1)
            for i in bytes_to_store:
                mem_list[heap_end] = i
                heap_end += 1
            memory = bytes(mem_list)
            heap += ast.literal_eval("b" + arg_1)
        case "loop":
            if get_register_value("rcx") != 0:
                set_register_value("rcx", get_register_value("rcx") - 1)
                instruction_pointer = int(arg_1) - 1
        case _:
            if ins != "nop":
                print("Program counter:", str(get_register_value("PC")) + "\nUnknown instruction:", ins)
    modify_status_register()
    set_register_value("PC", get_register_value("PC") + 1)
    flags["-"] = True
    if debug_mode:
        show_registers()
    if ins == "halt" or get_register_value("PC") == len(instructions):
        break

sys.exit(-1)

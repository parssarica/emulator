#!/usr/bin/python3

import sys
import ast
import ctypes
import sdl2
import sdl2.ext

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
try:
    with open("config.toml", "rt") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("Create a config.toml file to specify the settings.")
    sys.exit(1)

entry_point = 0
cpu_type = ""
create_screen = False
for line in lines:
    if line == "[config]":
        pass
    match(line.split("=")[0].strip()):
        case "cpu_type":
            cpu_type = line.split("=")[1].strip().replace("\"", "")
        case "debug_mode":
            debug_mode = True if line.split("=")[1].strip() == "1" else False
        case "entry_point":
            entry_point = int(line.split("=")[1].strip(), 16)
        case "file":
            file = line.split("=")[1].strip().replace("\"", "")
            try:
                with open(file, "rt") as f:
                    instructions = f.readlines()
            except:
                print(f"File {file} not found.")
                instructions.append("halt")
        case "create_screen":
            create_screen = True if line.split("=")[1].strip() == "1" else False

j = entry_point
for i in instructions:
    instructions[j] = i.strip().replace(",", "").lower()
    j += 1

functions = []
set_register_value("PC", entry_point)
function = False
ins = ""

if create_screen:
    sdl2.ext.init()
    window = sdl2.ext.Window("Commodore 64 Emulator", size=(320,200))
    window.show()
    renderer=sdl2.SDL_CreateRenderer(window.window, -1, 0)
    texture = sdl2.SDL_CreateTexture(renderer, sdl2.SDL_PIXELFORMAT_ARGB8888, sdl2.SDL_TEXTUREACCESS_STREAMING, 320, 200)
    event = sdl2.SDL_Event()

exit_code = -1

while instructions[get_register_value("PC")] != "halt":
    if create_screen:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_QUIT:
                instructions = ["halt"]
                set_register_value("PC", 0)
        pixels = ctypes.c_void_p()
        pitch = ctypes.c_int()
        sdl2.SDL_LockTexture(texture, None, ctypes.byref(pixels), ctypes.byref(pitch))
        pixel_ptr = ctypes.cast(pixels, ctypes.POINTER(ctypes.c_uint32))
        for y in range(200):
            for x in range(320):
                match(memory[0xd000 + y*200 + x]):
                    case 0x00:
                        red = 0
                        green = 0
                        blue = 0
                    case 0x01:
                        red = 255
                        green = 255
                        blue = 255
                    case 0x02:
                        red = 0x88
                        green = 0
                        blue = 0
                    case 0x03:
                        red = 0xaa
                        green = 0xff
                        blue = 0xee
                    case 0x04:
                        red = 0xcc
                        green = 0x44
                        blue = 0xcc
                    case 0x05:
                        red = 0x0
                        green = 0xcc
                        blue = 0x55
                    case 0x06:
                        red = 0
                        green = 0
                        blue = 0xaa
                    case 0x07:
                        red = 0xee
                        green = 0xee
                        blue = 0x77
                    case 0x08:
                        red = 0xdd
                        green = 0x88
                        blue = 0x55
                    case 0x09:
                        red = 0x66
                        green = 0x44
                        blue = 0
                    case 0x0A:
                        red = 0xff
                        green = 0x77
                        blue = 0x77
                    case 0x0B:
                        red = 0x33
                        green = 0x33
                        blue = 0x33
                    case 0x0C:
                        red = 0x77
                        green = 0x77
                        blue = 0x77
                    case 0x0D:
                        red = 0xaa
                        green = 0xff
                        blue = 0x66
                    case 0x0E:
                        red = 0x00
                        green = 0x88
                        blue = 0xff
                    case 0x0F:
                        red = 0xbb
                        green = 0xbb
                        blue = 0xbb
                    case _:
                        red = 0
                        green = 0
                        blue = 0
                        
                color = (255 << 24) | (red << 16) | (green << 8) | blue
                pixel_ptr[y * (pitch.value // 4) + x]
        sdl2.SDL_RenderClear(renderer)
        sdl2.SDL_RenderCopy(renderer, texture, None, None)
        sdl2.SDL_RenderPresent(renderer)
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

if create_screen:
    sdl2.SDL_DestroyTexture(texture)
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.ext.quit()

sys.exit(exit_code)

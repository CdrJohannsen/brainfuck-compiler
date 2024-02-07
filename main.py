#!/usr/bin/env python3
import sys, os

if len(sys.argv) < 2:
    print("Needs file to convert")
    exit()


with open(sys.argv[1], "r") as f:
    file = f.read()

unmatched = []
brackets = {}

translation = {}
for char in range(len(file)):
    if not file[char] in [">","<","+","-",".",",","[","]","#"]:
        translation[ord(file[char])] = None
file=file.translate(translation)

for char in range(len(file)):
    if file[char] == "[":
        unmatched.append(char)
    elif file[char] == "]":
        brackets[unmatched[-1]] = char
        brackets[char] = unmatched[-1]
        del unmatched[-1]

res_file = bytearray()
out_file = bytearray()


addr = {}
segments = {
    "right": None,
    "left": None,
    "inc": None,
    "dec": None,
    "write": None,
    "read": None,
    "left_br": None,
    "right_br": None,
    "debug": None,
    "ex": None,
    "c_off": None,
    "c_on": None,
    "w_term": None,
    "r_term": None
}

def mov(to:str, number:int)->list:
    match to:
        case "rax":
            return [0xB8,number]
        case "rdx":
            return [0xBA,number]
        case "rdi":
            return [0xBF,number]
        case "dil":
            return [0x40,0xB7,number]
        case _:
            print(f"Missing mov config for {to}")
            exit()

def syscall()->list:
    return [0x0F,0x05]

def get_addr(label):
    return addr[label]


class Segment:
    addr = 0
    addr_len = 4
    content = list()
    length = 0

    def __init__(self) -> None:
        global res_file
        res_file.extend(self.res_bytes())
        self.addr = len(res_file)

    def get_addr(self, length:int) -> bytearray:
        return bytearray(self.addr.to_bytes(length))

    def get_rel_addr(self,addr:int, length:int) -> bytearray:
        return bytearray((self.addr-addr).to_bytes(length,signed=True))

    def get_call(self,addr:int) -> bytearray:
        return bytearray([0xE8])+(self.addr+addr).to_bytes(4)

    def get_content(self):
        return bytearray([i if type(i) == type(int) else i.get_call() for i in self.content]+[0xC3])

    def res_bytes(self):
        return bytearray(self.length)

class EHdr(Segment):
    def __init__(self,addr,memsz,flags=5,offset=[0]*8):
        self.content = ([
            0x7F,0x45,0x4C,0x46,2,1,1,0,    # e_ident
            0,0,0,0,0,0,0,0,
            2,0,                            # e_type
            0x3E,0,                         # e_machine
            1,0,0,0]+                       # e_version
            get_addr("_start")+             # e_entry
            [0x40,0,0,0,0,0,0,0]+           # e_phoff
            get_addr("shdr")+               # e_shoff
            [0,0,0,0,                       # e_flags
            64,0,                           # e_ehsize
            0x38,0,                         # e_phentsize
            3,0,                            # e_phnum
            0x40,0,                         # e_shentsize
            4,0,                            # e_shnum
            3,0]                            # e_shstrndx
        )

class PHdr(Segment):
    def __init__(self,addr,memsz,flags=5,offset=[0]*8):
        self.content = ([
            1,0,0,0,                        # p_type
            flags,0,0,0]+                   # p_flags
            offset+                         # p_offset
            addr+                           # p_vaddr
            addr+                           # p_paddr
            self.length+                         # p_filesz
            memsz+                          # p_memsz
            [0,0x10,0,0,0,0,0,0]            # p_align
            )

class RTerm(Segment):
    pass

class WTerm(Segment):
    pass

class COff(Segment):
    def __init__(self):
        self.content = [segments["r_term"],segments["w_term"]]
        super().__init__()

class COn(Segment):
    def __init__(self):
        self.content = [segments["r_term"],segments["w_term"]]
        super().__init__()

class Right(Segment):
    def __init__(self):
        self.content = [0x48,0xFF,0xC3]
        super().__init__()

class Left(Segment):
    def __init__(self):
        self.content = [0x48,0xFF,0xCB]
        super().__init__()

class Inc(Segment):
    def __init__(self):
        self.content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xC7]+[0x40,0x88,0x3B]
        super().__init__()

class Dec(Segment):
    def __init__(self):
        self.content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xCF]+[0x40,0x88,0x3B]
        super().__init__()

class Write(Segment):
    def __init__(self):
        self.content = mov("rax",1)+mov("rdi",1)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()
        super().__init__()

class Read(Segment):
    def __init__(self):
        self.content = [segments["c_off"]]+mov("rax",0)+mov("dil",0)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()+[segments["c_on"]]
        super().__init__()

class LeftBr(Segment):
    pass

class RightBr(Segment):
    pass

class Exit(Segment):
    def __init__(self):
        self.content = mov("rax",60)+[0x48,0x8B,0x3B]+syscall()
        super().__init__()

    def get_call(self,addr) -> bytearray:
        return bytearray([0xE9])+self.get_rel_addr(addr,4)

class Debug(Segment):
    pass

segments["right"] = Right()
segments["left"] = Left()
segments["inc"] = Inc()
segments["dec"] = Dec()
segments["write"] = Write()
segments["read"] = Read()
segments["left_br"] = LeftBr()
segments["right_br"] = RightBr()
segments["debug"] = Debug()
segments["ex"] = Exit()
segments["c_off"] = COff()
segments["c_on"] = COn()
segments["w_term"] = WTerm()
segments["r_term"] = RTerm()




########################################
# Parse file
########################################
step = 0
while step < len(file):
    if file[step] == ">":
        out_file.extend(segments["right"].get_call(len(out_file)))
    elif file[step] == "<":
        out_file.extend(segments["left"].get_call(len(out_file)))
    elif file[step] == "+":
        out_file.extend(segments["inc"].get_call(len(out_file)))
    elif file[step] == "-":
        out_file.extend(segments["dec"].get_call(len(out_file)))
    elif file[step] == ".":
        out_file.extend(segments["write"].get_call(len(out_file)))
    elif file[step] == ",":
        out_file.extend(segments["read"].get_call(len(out_file)))
    elif file[step] == "[":
        out_file.extend(segments["left_br"].get_call(len(out_file)))
    elif file[step] == "]":
        out_file.extend(segments["right_br"].get_call(len(out_file)))
    elif file[step] == "#":
        out_file.extend(segments["debug"].get_call(len(out_file)))
    step += 1

out_file.extend(segments["ex"].get_call(len(out_file)))
with open("out.out", "wb") as f:
    f.write(out_file)

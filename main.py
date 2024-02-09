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

base_addr = 0x400000
res_file = bytearray()
out_file = []


data = {}

sections = {".shstrtab":None}
programms = {}

segments = {
    "c_off": None,
    "c_on": None,
    "r_term": None,
    "w_term": None,
    "write": None,
    "read": None,
    "inc": None,
    "dec": None,
    "right": None,
    "left": None,
    # "left_br": None,
    # "right_br": None,
    # "debug": None,
    "ex": None,
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
        case "rsi":
            return [0x48,0xBE]+list(bytearray(number.to_bytes(2)))
        case _:
            print(f"Missing mov config for {to}")
            exit()

def syscall()->list:
    return [0x0F,0x05]

def get_addr(addr:int,length:int=8):
    return list(addr.to_bytes(length,byteorder="little"))


class Segment:
    off = 0
    addr_len = 4
    content = list()
    length = 0

    def __init__(self) -> None:
        global res_file
        res_file.extend(self.res_bytes())
        self.off = len(res_file)

    def get_addr(self, length:int) -> list:
        return list((base_addr+self.off).to_bytes(length,"little"))

    def get_off(self, length:int) -> list:
        return list(self.off.to_bytes(length,"little"))

    def get_rel_off(self,addr:int, length:int) -> list:
        return list((self.off-addr).to_bytes(length,"little",signed=True))

    def get_content(self):
        return self.content

    def res_bytes(self):
        return bytearray(self.length)

class Function(Segment):
    def get_call(self,off:int) -> list:
        return [0xE8]+self.get_rel_off(off,4)

    def get_content(self):
        return [i if type(i) == int else i.get_call(self.off) for i in self.content]+[0xC3]


class EHdr(Segment):
    def __init__(self) -> None:
        self.content = ([
            0x7F,0x45,0x4C,0x46,2,1,1,0,    # e_ident
            0,0,0,0,0,0,0,0,
            2,0,                            # e_type
            0x3E,0,                         # e_machine
            1,0,0,0]+                       # e_version
            sections[".text"].get_entry()+  # e_entry
            [0x40,0,0,0,0,0,0,0]+           # e_phoff
            sections[".shstrtab"].header.get_addr(8)+               # e_shoff
            [0,0,0,0,                       # e_flags
            64,0,                           # e_ehsize
            0x38,0,                         # e_phentsize
            3,0,                            # e_phnum
            0x40,0,                         # e_shentsize
            len(sections),0,                # e_shnum
            0,0]                            # e_shstrndx
        )
        super().__init__()

class PHdr(Segment):
    def __init__(self,addr,filesz,memsz,flags=5,offset=0) -> None:
        self.length = 0x38
        self.content = ([
            1,0,0,0,                        # p_type
            flags,0,0,0]+                   # p_flags
            get_addr(offset,8)+                         # p_offset
            addr+                           # p_vaddr
            addr+                           # p_paddr
            get_addr(filesz,8)+             # p_filesz
            get_addr(memsz,8)+              # p_memsz
            [0,0x10,0,0,0,0,0,0]            # p_align
            )
        super().__init__()

class SHdr(Segment):
    def __init__(self,name,typ,flags,addr:list,offset:list) -> None:
        self.content = ([
            name,0,0,0,                     # sh_name
            typ,0,0,0,                      # sh_type
            flags,0,0,0,0,0,0,0]+           # sh_flags
            addr+                           # sh_addr
            offset+                         # sh_offset
            list(self.length.to_bytes(8,"little"))+  # sh_size
            [0,0,0,0,                       # sh_link
             0,0,0,0,                       # sh_info
             4,0,0,0,0,0,0,0,               # sh_addralign
             0,0,0,0,0,0,0,0]               # sh_entsize
            )
        super().__init__()

class Section(Segment):
    def __init__(self,name:str) -> None:
        self.name = name
        sections[name] = self
        self.index = sections[".shstrtab"].add_section(name)
        if not type(super()) == type(Bss):
            super().__init__()

class Shstrtab(Section):
    def __init__(self) -> None:
        self.names = []
        super().__init__(".shstrtab")
        self.header = SHdr(self.index,3,0,[0]*8,self.get_off(8))

    def add_section(self,name) -> int:
        self.names.append(name+"\x00")
        return len(self.names)-1

class Bss(Section):
    def __init__(self) -> None:
        super().__init__(".bss")
        self.off = 0x3000
        self.header = SHdr(self.index,8,3,[0]*8,self.get_off(8)) # TODO adress

class Text(Section):
    def __init__(self) -> None:
        super().__init__(".text")
        self.header = SHdr(self.index,1,6,[0]*8,self.get_off(8)) # TODO adress
        self.entrypoint = 0
        self.off = 0x1000
        self.length = len(self.get_content())

    def get_entry(self):
        content = []
        for segment in segments.values():
            content.extend(segment.get_content())
        self.entrypoint = len(content)+self.off
        return list(self.entrypoint.to_bytes(8,byteorder="little"))

    def get_content(self) -> list:
        step = 0
        content = []
        for segment in segments.values():
            content.extend(segment.get_content())
        while step < len(file):
            if file[step] == ">":
                content.extend(segments["right"].get_call(len(content)))
            elif file[step] == "<":
                content.extend(segments["left"].get_call(len(content)))
            elif file[step] == "+":
                content.extend(segments["inc"].get_call(len(content)))
            elif file[step] == "-":
                content.extend(segments["dec"].get_call(len(content)))
            elif file[step] == ".":
                content.extend(segments["write"].get_call(len(content)))
            elif file[step] == ",":
                content.extend(segments["read"].get_call(len(content)))
            elif file[step] == "[":
                content.extend(segments["left_br"].get_call(len(content)))
            elif file[step] == "]":
                content.extend(segments["right_br"].get_call(len(content)))
            elif file[step] == "#":
                content.extend(segments["debug"].get_call(len(content)))
            step += 1
        content.extend(segments["ex"].get_call(len(content)))
        return content

sections[".shstrtab"] = Shstrtab()
Bss()

class RTerm(Function):
    def __init__(self):
        self.content = mov("rax",16)+mov("rdi",0)+mov("rsi",0x5401)+[0x48,0xBA]+get_addr(sections[".bss"].off)+syscall()

class WTerm(Function):
    def __init__(self):
        self.content = mov("rax",16)+mov("rdi",0)+mov("rsi",0x5402)+[0x48,0xBA]+get_addr(sections[".bss"].off)+syscall()

segments["w_term"] = WTerm()
segments["r_term"] = RTerm()

class COff(Function):
    def __init__(self):
        self.content = [segments["r_term"],0x83,0x24,0x25]+get_addr(sections[".bss"].off+12,4)+[0xFD,segments["w_term"]]
        super().__init__()

class COn(Function):
    def __init__(self):
        self.content = [segments["r_term"],0x83,0x0C,0x25]+get_addr(sections[".bss"].off+12,4)+[0x02,segments["w_term"]]
        super().__init__()


segments["c_off"] = COff()
segments["c_on"] = COn()

class Right(Function):
    def __init__(self):
        self.content = [0x48,0xFF,0xC3]
        super().__init__()

class Left(Function):
    def __init__(self):
        self.content = [0x48,0xFF,0xCB]
        super().__init__()

class Inc(Function):
    def __init__(self):
        self.content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xC7]+[0x40,0x88,0x3B]
        super().__init__()

class Dec(Function):
    def __init__(self):
        self.content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xCF]+[0x40,0x88,0x3B]
        super().__init__()

class Write(Function):
    def __init__(self):
        self.content = mov("rax",1)+mov("rdi",1)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()
        super().__init__()

class Read(Function):
    def __init__(self):
        self.content = [segments["c_off"]]+mov("rax",0)+mov("dil",0)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()+[segments["c_on"]]
        super().__init__()

class LeftBr(Function):
    pass

class RightBr(Function):
    pass

class Exit(Function):
    def __init__(self):
        self.content = mov("rax",60)+[0x48,0x8B,0x3B]+syscall()
        super().__init__()

    def get_call(self,off) -> list:
        return [0xE9]+self.get_rel_off(off,4)

class Debug(Function):
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

Text()
out_file.extend(EHdr().get_content())
out_file.extend(PHdr(get_addr(base_addr),0xE8,0xE8,4).get_content())
out_file.extend(PHdr(
    get_addr(sections[".text"].off+base_addr),
    0xE8+sections[".text"].length,
    0xE8+sections[".text"].length,
    5,
    0x1000
).get_content())
out_file.extend(PHdr(get_addr(sections[".bss"].off+base_addr),0,30040,6).get_content())
out_file += [0] * (0x1000-len(out_file))
out_file.extend(sections[".text"].get_content())
out_file.extend(sections[".shstrtab"].get_content())
out_file.extend(sections[".shstrtab"].header.get_content())
out_file.extend(sections[".text"].header.get_content())
out_file.extend(Bss().header.get_content())

def flatten(in_list):
    out_list = []
    for element in in_list:
        if type(element) == list:
            for i in element:
                out_list.append(i)
        else:
            out_list.append(element)
    return out_list

out_file = flatten(out_file)
out_file = bytearray(out_file)

with open("out.out", "wb") as f:
    f.write(out_file)

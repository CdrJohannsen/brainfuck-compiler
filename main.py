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

res_file = bytearray()
out_file = []
s_names = ""


data = {}

sections = {}
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

def flatten(in_list):
    out_list = []
    for element in in_list:
        if type(element) == list:
            for i in element:
                if type(i) == Address:
                    out_list.extend(i.get())
                else:
                    out_list.append(i)
        elif type(element) == Address:
            out_list.extend(element.get())
        elif type(element) == int:
            out_list.append(element)
        else:
            print(f"Can't flatten out_list. {element} has type {type(element)}")
            exit()
    return out_list

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

class Address():
    def __init__(self,off:int,pref_len:int=8,pref_type:str="off") -> None:
        self.off = off
        self.pref_len = pref_len
        self.pref_type = pref_type

    def get_off(self,length:int=0) -> list:
        if not length:
            length = self.pref_len
        return list(self.off.to_bytes(length,byteorder="little",signed=True))

    def get_addr(self,length:int=0) -> list:
        if not length:
            length = self.pref_len
        return list((self.off+base_addr.off).to_bytes(length,byteorder="little",signed=True))

    def get(self,length:int=0) -> list:
        if not length:
            length = self.pref_len
        if self.pref_type == "off":
            return self.get_off(length)
        elif self.pref_type == "addr":
            return self.get_addr(length)
        else:
            print(f"Address type {self.pref_type} not avaliable!")
            exit()

    def __add__(self,a):
        if type(a) == int:
            return Address(self.off+a,self.pref_len,self.pref_type)
        else:
            return Address(self.off+a.off,self.pref_len,self.pref_type)
        
    def __sub__(self,a):
        if type(a) == int:
            return Address(self.off-a,self.pref_len,self.pref_type)
        else:
            return Address(self.off-a.off,self.pref_len,self.pref_type)
    
    def update(self,off=None,pref_len=8,pref_type=None):
        if not off == None:
            self.off = off
        if not pref_len == None:
            self.pref_len = pref_len
        if not pref_type == None:
            self.pref_type = pref_type

    def copy(self,f):
        self.off = f.off
        self.pref_len = f.pref_len
        self.pref_type = f.pref_type
        
base_addr = Address(0x400000)
shdr_start = Address(0)

bracket_addr = {}

for char in range(len(file)):
    if file[char] == "[":
        unmatched.append(char)
        bracket_addr[char] = Address(0,4)
    elif file[char] == "]":
        brackets[unmatched[-1]] = char
        brackets[char] = unmatched[-1]
        bracket_addr[char] = Address(0,4)
        del unmatched[-1]

class Segment:
    off = Address(0)
    content = list()
    length = 0

    def __init__(self) -> None:
        global res_file
        self.res_bytes()
        self.off = Address(len(res_file),4)

    def get_rel_off(self,off:Address) -> Address:
        return off-self.off

    def get_content(self):
        # return [i if type(i) == int else i.get() for i in self.content]
        return self.content

    def res_bytes(self):
        global res_file
        res_file.extend(bytearray(self.length))

class Function(Segment):
    off = Address(0,4)

    def __init__(self) -> None:
        for i in self.content:
            if type(i) == int:
                self.length += 1
            if type(i) == Address:
                self.length += i.pref_len
            else:
                self.length += 5
        self.length += 1
        super().__init__()

    def get_call(self,off:Address,index) -> list:
        return [0xE8]+[self.get_rel_off(off)]

    def get_content(self):
        return [i if type(i) == int else i.get_call(self.off,0) for i in self.content]+[0xC3]


class EHdr(Segment):
    def __init__(self) -> None:
        self.content = ([
            0x7F,0x45,0x4C,0x46,2,1,1,0,                # e_ident
            0,0,0,0,0,0,0,0,
            2,0,                                        # e_type
            0x3E,0,                                     # e_machine
            1,0,0,0]+                                   # e_version
            sections[".text"].get_entry()+              # e_entry
            [Address(0x40)]+                            # e_phoff
            [shdr_start]+                               # e_shoff
            [0,0,0,0,                                   # e_flags
            64,0,                                       # e_ehsize
            0x38,0,                                     # e_phentsize
            3,0,                                        # e_phnum
            0x40,0,                                     # e_shentsize
            len(sections),0,                            # e_shnum
            0,0]                                        # e_shstrndx
        )
        super().__init__()

class PHdr(Segment):
    def __init__(self,addr:Address,filesz:Address,memsz:Address,flags=5,offset=Address(0)) -> None:
        self.length = 0x38
        self.content = ([
            1,0,0,0,                        # p_type
            flags,0,0,0]+                   # p_flags
            [offset]+                       # p_offset
            [addr]+                         # p_vaddr
            [addr]+                         # p_paddr
            [filesz]+                       # p_filesz
            [memsz]+                        # p_memsz
            [0,0x10,0,0,0,0,0,0]            # p_align
            )
        super().__init__()

class SHdr(Segment):
    def __init__(self,name:int,typ:int,flags:int,addr:Address,offset:Address,length:int,align:int) -> None:
        self.content = ([
            name,0,0,0,                                 # sh_name
            typ,0,0,0,                                  # sh_type
            flags,0,0,0,0,0,0,0]+                       # sh_flags
            [addr]+                                     # sh_addr
            [offset]+                                   # sh_offset
            [Address(length)]+                          # sh_size
            [0,0,0,0,                                   # sh_link
             0,0,0,0,                                   # sh_info
             align,0,0,0,0,0,0,0,                       # sh_addralign
             0,0,0,0,0,0,0,0]                           # sh_entsize
            )
        super().__init__()

    def get_content(self):
        return super().get_content()

class Section(Segment):
    def __init__(self,name:str) -> None:
        self.name = name
        sections[name] = self
        global s_names
        s_names += name+"\x00"
        global shdr_start
        shdr_start += len(name)+1
        self.index = len(s_names)-len(name)-1
        if not type(super()) == type(Bss):
            super().__init__()

class Shstrtab(Section):
    def __init__(self) -> None:
        super().__init__(".shstrtab")

    def gen_header(self):
        self.header = SHdr(self.index,3,0,Address(0),shdr_start,len(s_names),1)

    def get_content(self) -> list:
        return [ord(i) for i in s_names]

class Bss(Section):
    def __init__(self) -> None:
        super().__init__(".bss")
        self.off = Address(0x3000)

    def gen_header(self):
        self.header = SHdr(self.index,8,3,Address(0x3000,8,"addr"),self.off,0x7558,4) # TODO adress

class Text(Section):
    def __init__(self) -> None:
        super().__init__(".text")
        self.entrypoint = Address(0)
        self.off = Address(0x1000)
        self.length = self.get_len()
        global shdr_start
        shdr_start += self.off + self.length
        self.res_bytes()

    def gen_header(self):
        self.header = SHdr(self.index,1,6,Address(0x1000,8,"addr"),self.off,self.length,0x10)

    def get_entry(self) -> list:
        content = []
        for segment in segments.values():
            content.extend(segment.get_content())
        self.entrypoint = base_addr+len(content)+self.off
        return self.entrypoint.get()

    def get_len(self) -> int:
        length = 0
        for segment in segments.values():
            length += segment.length
        length += len(file)*5
        length += 5
        return length

    def get_content(self) -> list:
        content = []
        for segment in segments.values():
            content.extend(segment.get_content())
        for char in range(len(file)):
            content.extend(self.get_segment(char).get_call(Address(len(content)),char))
        content.extend(segments["ex"].get_call(Address(len(content))))
        return content

    def get_segment(self,char:int):
        match file[char]:
            case ">":
                return segments["right"]
            case "<":
                return segments["left"]
            case "+":
                return segments["inc"]
            case "-":
                return segments["dec"]
            case ".":
                return segments["write"]
            case ",":
                return segments["read"]
            case "[":
                return segments["left_br"]
            case "]":
                return segments["right_br"]
            case "#":
                return segments["debug"]

sections[".shstrtab"] = Shstrtab()
Bss()

class RTerm(Function):
    def __init__(self):
        self.content = mov("rax",16)+mov("rdi",0)+mov("rsi",0x5401)+[0x48,0xBA]+sections[".bss"].off.get(4)+syscall()
        super().__init__()

class WTerm(Function):
    def __init__(self):
        self.content = mov("rax",16)+mov("rdi",0)+mov("rsi",0x5402)+[0x48,0xBA]+sections[".bss"].off.get(4)+syscall()
        super().__init__()

segments["w_term"] = WTerm()
segments["r_term"] = RTerm()

class COff(Function):
    def __init__(self):
        self.content = [segments["r_term"],0x83,0x24,0x25]+(sections[".bss"].off+12).get(4)+[0xFD,segments["w_term"]]
        super().__init__()

class COn(Function):
    def __init__(self):
        self.content = [segments["r_term"],0x83,0x0C,0x25]+(sections[".bss"].off+12).get(4)+[0x02,segments["w_term"]]
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
    def __init__(self) -> None:
        self.content = [0x48, 0x8B, 0x3B, 0x40, 0x08, 0xFF, 0x0F, 0x84]
        self.length = 4
        super().__init__()

    def get_call(self,off:Address,index:int):
        bracket_addr[index].copy(off)
        return self.content + [bracket_addr[brackets[index]]]

class RightBr(Function):
    def __init__(self) -> None:
        self.content = [0x48, 0x8B, 0x3B, 0x40, 0x08, 0xFF, 0x0F, 0x85]
        self.length = 4
        super().__init__()

    def get_call(self,off:Address,index:int):
        bracket_addr[index].copy(off)
        return self.content + [bracket_addr[brackets[index]]]

class Exit(Function):
    def __init__(self):
        self.content = mov("rax",60)+[0x48,0x8B,0x3B]+syscall()
        super().__init__()

    def get_call(self,off:Address) -> list:
        return [0xE9]+[self.get_rel_off(off)]

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
out_file.extend(PHdr(base_addr,Address(0xE8),Address(0xE8),4).get_content())
out_file.extend(PHdr(
    (base_addr+sections[".text"].off),
    Address(0xE8+sections[".text"].length),
    Address(0xE8+sections[".text"].length),
    5,
    Address(0x1000)
).get_content())
out_file.extend(PHdr((base_addr+sections[".bss"].off),Address(0),Address(30040),6).get_content())
out_file += [0] * (0x1000-len(flatten(out_file)))
out_file.extend(sections[".text"].get_content())
out_file.extend(sections[".shstrtab"].get_content())
sections[".shstrtab"].gen_header()
out_file.extend(sections[".shstrtab"].header.get_content())
sections[".bss"].gen_header()
out_file.extend(sections[".bss"].header.get_content())
sections[".text"].gen_header()
out_file.extend(sections[".text"].header.get_content())

out_file = flatten(out_file)
out_file = bytearray(out_file)

with open("out.out", "wb") as f:
    f.write(out_file)

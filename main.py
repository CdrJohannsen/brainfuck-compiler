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
res_text = bytearray()
out_file = []
s_names = ""

sections = {}
programms = {}

segments = {}

def flatten(in_list):
    """ Flatten nested list"""
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
    """ Get a mov instruction """
    desc:list
    length:int
    match to:
        case "rax":
            desc = [0xB8]
            length = 4
        case "rdx":
            desc = [0xBA]
            length = 4
        case "rdi":
            desc = [0xBF]
            length = 4
        case "dil":
            desc = [0x40,0xB7]
            length = 1
        case "rsi":
            desc = [0xBE]
            length = 4
        case _:
            print(f"Missing mov config for {to}")
            exit()
    return desc + list(bytearray(number.to_bytes(length,byteorder="little")))

def syscall()->list:
    """ Get Syscall """
    return [0x0F,0x05]

class Address():
    """Address object"""
    def __init__(self,off:int,pref_len:int=8,pref_type:str="off") -> None:
        self.off = off
        self.pref_len = pref_len
        self.pref_type = pref_type

    def get_off(self,length:int=0) -> list:
        """Get the file offset of the address"""
        if not length:
            length = self.pref_len
        return list(self.off.to_bytes(length,byteorder="little",signed=True))

    def get_addr(self,length:int=0) -> list:
        """Get the memory offset of the address"""
        if not length:
            length = self.pref_len
        return list((self.off+base_addr.off).to_bytes(length,byteorder="little",signed=True))

    def get(self,length:int=0) -> list:
        """Get prefered offset of the address"""
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

    def __str__(self) -> str:
        return f"off: {self.off} len:{self.pref_len}"
    
    def update(self,off=None,pref_len=None,pref_type=None):
        """Change parameters of the address"""
        if not off == None:
            self.off = off
        if not pref_len == None:
            self.pref_len = pref_len
        if not pref_type == None:
            self.pref_type = pref_type

    def copy(self,f):
        """Copy another Address"""
        self.off = f.off
        self.pref_len = f.pref_len
        self.pref_type = f.pref_type
        
base_addr = Address(0x400000)
shdr_start = Address(0)

bracket_addr = {}

class FunctionWrapper:
    """Wraps a Function object in a generalized class"""
    def __init__(self, ref) -> None:
        self.reference = ref
        self.index = 0

    def get_call(self, offset:int) -> list:
        return self.reference.get_call(offset)

    def get_length(self):
        return len(self.reference.get_call(0))

    def calc_off(self, ref, index:int) -> int:
        """Calculate the offset to another Address"""
        length = self.reference.calc_off(ref, index)
        return length

class Segment:
    """Base class for all Segments"""
    off = Address(0)
    content = list()
    length = 0

    def __init__(self) -> None:
        self.off = Address(len(res_file),4)
        self.res_bytes()

    def get_rel_off(self,off:Address) -> Address:
        """Get the relative offset to another address"""
        return self.off-off

    def get_content(self):
        return self.content

    def res_bytes(self):
        """Reserve bytes"""
        global res_file
        res_file.extend(bytearray(self.length))

class Function(Segment):
    """Contains the content for a function"""
    def __init__(self) -> None:
        for i in self.content:
            if type(i) == int:
                self.length += 1
            elif type(i) == Address:
                self.length += i.pref_len
            else:
                self.length += 5
        self.length += 1
        self.off = Address(len(res_text),4)
        self.res_bytes()

    def res_bytes(self):
        """Reserve bytes"""
        global res_text
        res_text.extend(bytearray(self.length))
        super().res_bytes()

    def get_call(self,off:Address) -> list:
        """Get a call to this function"""
        call = [0xE8]+self.get_rel_off(off).get()
        return call

    def get_content(self):
        """Get the content of this function"""
        content = []
        for i in range(len(self.content)):
            if type(self.content[i]) == int:
                content.append(self.content[i])
            elif type(self.content[i]) == Address:
                content.extend(self.content[i].get())
            else:
                content.extend(flatten(self.content[i].get_call(self.off+len(content)+5)))
        content += [0xC3]
        self.length = len(flatten(self.get_call(Address(0,pref_len=4))))
        return content


class EHdr(Segment):
    """Elf64 header"""
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
    """Programm header"""
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
    """Section header"""
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
    """Generic section template"""
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
    """Shstrtab section
    Holds the names of the sections"""
    def __init__(self) -> None:
        super().__init__(".shstrtab")

    def gen_header(self):
        self.header = SHdr(self.index,3,0,Address(0),shdr_start,len(s_names),1)

    def get_content(self) -> list:
        return [ord(i) for i in s_names]

class Bss(Section):
    """Bss section
    The section where data ist stored (Not sure if this souldn't be another section)"""
    def __init__(self) -> None:
        super().__init__(".bss")
        self.off = Address(0x3000)

    def gen_header(self):
        self.header = SHdr(self.index,8,3,Address(0x3000,8,"addr"),self.off,0x7558,4) # TODO adress

class Text(Section):
    """Text section
    Holds the executable code"""
    def __init__(self) -> None:
        super().__init__(".text")
        self.get_entry()
        self.off = Address(0x1000)
        self.length = self.get_len()
        global shdr_start
        shdr_start += self.off + self.length
        self.res_bytes()

    def gen_header(self):
        self.header = SHdr(self.index,1,6,Address(0x1000,8,"addr"),self.off,self.length,0x10)

    def get_entry(self) -> list:
        """Get the entrypoint of the executable"""
        defs = []
        for segment in segments.values():
            defs.extend(segment.get_content())
        self.entrypoint = self.off + len(flatten(defs)) + base_addr
        return self.entrypoint.get()

    def get_len(self) -> int:
        """Get the length of this section"""
        length = len(flatten(self.get_content()))
        return length

    def get_content(self) -> list:
        """Get the content of this section
        This is the executable code"""
        defs = []
        # Gets the function definitions
        for segment in segments.values():
            defs.extend(segment.get_content())
        defs.append([0x48,0xBB]+Address(0x3024,8,"addr").get())
        length = len(flatten(defs))
        func_calls = []

        # Create a FunctionWrapper for each function call
        for char in range(len(file)):
            func_calls.append(FunctionWrapper(self.get_segment(char)))

        # Match the brackets together and update their settings
        unmatched = []
        for part in func_calls:
            if type(part.reference) == LeftBr:
                part.index = length
                unmatched.append(part)
            elif type(part.reference) == RightBr:
                length += part.calc_off(unmatched[-1],length)
                unmatched.pop()
            else:
                length += part.get_length()

        # Get the function calls and bracket jumps
        content = []
        length = Address(len(flatten(defs)),pref_len=4) + 5
        for part in func_calls:
            content.extend(part.get_call(length))
            length += part.get_length()

        # Exit
        content.extend(segments["ex"].get_call(length))

        content = defs + content
        content += [0] * (len(content) % 2)
        return content

    def get_segment(self,char:int):
        """Get the function object for a character"""
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
                return segments["left_br"].__class__()
            case "]":
                return segments["right_br"].__class__()
            case "#":
                return segments["debug"]

# Create .shstrtab section to wich other sections can write their names to
sections[".shstrtab"] = Shstrtab()
# Create .bss section
Bss()

class RTerm(Function):
    """read_stdin_termios"""
    def __init__(self):
        self.content = mov("rax",16)+mov("rdi",0)+mov("rsi",0x5401)+[0x48,0xBA]+sections[".bss"].off.get_addr(8)+syscall()
        super().__init__()

class WTerm(Function):
    """write_stdin_termios"""
    def __init__(self):
        self.content = mov("rax",16)+mov("rdi",0)+mov("rsi",0x5402)+[0x48,0xBA]+sections[".bss"].off.get_addr(8)+syscall()
        super().__init__()

# These object need to be created here, so the next classes can use them
segments["r_term"] = RTerm()
segments["w_term"] = WTerm()

class COff(Function):
    """Turn off canonical mode"""
    def __init__(self):
        self.content = [segments["r_term"],0x83,0x24,0x25]+(sections[".bss"].off+12).get_addr(4)+[0xFD,segments["w_term"]]
        super().__init__()

class COn(Function):
    """Turn on canonical mode"""
    def __init__(self):
        self.content = [segments["r_term"],0x83,0x0C,0x25]+(sections[".bss"].off+12).get_addr(4)+[0x02,segments["w_term"]]
        super().__init__()

# These object need to be created here, so the next classes can use them
segments["c_off"] = COff()
segments["c_on"] = COn()

class Right(Function):
    """Move the pointer to the right"""
    def __init__(self):
        self.content = [0x48,0xFF,0xC3]
        super().__init__()

class Left(Function):
    """Move the pointer to the left"""
    def __init__(self):
        self.content = [0x48,0xFF,0xCB]
        super().__init__()

class Inc(Function):
    """Increment the byte at the pointer location"""
    def __init__(self):
        self.content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xC7]+[0x40,0x88,0x3B]
        super().__init__()

class Dec(Function):
    """Decrement the byte at the pointer location"""
    def __init__(self):
        self.content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xCF]+[0x40,0x88,0x3B]
        super().__init__()

class Write(Function):
    """Write to stdout"""
    def __init__(self):
        self.content = mov("rax",1)+mov("rdi",1)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()
        super().__init__()

class Read(Function):
    """Read one char from stdin"""
    def __init__(self):
        self.content = [segments["c_off"]]+mov("rax",0)+mov("dil",0)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()+[segments["c_on"]]
        super().__init__()


class Bracket(Function):
    """Generic bracket class"""
    def __init__(self) -> None:
        self.content = [0x48, 0x8B, 0x3B, 0x40, 0x08, 0xFF]
        self.length = 0

    def update(self, off:int, short:bool):
        """Update the values"""
        left_br = True if off >= 0 else False
        if short:
            self.content += [0x74 if left_br else 0x75] + (Address(off, pref_len=1) - 8 + 16 * left_br ).get()
        else:
            self.content += [0x0F, 0x84 if left_br else 0x85] + (Address(off,pref_len=4) - 12 + 24 * left_br).get()
        self.length = len(self.content)

    def get_content(self):
        return []

    def get_call(self,off:Address) -> list:
        return self.content

class LeftBr(Bracket):
    """Empty bracket class"""
    pass

class RightBr(Bracket):
    """Right bracket"""
    def calc_off(self,ref:FunctionWrapper,index:int) -> int:
        """Calculate the offset to the matching bracket"""
        off = index - ref.index
        short = False
        if off <= 127 and off >= -128:
            short = True
        ref.reference.update(off, short)
        self.update(-off, short)
        return 2 * self.length 

class Exit(Function):
    """The exit function
    Exits with code 0"""
    def __init__(self):
        self.content = mov("rax",60)+[0x48,0x8B,0x3B]+syscall()
        super().__init__()
        self.length -= 1

    def get_call(self,off:Address) -> list:
        return [0xE9]+self.get_rel_off(off).get()

    def get_content(self):
        return self.content

class Debug(Function):
    """Currently not implemented"""
    pass

# Create objects for the function classes
segments["write"] = Write()
segments["read"] = Read()
segments["inc"] = Inc()
segments["dec"] = Dec()
segments["right"] = Right()
segments["left"] = Left()
segments["left_br"] = LeftBr()
segments["right_br"] = RightBr()
# segments["debug"] = Debug()
segments["ex"] = Exit()

# Create .text section
Text()

# Fill the out file with all content
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

# Convert the outfile to a bytearray
out_file = flatten(out_file)
out_file = bytearray(out_file)

# Write outfile and make executable
with open("a.out", "wb") as f:
    f.write(out_file)
os.system("chmod +x a.out")

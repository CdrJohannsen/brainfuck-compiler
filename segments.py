addr = {}

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

def syscall()->list:
    return [0x0F,0x05]

def get_addr(label):
    return addr[label]


def get_elf_header():
    return bytearray([
        0x7F,0x45,0x4C,0x46,2,1,1,0,    # e_ident
        0,0,0,0,0,0,0,0,
        2,0,                            # e_type
        0x3E,0,                         # e_machine
        1,0,0,0]+                       # e_version
        get_addr("_start")+             # e_entry
        get_addr("phdr")+               # e_phoff
        get_addr("shdr")+               # e_shoff
        [0,0,0,0,                       # e_flags
        64,0,                           # e_ehsize
        0x38,0,                         # e_phentsize
        3,0,                            # e_phnum
        0x40,0,                         # e_shentsize
        4,0,                            # e_shnum
        3,0]                            # e_shstrndx
    )

def get_programm_header(addr,filesz,memsz,flags=5,offset=[0]*8):
    return bytearray([
        1,0,0,0,                        # p_type
        flags,0,0,0]+                   # p_flags
        offset+                         # p_offset
        addr+                           # p_vaddr
        addr+                           # p_paddr
        filesz+                         # p_filesz
        memsz+                          # p_memsz
        [0,0x10,0,0,0,0,0,0]            # p_align
    )

class Segment:
    addr = bytearray()
    content = list()

    def get_call(self) -> bytearray:
        return bytearray([0xE8])+self.addr

    def get_content(self):
        return bytearray([i if type(i) == type(int) else i.get_call() for i in self.content]+[0xC3])

class RTerm(Segment):
    pass

class WTerm(Segment):
    pass

w_term = WTerm()
r_term = RTerm()

class COff(Segment):
    content = [r_term,w_term]

class COn(Segment):
    content = [r_term,w_term]

c_off = COff()
c_on = COn()

class Right(Segment):
    content = [0x48,0xFF,0xC3]

class Left(Segment):
    content = [0x48,0xFF,0xCB]

class Inc(Segment):
    content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xC7]+[0x40,0x88,0x3B]

class Dec(Segment):
    content = [0x48,0x8B,0x3B]+[0x40,0xFE,0xCF]+[0x40,0x88,0x3B]

class Write(Segment):
    content = mov("rax",1)+mov("rdi",1)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()

class Read(Segment):
    content = [c_off]+mov("rax",0)+mov("dil",0)+[0x48,0x89,0xDE]+mov("rdx",1)+syscall()+[c_on]

class LeftBr(Segment):
    pass

class RightBr(Segment):
    pass

class Exit(Segment):
    content = mov("rax",60)+[0x48,0x8B,0x3B]+syscall()

    def get_call(self) -> bytearray:
        return bytearray([0xE9])+self.addr

class Debug(Segment):
    pass

right = Right()
left = Left()
inc = Inc()
dec = Dec()
write = Write()
read = Read()
left_br = LeftBr()
right_br = RightBr()
debug = Debug()
ex = Exit()

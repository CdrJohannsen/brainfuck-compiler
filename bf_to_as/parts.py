def get_header():
 return """
global _start
    section .bss
        termios:        resb 36
        stdin_fd:       equ 0           ; STDIN_FILENO
        ICANON:         equ 1<<1
        ECHO:           equ 1<<3
	    memo: resb 30000
    ; section .data

	; memo: times 30000 db 0

    section .text

    %include 'functions.s'
    _start:
        mov rbx, memo
"""

def get_write():
    return "        call write\n"

def get_read():
    return "        call read\n"

def get_inc():
    return "        call increment\n"

def get_dec():
    return "        call decrement\n"

def get_right():
    return "        call mov_right\n"

def get_left():
    return "        call mov_left\n"

def get_exit():
    return "        jmp exit\n"

def get_je(number:int,match:int):
    return f"""
        mov rdi, [rbx]
        or dil, dil
        je branch_{match}
    branch_{number}:
"""

def get_jne(number:int,match:int):
    return f"""
        mov rdi, [rbx]
        or dil, dil
        jne branch_{match}
    branch_{number}:
"""

def get_debug():
#     return f"""
#         mov rax, 1
#         mov rdi, 1
#         mov rsi, [rbx]
#         mov rdx, 8
#         syscall
# """
    return f"""
        mov rax, 1
        mov rdi, 1
        mov rsi, memo
        mov rdx, 30000
        syscall
        jmp exit
"""

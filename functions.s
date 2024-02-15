    read_stdin_termios:
        ; push r10
        mov rax, 16
        mov rdi, stdin_fd
        mov rsi, 5401h
        mov rdx, termios
        syscall
        ; pop r10
        ret
    write_stdin_termios:
        ; push r10
        mov rax, 16
        mov rdi, stdin_fd
        mov rsi, 5402h
        mov rdx, termios
        syscall
        ; pop r10
        ret

    canonical_off:
        call read_stdin_termios
        ; clear canonical bit in local mode flags
        and dword [termios+12], ~ICANON
        call write_stdin_termios
        ret

    canonical_on:
        call read_stdin_termios
        ; set canonical bit in local mode flags
        or dword [termios+12], ICANON
        call write_stdin_termios
        ret

    write:
        mov rax, 1
        mov rdi, 1
        mov rsi, rbx
        mov rdx, 1
        syscall
        ret

    read:
        call canonical_off
        mov rax, 0
        mov dil, 0
        mov rsi, rbx
        mov rdx, 1
        syscall
        call canonical_on
        ret

    increment:
        mov rdi, [rbx]
        inc dil
        mov [rbx], dil
        ret

    decrement:
        mov rdi, [rbx]
        dec dil
        mov [rbx], dil
        ret

    mov_right:
        inc rbx
        ret

    mov_left:
        dec rbx
        ret

    exit:
        mov rax, 60
        mov rdi, [rbx]
        syscall


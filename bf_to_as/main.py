#!/usr/bin/env python3
from parts import *
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

pointer = 0
memory = bytearray(1024)

out_file = get_header()

step = 0
while step < len(file):
    if file[step] == ">":
        out_file += get_right()
    elif file[step] == "<":
        out_file += get_left()
    elif file[step] == "+":
        out_file += get_inc()
    elif file[step] == "-":
        out_file += get_dec()
    elif file[step] == ".":
        out_file += get_write()
    elif file[step] == ",":
        out_file += get_read()
    elif file[step] == "[":
        out_file += get_jne(step,brackets[step])
    elif file[step] == "]":
        out_file += get_jz(step,brackets[step])
    elif file[step] == "#":
        out_file += get_debug()
    step += 1

out_file += get_exit()
with open("out.s", "w") as f:
    f.write(out_file)

os.system("nasm -f elf64 out.s")
os.system("ld out.o")

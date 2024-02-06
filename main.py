#!/usr/bin/env python3
from segments import *
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


out_file = bytearray()

step = 0
while step < len(file):
    if file[step] == ">":
        out_file.extend(right.get_call())
    elif file[step] == "<":
        out_file.extend(left.get_call())
    elif file[step] == "+":
        out_file.extend(inc.get_call())
    elif file[step] == "-":
        out_file.extend(dec.get_call())
    elif file[step] == ".":
        out_file.extend(write.get_call())
    elif file[step] == ",":
        out_file.extend(read.get_call())
    elif file[step] == "[":
        out_file.extend(left_br.get_call())
    elif file[step] == "]":
        out_file.extend(right_br.get_call())
    elif file[step] == "#":
        out_file.extend(debug.get_call())
    step += 1

out_file.extend(ex.get_call())
with open("out.out", "wb") as f:
    f.write(out_file)

# os.system("nasm -f elf64 out.s")
# os.system("ld out.o")

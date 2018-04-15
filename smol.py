# Smol is a basic bf interpreter, with 1 additional instruction:
# '\': overrwrites every cell in the tape with 0s
# this makes life a little easier since boolscript reuses the same tape for all
# bf programs

import sys
import itertools

class Smol:
    def __init__(self, tapesize=1):
        self.env = {
            '+': lambda: self.incdec(1, 0),
            '-': lambda: self.incdec(-1, 0),
            '>': lambda: self.incdec(0, 1),
            '<': lambda: self.incdec(0, -1),
            '.': lambda: print(chr(self.tape[self.pointer]), end=''),
            ',': lambda: self.incdec(int(input('\n%d? ' % self.pointer)) - self.tape[self.pointer], 0),
            '[': lambda: self.loop(True),
            ']': lambda: self.loop(False),
            '\\':lambda: self.reset()
        }
        self.tape = [0 for x in range(tapesize)]
        self.jmp_stack = []  # remembers positions on tape
        self.pointer = 0
        self.pc = 0

    def run(self, program):
        while self.pc < len(program):
            if program[self.pc] not in self.env: next
            self.env[program[self.pc]]()
            self.pc += 1
        return self.tape[self.pointer]

    def reset(self):
        self.tape = [0 for x in self.tape]

    def incdec(self, tape_inc, pointer_inc):
        self.pointer += pointer_inc
        if self.pointer >= len(self.tape): self.tape.append(0)
        self.tape[self.pointer] += tape_inc
        if self.tape[self.pointer] < 0: self.tape[self.pointer] = 0

    def loop(self, open):
        if open: self.jmp_stack.append(self.pc)  # save tape position
        elif self.tape[self.pointer] == 0: self.jmp_stack.pop()  # forget saved position
        else: self.pc = self.jmp_stack[-1]  # jmp to saved position at the top

    def __str__(self):
        return str(self.tape)

def main():
    smol = Smol()
    print('\n--smol interpreter--\n\nvalid instructions: {}\n'.format([k for k in smol.env]))
    smol.run([c for c in list(itertools.chain.from_iterable(open(sys.argv[1], 'rU'))) if c in smol.env])
    print(smol)

if __name__ == '__main__': main()

"""CPU functionality."""

import sys


# Flag
FL = [0] * 3
# Stack Pointer
SP = 7
# interrupt mask
IM = 5
# Interrupt status
IS = 6
INT = [0] * 8


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        self.ram = [0] * 256
        self.pc = 0
        self.running = False
        self.ops = {
            0b10100000: self.add_alu,
            0b10101000: self.and_alu,
            0b01010000: self.call,
            0b10100111: self.cmp_alu,
            0b00000001: self.hlt,
            0b01010101: self.jeq,
            0b01010100: self.jump,
            0b01010110: self.jne,
            0b10000010: self.ldi,
            0b10100010: self.mul_alu,
            0b01000110: self.pop_reg,
            0b01001000: self.pra,
            0b01000111: self.prn,
            0b01000101: self.push_reg,
            0b00010001: self.ret_sub,
            0b10000100: self.st
        }
        self.args = {
            0b10100000: 2,
            0b10101000: 2,
            0b01010000: 1,
            0b10100111: 2,
            0b00000001: 0,
            0b01010101: 1,
            0b01010100: 1,
            0b01010110: 1,
            0b10000010: 2,
            0b10100010: 2,
            0b01000110: 1,
            0b01001000: 1,
            0b01000111: 1,
            0b01000101: 1,
            0b00010001: 0,
            0b10000100: 2
        }

    def load(self):
        """Load a program into memory."""
        address = 0
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()
                    if len(temp) == 0:
                        continue
                    if temp[0][0] == "#":
                        continue

                    self.ram[address] = int(temp[0], 2)
                    address += 1
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")

        if address == 0:
            print("Empty!")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = self.fl | 0b00000001
            else:
                self.fl = self.fl & 0b11111110

            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = self.fl | 0b00000010
            else:
                self.fl = self.fl & 0b11111101

            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = self.fl | 0b00000100
            else:
                self.fl = self.fl & 0b11111011

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    # OP functions
    def add_alu(self, reg_a, reg_b):
        self.reg[reg_a] += self.reg[reg_b]
        self.pc += 3

    def and_alu(self, reg_a, reg_b):
        num1 = int(self.reg[reg_a])
        num2 = int(self.reg[reg_b])
        self.pc += 3

    def call(self, reg_num):
        ret_addr = self.pc + 2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = ret_addr
        self.pc = self.reg[reg_num]

    def cmp_alu(self, reg_a, reg_b):
        if self.reg[reg_a] == self.reg[reg_b]:
            # set FL from E to 1
            FL[-1] = 1
        else:
            # other wise set to 0
            FL[-1] = 0

        if self.reg[reg_a] > self.reg[reg_b]:
            # set FL from G to 1
            FL[-2] = 1
        else:
            # otherwise to 0
            FL[-2] = 0

        if self.reg[reg_a] < self.reg[reg_b]:
            # set FL bit from L to 1
            FL[-3] = 1
        else:
            # otherwise set to 0
            FL[-3] = 0
        self.pc += 3

    def hlt(self):
        self.running = False

    def jeq(self, reg_num):
        if int(FL[-1]) == 1:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def jump(self, reg_num):
        self.pc = self.reg[reg_num]

    def jne(self, reg_num):
        if int(FL[-1]) == 0:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc += 3

    def mul_alu(self, reg_a, reg_b):
        self.reg[reg_a] *= self.reg[reg_b]
        self.pc += 3

    def pra(self, reg_num):
        print(self.reg[reg_num])
        self.pc += 2

    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc += 2

    def push_reg(self, reg_num):
        self.reg[SP] -= 1
        stack_top = self.reg[SP]
        self.ram[stack_top] = self.reg[reg_num]
        self.pc += 2

    def pop_reg(self, reg_num):
        stack_top = self.reg[SP]
        self.reg[reg_num] = self.ram[stack_top]
        self.reg[SP] += 1
        self.pc += 2

    def ret_sub(self):
        ret_addr = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        self.pc = ret_addr

    def st(self, reg_a, reg_b):
        addr = self.reg[reg_a]
        value = self.reg[reg_b]
        self.ram_write(addr, value)
        self.pc += 3

    def run(self):
        self.running = True

        while self.running:
            ir = self.ram_read(self.pc)
            arg1 = self.ram_read(self.pc + 1)
            arg2 = self.ram_read(self.pc + 2)

            if self.args[ir] == 2:
                self.ops[ir](arg1, arg2)
            if self.args[ir] == 1:
                self.ops[ir](arg1)
            if self.args[ir] == 0:
                self.ops[ir]()


c = CPU()
c.load()
c.run()

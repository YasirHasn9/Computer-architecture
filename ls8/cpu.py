"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.pc = 0
        # Halt the CPU (and exit the emulator).
        self.hlt = 1
        # LDI register immediate
        self.ldi = 82

        # `PRN register` pseudo-instruction
        self.prn = 47

    # MAR: Memory Address Register, holds the memory address we're reading or writing
    def ram_read(self, mar):
        return self.ram[mar]

    # MDR: Memory Data Register, holds the value to write or the value just read
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            '''
            grab the ir from the ram 
            check it is 1
                then stop running 


            check if the ir is ldi
                grab the register number increment the pc by one  --> pc --> commend
                grab the value of the commend --> pc --> value
                increments the pc + 3 --> commend + value pointer ; skip them
                so we don't get conflict with other pointer in the memory


            check if ir is prn
                grab the value 
                print the pointer --> value 
                increments pc
                pc += 2

            '''
            ir = self.ram[self.pc]  # 0

            if ir == self.hlt:
                running = False

            elif ir == self.ldi:
                reg_num = self.ram[self.pc + 1]
                self.registers[reg_num] = self.ram[self.pc + 2]
                self.pc += 3

            elif ir == self.prn:
                reg_num = self.ram[self.pc + 1]
                print(self.registers[reg_num])
                self.pc += 2

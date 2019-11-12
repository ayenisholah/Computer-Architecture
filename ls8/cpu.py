"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [None] * 256
        self.pc = 0

    def ram_read(self, index):
        return(self.ram[index])

    def ram_write(self, value):
        command = input("Enter an address you want to write to: ")
        index = int(command)
        self.ram[index] = value
        return(self.ram[index])

    def load(self):
        """Load a program into memory."""

        address = 0
        with open("interrupts.ls8") as document:
            for line in document:
                print(line)

        if len(sys.argv) != 2:
            print("usage: 02-fileio02.py <filename>")
            sys.exit(1)

    try:
        with open(sys.argv[1]) as f:
            for line in f:
                print(line)
    except FileNotFoundError:
        print(f"{sys.argv[0]}: {sys.argv[1]} not found")

        # For now, we've just hardcoded a program:

        program = []

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "HLT":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "SAVE":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "PRINT_NUM":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "PRINT_REG":
            self.reg[reg_a] -= self.reg[reg_b]

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
        PRINT_SHOLA = 2
        PRINT_NUM = 3
        SAVE = 4
        PRINT_REG = 5
        ADD = 6
        IR = None
        running = True
        # looks like we need a converter for the binary
        while running:

            command = self.ram_read(self.pc)
            if command == SAVE:
                return
            elif command == PRINT_REG:
                pass
            else:
                print(f"Unknown Instruction {command}")
                sys.exit(1)

            self.pc += 1


cpu = CPU()
cpu.load()

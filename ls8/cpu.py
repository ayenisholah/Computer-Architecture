"""
    CPU functionality.
"""
import sys


class CPU:
    """
    Main CPU class.
    """

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.IR = None

    def ram_read(self, index):
        return(self.ram[index])

    def ram_write(self, value, index):
        self.ram[index] = value
        return(self.ram[index])

    def load(self):
        """Load a program into memory."""
        address = 0

        program = []
        try:
            with open(sys.argv[1]) as document:
                for line in document:
                    if line[0].startswith("0") or line[0].startswith("1"):
                        # split before and after any comment symbol '#'
                        comment_split = line.split("#")[0]
                        # convert the pre-comment portion (to the left) from binary to a value
                        # extract the first part of the split to a number variable
                        # and trim whitespace
                        num = comment_split.strip()

                        # ignore blank lines / comment only lines
                        if len(num) == 0:
                            continue

                        # set the number to an integer of base 2
                        value = int(num, 2)
                        program.append(value)
                    # print the value in binary and in decimal
                    # print(f"{value:08b}: {value:d}")
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

        for instructions in program:
            self.ram[address] = instructions
            address += 1

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
        PRN = 0b01000111
        LDI = 0b10000010
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        running = True

        while running:
            command = self.ram_read(self.pc)
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if command == LDI:
                self.IR = command
                instruction_size = 3
                reg = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg] = value

            elif command == PRN:
                self.IR = command
                instruction_size = 2
                reg = self.ram[self.pc + 1]
                print(self.reg[reg])

            elif command == MUL:
                self.IR = command
                instruction_size = 3
                reg_a = self.ram[self.pc + 1]
                reg_b = self.ram[self.pc + 2]
                self.reg[reg_a] *= self.reg[reg_b]

            elif command == PUSH:
                self.IR = command
                val = self.reg[operand_a]
                # self.reg -= 1
                self.ram_write(self.reg, val)
                self.pc += 3

            elif command == POP:
                val = self.reg[operand_a]
                self.reg += 1
                self.ram_write(self.reg, val)
                self.pc += 3

            elif IR == HLT:
                running = False

            self.pc += instruction_size

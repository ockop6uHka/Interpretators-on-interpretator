class LogicInterpreter:
    def __init__(self, basis):
        self.basis = basis

    def nand(self, a, b):
        return not (a and b)

    def nor(self, a, b):
        return not (a or b)

    def neg(self, a):
        if self.basis == 'nand':
            return self.nand(a, a)
        elif self.basis == 'nor':
            return self.nor(a, a)
        else:
            raise ValueError("Unsupported basis")

    def and_op(self, a, b):
        if self.basis == 'nand':
            return self.nand(self.nand(a, b), self.nand(a, b))
        elif self.basis == 'nor':
            return self.nor(self.nor(a, a), self.nor(b, b))
        else:
            raise ValueError("Unsupported basis")

    def or_op(self, a, b):
        if self.basis == 'nand':
            return self.nand(self.nand(a, a), self.nand(b, b))
        elif self.basis == 'nor':
            return self.nor(self.nor(a, b), self.nor(a, b))
        else:
            raise ValueError("Unsupported basis")

    def evaluate(self, instructions, variables):
        stack = []
        for meaning in instructions:
            print(stack)
            if meaning in variables:
                stack.append(variables[meaning])
            elif meaning == 'AND':
                b = stack.pop()
                a = stack.pop()
                stack.append(self.and_op(a, b))
            elif meaning == 'OR':
                b = stack.pop()
                a = stack.pop()
                stack.append(self.or_op(a, b))
            elif meaning == 'NOT':
                a = stack.pop()
                stack.append(self.neg(a))
            else:
                raise ValueError(f"Unknown meaning: {meaning}")

        return stack[0]

#(¬A∧B)∨(A∧¬B)
#
instructions1 = ['A', 'NOT', 'B', 'AND', 'A', 'B', 'NOT', 'AND', 'OR']
variables1 = {'A': True, 'B': False}

#((¬A ∧ B) ∧ (C ∨ D))
#(¬A ∧ B ∧ C) ∨ (¬A ∧ B ∧ D)
instructions2 = ['A', 'NOT', 'B', 'AND', 'C', 'AND', 'A', 'NOT', 'B', 'AND', 'D', 'AND', 'OR']
#expression2 = ['A', 'NOT', 'B', 'AND', 'C', 'D', 'OR', 'AND']
variables2 = {'A': True, 'B': False, 'C': False, 'D': False}

interpreter_nand = LogicInterpreter('nand')
result_nand1 = interpreter_nand.evaluate(instructions1, variables1)
result_nand2 = interpreter_nand.evaluate(instructions2, variables2)

interpreter_nor = LogicInterpreter('nor')
result_nor1 = interpreter_nor.evaluate(instructions1, variables1)
result_nor2 = interpreter_nor.evaluate(instructions2, variables2)

print(f"\nNAND basis data1: {result_nand1}")
print(f"NAND basis data2: {result_nand2}\n")
print(f'NOR basis data1: {result_nor1}')
print(f'NOR basis data2: {result_nor2}')

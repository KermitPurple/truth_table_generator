from enum import Enum
from dataclasses import dataclass

class TokenType(Enum):
    L_PAREN = 0
    R_PAREN = 1
    VARIABLE = 2
    OP_OR = 3
    OP_XOR = 4
    OP_AND = 5
    OP_NOT = 6

@dataclass
class Token:
    token_type: TokenType
    value: any = None

    @staticmethod
    def read_string(string: str) -> ['Token', ...]:
        result = []
        for ch in string:
            if ch.isalpha():
                result.append(Token(TokenType.VARIABLE, ch))
            elif ch == '(':
                result.append(Token(TokenType.L_PAREN))
            elif ch == ')':
                result.append(Token(TokenType.R_PAREN))
            elif ch in ['|', '+']:
                result.append(Token(TokenType.OP_OR))
            elif ch == '^':
                result.append(Token(TokenType.OP_XOR))
            elif ch in ['.', '', '&']:
                result.append(Token(TokenType.OP_AND))
            elif ch in ['~', '!']:
                result.append(Token(TokenType.OP_NOT))
        return result

@dataclass
class Variable:
    name: str

    def exec(self, env: dict) -> int:
        return env[self.name]

class BinaryOperator:
    func = lambda a, b: 0

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def exec(self, env: dict) -> int:
        return self.func(self.left.exec(env), self.right.exec(env))

class Or(BinaryOperator):
    func = lambda a, b: a | b

class Xor(BinaryOperator):
    func = lambda a, b: a ^ b

class And(BinaryOperator):
    func = lambda a, b: a & b

class Not:
    def __init__(self, var):
        self.var = var
        self.func = lambda a: ~a

    def exec(self, env: dict) -> int:
        return self.func(self.var.exec(env))

def nloops(n: int, to_loop: 'iterable', func = lambda x: 0,*args):
    if n == 0:
        print(*args, func(args), sep = ' | ')
        return
    for i in to_loop:
        nloops(n - 1, to_loop, func, *args, i)

def print_truth_table(eq: str):
    ops = {
            '^': lambda a, b: a ^ b,
            '|': lambda a, b: a | b,
            '&': lambda a, b: a & b,
            '.': lambda a, b: a & b,
            '': lambda a, b: a & b,
            }
    items = list({ch for ch in eq if ch.isalpha()})
    print(*items, eq, sep = ' | ')
    op_char = eq
    for ch in eq:
        if ch.isalpha():
            op_char = op_char.replace(ch, '')
    op = ops[op_char]
    func = lambda args: op(args[0], args[1])
    nloops(len(items), range(0, 2), func)

if __name__ == '__main__':
    # print_truth_table('AB')
    l = Token.read_string('A^B')
    print(l)

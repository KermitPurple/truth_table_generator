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
        prev_was_alpha = False
        for ch in string:
            if ch.isalpha():
                if prev_was_alpha:
                    result.append(Token(TokenType.OP_AND))
                result.append(Token(TokenType.VARIABLE, ch))
                prev_was_alpha = True
            else:
                prev_was_alpha = False
                if ch == '(':
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
    func = lambda self, a, b: 0

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def exec(self, env: dict) -> int:
        return self.func(self.left.exec(env), self.right.exec(env))

class Or(BinaryOperator):
    func = lambda self, a, b: a | b

class Xor(BinaryOperator):
    func = lambda self, a, b: a ^ b

class And(BinaryOperator):
    func = lambda self, a, b: a & b

class Not:
    def __init__(self, var):
        self.var = var
        self.func = lambda a: (a + 1) % 2

    def exec(self, env: dict) -> int:
        return self.func(self.var.exec(env))

def create_equation(token_list: [Token, ...]):
    # algo to impliment
    # find main operator
    # recurse on other parts if needed.
    if len(token_list) == 1:
        return Variable(token_list[0].value)
    for i, item in enumerate(token_list):
        if item.token_type is TokenType.OP_AND:
            return And(create_equation(token_list[i - 1: i]), create_equation(token_list[i + 1: i + 2]))
        elif item.token_type is TokenType.OP_XOR:
            return Xor(create_equation(token_list[i - 1: i]), create_equation(token_list[i + 1: i + 2]))
        elif item.token_type is TokenType.OP_OR:
            return Or(create_equation(token_list[i - 1: i]), create_equation(token_list[i + 1: i + 2]))
        elif item.token_type is TokenType.OP_NOT:
            return Not(create_equation(token_list[i + 1: i + 2]))

def nloops(n: int, to_loop: 'iterable', func, lst, *args):
    if n == 0:
        dct = {}
        for i, item in enumerate(lst):
            dct[lst[i]] = args[i]
        print(*args, func(dct), sep = ' | ')
        return
    for i in to_loop:
        nloops(n - 1, to_loop, func, lst, *args, i)

def print_truth_table(eq_str: str):
    items = list({ch for ch in eq_str if ch.isalpha()})
    print(*items, eq_str, sep = ' | ')
    l = Token.read_string(eq_str)
    eq = create_equation(l)
    nloops(len(items), range(0, 2), lambda x: eq.exec(x), items)

if __name__ == '__main__':
    print_truth_table('AB')
    print()
    print_truth_table('A|B')
    print()
    print_truth_table('A^B')
    print()
    print_truth_table('!A')
    print()

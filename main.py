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
    print_truth_table('AB')


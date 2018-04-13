import sys
import random

T, F = 'T', 'F'
OUT = '0'

ws = lambda c: c == ' ' or c == '\n' or c =='\r'
tf = lambda c: c == T or c == F
toss = lambda: B(T) if random.randint(0, 1) == 1 else B(F)
clean = lambda raw: [c for c in raw if not ws(c)]
interpret = lambda tree: eval(eat(tree[OUT]))

tree = {}

class AST(object):
    pass

class OP(AST):
    def __init__(self, left, op, right):
        self.left = B(left)
        self.op = op
        self.right = B(right)

    def __str__(self):
        return '({} {} {})'.format(self.left, self.op, self.right)

    __repr__ = __str__

class B(AST):
    def __init__(self, value):
        self.value = eat(value)

    def __str__(self):
        return '({})'.format(self.value)

    __repr__ = __str__

def error():
    print("not allowed!")
    exit(-1)

def parse(tokens):
    token = tokens.pop(0)
    if token == "'":
        q = []
        while tokens[0] != "'":
            q.append(tokens.pop(0))
        tokens.pop(0)
        return run(q).value

    if token == '(':
        f = []
        while tokens[0] != ')':
            f.append(parse(tokens))
        tokens.pop(0)
        return f
    elif token == ')':
        error()
    else:
        if token == '-': token += tokens.pop(0)
        return token

def eat(exp):
    if not isinstance(exp, list):
        return exp
    while len(exp) > 0:
        if len(exp) == 1:
            ast = B(exp.pop(0))
            break
        if len(exp) == 2:
            error()
        ast = OP(exp.pop(0), exp.pop(0), exp.pop(0))
    return ast

def store(tokens):
    tree = {}
    while len(tokens) > 0:
        t = tokens.pop()
        if t == '+':
            t = tokens.pop()
            tree[t] = eat(tokens.pop())
    return tree

def eval(ast):
    if isinstance(ast, B):
        if isinstance(ast.value, OP):
            ast = eval(ast.value)
        if not tf(ast.value):
            if ast.value == '?':
                t = toss()
                return t
            if ast.value not in tree:
                token = input('%s? ' % ast.value)
                if not tf(token):
                    token = run(list(token)).value
                tree[ast.value] = B(token)
            ast = eval(tree[ast.value])
        return ast
    op = ast.op
    p = eval(ast.left)
    if op == '&':
        if p.value == T:
            return eval(ast.right)
        return p
    if op == '|':
        if p.value == T:
            return p
        return eval(ast.right)
    if op == '^':
        q = eval(ast.right)
        if p.value == q.value:
            return tree[F]
        return tree[T]
    if op == '~':
        if p.value == T and eval(ast.right).value == T:
            return tree[F]
        return tree[T]
    if op == '->':
        if p.value == T:
            return eval(ast.right)
        return tree[T]

def run(raw):
    try:
        tree.update(store(parse(clean(raw))))
    except:
        error()
    tree.update({T: B(T), F: B(F)})

    if len(sys.argv) > 2 and sys.argv[2] == '-d':
        print(tree)

    result = None
    while result is None:
        try:
            result = interpret(tree)
        except RecursionError:
            pass
        except KeyboardInterrupt:
            print('bye')
            exit(0)
        except:
            error()
    return result

print("""
--(p&q)--

- 0 : program entry
- + : record
- & : and
- ~ : nand
- | : or
- ^ : xor
- ->: implies
""")

if len(sys.argv) < 2: error()

raw = []
if (sys.argv[1][0] == '('):
    raw = list(sys.argv[1])
else:
    with open(sys.argv[1], 'rU') as f:
        while True:
            c = f.read(1)
            if not c: break
            raw.append(c)

output = '({}0+)'.format(run(raw))
print('--output--\nresult:', run(output))
print('equivalent program:', output)

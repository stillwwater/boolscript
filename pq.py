import sys
import random
import smol

T, F = 'T', 'F'
OUT = '0'

smol = smol.Smol()

ws = lambda c: c == ' ' or c == '\n' or c =='\r'
tf = lambda c: c == T or c == F
toss = lambda: Statement(T) if random.randint(0, 1) == 1 else Statement(F)
clean = lambda raw: [c for c in raw if not ws(c)]
interpret = lambda tree: eval(eat(tree[OUT]))

tree = {}

class ASTNode(object):
    def __str__(self):
        return '({})'.format(self.value)

    __repr__ = __str__

class ComplexStatement(ASTNode):
    def __init__(self, left, op, right):
        self.left = Statement(left)
        self.op = op
        self.right = Statement(right)

    def __str__(self):
        return '({} {} {})'.format(self.left, self.op, self.right)

    __repr__ = __str__

class Statement(ASTNode):
    def __init__(self, value):
        self.value = eat(value)

class Proc(ASTNode):
    def __init__(self, program):
        self.value = clean(program)

    def run(self):
        if (self.value[0] == '('):
            # run an inner program
            return run(self.value)
        # run a smol bf program
        smol.pc = 0
        res = smol.run(self.value)
        print('tape: {}'.format(smol.tape))
        return Statement(F) if res == 0 else Statement(T)

def error():
    print("not allowed!")
    exit(-1)

def parse(tokens):
    token = tokens.pop(0)
    if token == "{" or token == "'":
        q = ''
        while tokens[0] != "}" and tokens[0] != "'":
            q += (tokens.pop(0))
        ending = tokens.pop(0)
        return q if ending == '}' else Proc(q).run().value
    if token == '(':
        f = []
        while tokens[0] != ')':
            f.append(parse(tokens))
        tokens.pop(0)
        return f
    elif token == ')' or token == '}':
        error()
    else:
        if token == '-': token += tokens.pop(0)
        return token

def eat(exp):
    if not isinstance(exp, list):
        return exp
    while len(exp) > 0:
        if len(exp) == 1:
            a = exp.pop(0)
            ast = Statement(a) if len(a) == 1 else Proc(a)
            break
        if len(exp) == 2:
            error()
        ast = ComplexStatement(exp.pop(0), exp.pop(0), exp.pop(0))
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
    if isinstance(ast, Proc):
        # this node is a procedure, or an inner program
        # exectute it and replace it with the return value
        ast = ast.run()
        print('inner: {}'.format(ast))
    if isinstance(ast, Statement):
        if isinstance(ast.value, ComplexStatement):
            ast = eval(ast.value)
        if not tf(ast.value):
            if ast.value == '?':
                t = toss()
                return t
            if ast.value not in tree:
                token = input('%s? ' % ast.value)
                if not tf(token):
                    token = run(list(token)).value
                tree[ast.value] = Statement(token)
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
    tree.update({T: Statement(T), F: Statement(F)})

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
--(boolscript)--

- 0 : program entry
- + : record
- & : and
- ~ : nand
- | : or
- ^ : xor
- ->: implies

--inner output--
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
run(output)
print('\noutput:', output)

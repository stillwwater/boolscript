## (Boolscript)

Boolscript is a language based on Boolean algebra. Conditional statements are reduced to `T` or `F` using 5 logical operators, until the program is reduced to either `((T)0+)` or `((F)0+)`.  A statement can be a statement, plus an operator, plus another statement; multiple operators within a statement is not allowed. The result, and the simplified version of the program, is printed once the program halts.

Instructions:

```
- 0 : program entry
- + : define
- ? : random, 50%T, 50%F (new value every time the statement is evaluated)
- undefined char : receive input (must be T, F, or another P&Q program)
```

Operators:

```
- & : and
- ~ : nand
- | : or
- ^ : xor
- ->: implies
```

Running:

```bash
python3 pq.py filename
python3 pq.py '((p&q)0+)'
debug: -d
```

### Examples:

[Truth machine:](http://esolangs.org/wiki/Truth-machine)

```python
((p&0)0+)
```

[Cat:](http://esolangs.org/wiki/Cat_program)

```python
((p)0+)
```

Running a child program, replacing it with its output:

```python
(({((p)0+)})0+)
```

*Child programs running within a parent program have access to the parent's definitions*.

Hello World:

```R
(({\++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.})0+)
```

If, then:

```R
((p->q)0+)
```

Check for equality:

```python
((T~(p^q))0+)
```

Invert input:

```python
((T~p)0+)
```

Pseudo-random value:

```python
(('((?)0+)'&0)0+)
```

*The program above will either print its output and halt, or it will run forever then print its output.*

*Using quotes means the child program will run once during parsing, surrounding it with '{}' means it'll run each time the statement is executed.*

```R
((?&0)0+)
```

*The program above will run until the random value is F; thus it will always output (F)*

Defining named-statements:

```R
((p->q)A+((T~q)->(T~p))B+(T~(A^B))0+)

p inplies q is equal to not q implies not p; this will always be true
```

Comments and whitespace:

```R
anything outside the program parenthesis is a comment
((p|q)
  A+
(r->(T~p))
  B+
(A&B)
  0+) whitespace is ignored
```

### Syntax:

```
<operator> ::= '&' | '~' | '|' | '^' | '->'
<statement> ::= '(' <complex-statement> | <char> ')'
<complex-statement> ::= <statement> <operator> <statement>
<named-statement> ::= <statement> <char> '+'
<program> ::= '(' *<named-statement> ')'
```

<sub>this is kind of a joke language, but hopefully you can create interesting things with it</sub>

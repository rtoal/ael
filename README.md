![Logo](https://raw.githubusercontent.com/rtoal/ael/main/docs/ael.png)

# Ael

This is a compiler for the language **Ael** written completely from scratch with no external libraries. Why? This is an introductory example for a compiler course, where learning the mechanics of tokenizing and parsing is an important goal. Besides, rolling your own lexer and parser is more often than not something you find yourself doing eventually.

Ael stands for (A)rithmetic (E)xpression (L)anguage. It’s the language of arithmetic expressions with `+`, `-`, `*`, `/`, `abs`, `sqrt`, and parentheses, together with declarations, assignments, and print statements. The language wants to be _just simple enough_ for the compiler writer to (1) experience the difference between statements and expressions, (2) have something to do during semantic analysis, and (3) provide a handful of optimization opportunities.

In the spirit of an introductory tutorial, this compiler features multiple backends: it can generate JavaScript, C, and LLVM. Why not a real assembly language? It’s fair to say LLVM these days takes things plenty far enough along for an introductory example. One can learn about register allocation and hardware-specific optimizations elsewhere.

## Sample Program

Here is a sample program in the language:

```
let x = 3 * 9
let y = 793 + (2 / abs 80 + x) * x
print 8 * x - (-y)
x = y
print y / sqrt 3
```

## Grammar

Here is the grammar of the language. Non-terminals begin with a capital letter, and their right-hand sides allow for skips (whitespace and comments) between each term. The token rules begin with lowercase letters and their right-hand sides are [Python regular expressions](https://docs.python.org/3/library/re.html) in Unicode mode; they are also meant to be processed in order, so that keywords are “matched” before identifiers.

```
Program     = Stmt+
Stmt        = Decl | AssignStmt | PrintStmt
Decl        = let id "=" Exp
AssignStmt  = id "=" Exp
PrintStmt   = print Exp
Exp         = Term (("+" | "-") Term)*
Term        = Factor (("*" | "/") Factor)*
Factor      = num | id | ("-" | abs | sqrt) Factor | "(" Exp ")"
let         = let\b
print       = print\b
abs         = abs\b
sqrt        = sqrt\b
num         = \d+(\.\d+)?
id          = (?!(abs|sqrt|let|print)\b)\w+
skip        = \s+|//.*?(\n|$)
```

## Running

The compiler is written in modern Python. You will need version 3.8 or above.

Because this application was written as a tutorial, the compiler exposes what each phase does, as well as providing multiple translations:

```
./aelc <filename> <output_type>
```

The output type argument tells the compiler what to print to standard output:

- `tokens` &nbsp;&nbsp; the token sequence
- `ast` &nbsp;&nbsp; the abstract syntax tree
- `analyzed` &nbsp;&nbsp; the semantically analyzed representation
- `optimized` &nbsp;&nbsp; the optimized semantically analyzed representation
- `js` &nbsp;&nbsp; the translation to JavaScript
- `c` &nbsp;&nbsp; the translation to C
- `llvm` &nbsp;&nbsp; the translation to LLVM

To keep things simple, the compiler will halt on the first error it finds.

Here’s a short transcript to give you a sense of the compiler behavior:

```
$ cat examples/constants.ael
// Fun for testing constant folding
let x = 0 - 5
print x + 8 * 10 + 200 / 5

$ ./aelc examples/constants.ael tokens
('#KEYWORD', 'let')
('#IDENTIFIER', 'x')
('#SYMBOL', '=')
('#NUMBER', '0')
('#SYMBOL', '-')
('#NUMBER', '5')
('#KEYWORD', 'print')
('#IDENTIFIER', 'x')
('#SYMBOL', '+')
('#NUMBER', '8')
('#SYMBOL', '*')
('#NUMBER', '10')
('#SYMBOL', '+')
('#NUMBER', '200')
('#SYMBOL', '/')
('#NUMBER', '5')
('#END', '')

$ ./aelc examples/constants.ael ast
   1 | program: Program
   2 |   statements[0]: Declaration name='x'
   3 |     initializer: BinaryExpression op='-'
   4 |       left: LiteralExpression value=0
   5 |       right: LiteralExpression value=5
   6 |   statements[1]: PrintStatement
   7 |     expression: BinaryExpression op='+'
   8 |       left: BinaryExpression op='+'
   9 |         left: IdentifierExpression name='x'
  10 |         right: BinaryExpression op='*'
  11 |           left: LiteralExpression value=8
  12 |           right: LiteralExpression value=10
  13 |       right: BinaryExpression op='/'
  14 |         left: LiteralExpression value=200
  15 |         right: LiteralExpression value=5


$ ./aelc examples/constants.ael analyzed
   1 | program: Program
   2 |   statements[0]: Declaration name='x'
   3 |     initializer: BinaryExpression op='-'
   4 |       left: LiteralExpression value=0
   5 |       right: LiteralExpression value=5
   6 |   statements[1]: PrintStatement
   7 |     expression: BinaryExpression op='+'
   8 |       left: BinaryExpression op='+'
   9 |         left: IdentifierExpression name='x' ref=$2
  10 |         right: BinaryExpression op='*'
  11 |           left: LiteralExpression value=8
  12 |           right: LiteralExpression value=10
  13 |       right: BinaryExpression op='/'
  14 |         left: LiteralExpression value=200
  15 |         right: LiteralExpression value=5


$ ./aelc examples/constants.ael optimized
   1 | program: Program
   2 |   statements[0]: Declaration name='x'
   3 |     initializer: LiteralExpression value=-5
   4 |   statements[1]: PrintStatement
   5 |     expression: BinaryExpression op='+'
   6 |       left: BinaryExpression op='+'
   7 |         left: IdentifierExpression name='x' ref=$2
   8 |         right: LiteralExpression value=80
   9 |       right: LiteralExpression value=40.0


$ ./aelc examples/constants.ael js
let x_1 = -5;
console.log(((x_1 + 80) + 40.0));

$ ./aelc examples/constants.ael c
#include <stdio.h>
#include <math.h>
int main() {
double x_1 = -5;
printf("%g\n", ((x_1 + 80) + 40.0));
return 0;
}

$ ./aelc examples/constants.ael llvm
@format = private constant [3 x i8] c"%g\0A"
declare i64 @printf(i8*, ...)
declare double @llvm.fabs(double)
declare double @llvm.sqrt.f64(double)
define i64 @main() {
entry:
%0 = fadd double -5.0, 80.0
%1 = fadd double %0, 40.0
call i64 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @format, i64 0, i64 0), double %1)
ret i64 0
}
```

## Contributing

I’m happy to take PRs. As usual, be nice when filing issues and contributing. Do remember the idea is to keep the language tiny; if you’d like to extend the language, you’re probably better forking into a _new_ project. However, I would _love_ to see any improvements you might have for the implementation or the pedagogy.

To set up your development environment, make sure you have Python 3.8 and py.test. A best practice is of course to set up your own virtual environment. You can run `py.test` directly in the project root, or, install pytest-cov and run:

```
coverage run --source ael -m pytest tests && coverage report -m
```

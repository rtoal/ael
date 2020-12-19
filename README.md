# ael

This is aompiler for the language Ael written completely from scratch with no external libraries. Ael stands for (A)rithmetic (E)xpression (L)anguage. It’s the language of arithmetic expressions over integers, limited to `+`, `-`, `*`, `/`, `abs`, and `sqrt` (with parentheses of course). The purpose of this language is to serve as an introductory example for compiler writing, so the language contains rather gratuitous declarations, assignments, and print statements.

## Sample Program

Here is a sample program in the language:

```
let x = 3 * 9
let y = 793 + (2 / abs 80 + x) * x
print 8 * x - (-y)
x = y
print y / sqrt 3
```

# Grammar

Here is the grammar of the language:

```
Program     = Stmt+
Stmt        = Decl | AssignStmt | PrintStmt
Decl        = "let" id "=" Exp
AssignStmt  = id "=" Exp
PrintStmt   = "print" Stmt
Exp         = Term (("+" | "-") Term)*
Term        = Factor (("*" | "/") Factor)*
Factor      = num | id | unaryop Factor | "(" Exp ")"
unaryop     = -|(abs|sqrt)\b
num         = \d+
keyword     = (let|print|abs|sqrt)\b
id          = \w+
```

# Running

The compiler is written in fairly modern Python. You will need version 3.8 or above.

Because this is an illustration of compiler writing, there are command line options that expose what each of the compiler phases are doing:

<dl>
<dt>`ael -t myprogram.ael`</dt>
<dd>Dumps the token sequence of `myprogram.ael` then stops</dd>

<dt>`ael -a myprogram.ael`</dt>
<dd>Dumps the abstract syntax tree `myprogram.ael` then stops</dd>

<dt>`ael -i myprogram.ael`</dt>
<dd>Dumps the semantic-checked graph of `myprogram.ael` then stops</dd>

<dt>`ael -o myprogram.ael`</dt>
<dd>Dumps the optimized semantic-checked graph of `myprogram.ael` then stops</dd>

<dt>`ael myprogram.ael`</dt>
<dd>Outputs the target code for `myprogram.ael`</dd>
</dl>

# Contributing

I’m happy to take PRs. As usual, be nice when filing issues and contributing. Do remember the idea is to keep the language tiny; if you’d like to extend the language, you’re probably better forking this into a new project. However, I would love to see any improvements you might have in the implementation (and the pedagogy).

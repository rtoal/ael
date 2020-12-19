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
<dt><code>ael -t myprogram.ael</dt>
<dd>Dumps the token sequence of <code>myprogram.ael</code> then stops</dd>

<dt><code>ael -a myprogram.ael</code></dt>
<dd>Dumps the abstract syntax tree <code>myprogram.ael</code> then stops</dd>

<dt><code>ael -i myprogram.ael</code></dt>
<dd>Dumps the semantic-checked graph of <code>myprogram.ael</code> then stops</dd>

<dt><code>ael -o myprogram.ael</code></dt>
<dd>Dumps the optimized semantic-checked graph of <code>myprogram.ael</code> then stops</dd>

<dt><code>ael myprogram.ael</code></dt>
<dd>Outputs the target code for <code>myprogram.ael</code></dd>
</dl>

# Contributing

I’m happy to take PRs. As usual, be nice when filing issues and contributing. Do remember the idea is to keep the language tiny; if you’d like to extend the language, you’re probably better forking this into a new project. However, I would love to see any improvements you might have in the implementation (and the pedagogy).

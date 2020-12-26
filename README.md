# Ael

This is a compiler for the language **Ael** written completely from scratch with no external libraries. Why? This is an introductory example for a compiler course.

Ael stands for (A)rithmetic (E)xpression (L)anguage. It’s the language of arithmetic expressions over integers, limited to `+`, `-`, `*`, `/`, `abs`, `sqrt`, and parentheses, together with declarations, assignments, and print statements. The idea is to give the language _just enough_ to (1) illustrate the difference between statements and expressions, (2) have something to do during semantic analysis, and (3) allow for more than one optimization.

In the spirit of an introductory tutorial, this compiler features multiple backends: it can generate JavaScript, C, and LLVM. Why not assembly? Well, LLVM, these days, takes things plenty far enough along for an introductory example.

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
Factor      = num | id | unaryop Factor | "(" Exp ")"
unaryop     = -|(abs|sqrt)\b
num         = \d+(\.\d+)?
let         = let\b
print       = print\b
id          = \w+
skip        = \s+|//[^\n]*\n
```

## Running

The compiler is written in fairly modern Python. You will need version 3.8 or above.

Because this is an illustration of compiler writing, there are command line options that expose what each of the compiler phases are doing:

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

## Contributing

I’m happy to take PRs. As usual, be nice when filing issues and contributing. Do remember the idea is to keep the language tiny; if you’d like to extend the language, you’re probably better forking into a new project. However, I would _love_ to see any improvements you might have for the implementation or the pedagogy.

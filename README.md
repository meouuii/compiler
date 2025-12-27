# Simple Compiler from Scratch (Python)

This project implements a simple compiler pipeline from scratch using Python. The goal is to demonstrate how Theory of Computation concepts are applied in real compiler design.

The compiler supports:
- Arithmetic expressions
- Variables and assignments
- Parentheses and operator precedence
- `print` statements
- Multi-line input execution

## Example Program

```text
x = 5
y = 10
print x + y
````

**Output**

```text
15
```

## Compiler Pipeline

The compiler is built in four main stages:

## 1. Lexical Analysis (Lexer)

* Reads raw input characters
* Groups them into tokens (INT, IDENTIFIER, PLUS, etc.)
* Based on Regular Languages and Finite Automata

## 2. Syntax Analysis (Parser)

* Consumes tokens from the lexer
* Validates syntax using a Context-Free Grammar (CFG)
* Builds an Abstract Syntax Tree (AST)

## 3. Abstract Syntax Tree (AST)

* Represents the hierarchical structure of the program
* Encodes operator precedence and program meaning
* Simplified version of a parse tree

## 4. Interpreter

* Traverses the AST
* Evaluates expressions
* Manages variables using a symbol table
* Produces the final output


## Grammar (CFG)

```
expr    → print expr
        | IDENTIFIER = expr
        | term ((+ | -) term)*

term    → factor ((* | /) factor)*

factor  → INT
        | FLOAT
        | IDENTIFIER
        | '(' expr ')'
```

## How to Run

### 1. Shell / REPL Mode (During Development)
While building and testing the compiler, you can use the interactive shell to run expressions line by line by running the shell file.

### 2. GUI Mode
To test the complete compiler with multi-line programs, run the Streamlit interface by:
```text
streamlit run gui.py
````

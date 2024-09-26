# Luppolo

Luppolo is a DSL capable of manipulating algebraic expressions.
The interpreter is written in Python using ANTLR4 as a parser generator.

This project was developed as part of the "Linguaggi e Traduttori" course for the Bachelor's degree in Computer Science at the University of Milan (Università degli Studi di Milano).

Project specifications [here](https://github.com/let-unimi/progetti/tree/master/05-Luppolo).

## Features

- **Run Luppolo Programs:** Execute `.lpp` source files from the command line.
- **Compile to Intermediate Representation (IR):** Convert Luppolo source files to JSON-based IR.
- **Trace Execution:** Visualize the stack trace during program execution.
- **Argument Passing:** Pass arguments directly to the program from the command line.
- **Optimization:** Optimize the Luppolo Abstract Syntax Tree (AST) before execution or compilation.
- **Automated Testing:** Run unit tests using `pytest` for `.lpp` programs to validate output.
  
## Requirements

- **Python 3.10+**
- Python Packages:
  - `antlr4-python3-runtime`

### Developer Requirements

- [ANTLR 4.13.1](https://www.antlr.org/download/antlr-4.13.1-complete.jar)
- Python Packages:
  - `ruff`
  - `pytest`

<!-- 
## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Andreal2000/luppolo.git
   cd luppolo
   ```

2. Install dependencies:
   ```bash
   pip install .
   ```

3. Ensure that the Luppolo CLI tool is ready for use:
   ```bash
   python -m src.main --help
   ```
-->

## Usage

### Running a Luppolo Program

You can run a `.lpp` file directly from the command line:

```bash
python -m src.main run path/to/file.lpp [args...]
```

For example, to run a file with arguments:

```bash
python -m src.main run examples/simple_program.lpp 4 5
```

### Compiling a Luppolo Program

To compile a `.lpp` file to JSON-based Intermediate Representation (IR):

```bash
python -m src.main compile path/to/file.lpp --output ir_output.json
```

- The `--output` parameter is optional. If not specified, the IR will be saved to a file named after the input source file (e.g., `file.lpp -> file.json`).

### Running a Compiled IR File

You can also execute a previously compiled IR file by running:

```bash
python -m src.main run path/to/ir_output.json [args...]
```

### Additional Options

- **Optimize the AST:**
  Use the `--optimize` flag to apply optimizations before execution or compilation:
  
  ```bash
  python -m src.main run --optimize path/to/file.lpp
  ```

- **Output the AST:**
  Use the `--ast` flag to print the AST before execution or compilation:
  
  ```bash
  python -m src.main run --ast path/to/file.lpp
  ```

- **Trace Execution:**
  Use the `--trace` flag to print the stack trace during the program's run:
  
  ```bash
  python -m src.main run --trace path/to/file.lpp
  ```

### Testing Luppolo Programs

You can run automated tests for all `.lpp` files located in the `test/` directory.

To run the tests:

```bash
pytest test/
```

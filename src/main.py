import argparse
import json
import os
import sys

from antlr4 import CommonTokenStream, InputStream

from src.ast.luppolo_ast_visitor import LuppoloAstVisitor
from src.ast.optimizer import optimize
from src.ast.threading import thread_program, thread_to_json
from src.error.luppolo_error_listener import LuppoloErrorListener
from src.grammar.LuppoloLexer import LuppoloLexer
from src.grammar.LuppoloParser import LuppoloParser
from src.interpreter.expression import num, sym
from src.interpreter.interpreter import interpreter


def compile_source(src: str, optimize_flag: bool = False, ast_flag: bool = False):
    input_stream = InputStream(src)
    lexer = LuppoloLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    lexer.reset()

    parser = LuppoloParser(token_stream)
    error_listener = LuppoloErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    luppolo_tree = parser.program()

    if error_listener.getWarningCount() > 0:
        print(
            f"{error_listener.getWarningCount()} syntax warning(s) detected and automatically corrected."
        )

    if error_listener.getErrorCount() > 0:
        print(f"{error_listener.getErrorCount()} syntax error(s) detected.")
        raise Exception("Error in compile: There is a syntax error in the source code")

    # Visit AST
    luppolo_ast_visitor = LuppoloAstVisitor()
    luppolo_ast = luppolo_ast_visitor.visit(luppolo_tree)

    # Optimize if the flag is set
    if optimize_flag:
        luppolo_ast = optimize(luppolo_ast)

    # Output of the AST
    if ast_flag:
        print("AST:")
        print(luppolo_ast.print())

    # Generate threads and convert to JSON IR
    thread = thread_program(luppolo_ast)
    ir = thread_to_json(thread)

    return ir


def run_ir(ir: dict, args: list = [], trace_flag: bool = False):
    # Parse arguments
    processed_args = []
    for arg in args:
        if (type(arg) is int) or (type(arg) is str and arg.isdigit()):
            processed_args.append(num(int(arg)))
        elif len(arg) == 1 and arg.islower():
            processed_args.append(sym(arg))
        else:
            raise Exception(f"ERROR in args: Invalid argument {arg}")

    # Execute the program
    return interpreter(ir, args=processed_args, trace=trace_flag)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Luppolo DSL Compiler and Interpreter")

    # Subparsers for `run` and `compile` modes
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run the source code")
    run_parser.add_argument(
        "file", help="The source file to run, must end with .lpp or .json"
    )
    run_parser.add_argument(
        "args", nargs="*", help="Arguments to pass when running the program", type=str
    )
    run_parser.add_argument(
        "-O",
        "--optimize",
        action="store_true",
        help="Apply optimization to the AST before execution",
    )
    run_parser.add_argument(
        "-a",
        "--ast",
        action="store_true",
        help="Print the AST of the source code",
    )
    run_parser.add_argument(
        "-t",
        "--trace",
        action="store_true",
        help="Print the trace of the stack interpreter during execution",
    )

    # Compile command
    compile_parser = subparsers.add_parser(
        "compile", help="Compile the source code to JSON IR"
    )
    compile_parser.add_argument(
        "file", help="The source file to compile, must end with .lpp"
    )
    compile_parser.add_argument(
        "-o", "--output", help="Output file for compiled IR (default: file.json)"
    )
    compile_parser.add_argument(
        "-O",
        "--optimize",
        action="store_true",
        help="Apply optimization to the AST before compilation",
    )
    compile_parser.add_argument(
        "-a",
        "--ast",
        action="store_true",
        help="Print the AST of the source code",
    )

    args = parser.parse_args()

    # Try to open the file and handle any errors
    try:
        # Ensure the file exists before proceeding
        if not os.path.exists(args.file):
            raise FileNotFoundError(f"File not found: {args.file}")

        # Determine if it's a source file (.lpp) or a compiled file (.json)
        if args.file.endswith(".lpp"):
            with open(args.file, "r") as f:
                src = f.read()

            if args.command == "run":
                print(
                    run_ir(
                        compile_source(src, args.optimize, args.ast),
                        args.args,
                        args.trace,
                    )
                )
            elif args.command == "compile":
                output_file = (
                    args.output
                    if args.output
                    else os.path.splitext(args.file)[0] + ".json"
                )

                ir = compile_source(src, args.optimize, args.ast)

                # Write IR to file
                with open(output_file, "w") as f:
                    json.dump(ir, f, indent=4)

                print(f"Compiled successfully. IR saved to {output_file}.")

        elif args.file.endswith(".json"):
            with open(args.file, "r") as f:
                compiled_ir = json.load(f)

            if args.command == "run":
                print(run_ir(compiled_ir, args.args, args.trace))

        else:
            raise Exception(f"ERROR: Unsupported file type: {args.file}")

    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except PermissionError:
        print(f"ERROR: Permission denied while trying to open {args.file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"ERROR: Failed to decode JSON from {args.file}")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

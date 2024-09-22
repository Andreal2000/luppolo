from collections import deque

from src.ast.tree import Tree, TreeKind
from src.interpreter.stdlib import STDLIB


def set_thread(ast, name, node):
    ast.jumps[name] = node


def concat_threads(prev, succ):
    if prev:
        set_thread(prev[-1], "next", succ[0])
    return prev + succ


def thread_to_json(thread):
    def to_json(threads):
        program = []
        for t in threads:
            program += [
                {
                    "kind": t.kind.name,
                    "value": t.value,
                    "jumps": {
                        k: threads.index(v) if v else None for k, v in t.jumps.items()
                    },
                }
            ]
        return program

    return {k: to_json(v) for k, v in thread.items()}


def thread_program(source):
    def thread(ast):
        match ast.kind:
            case TreeKind.PROGRAM:
                raise Exception(
                    "ERROR in threading: Program node should not be threaded directly"
                )

            case TreeKind.FUNCTION:
                threads = []
                for child in ast.children:
                    threads = concat_threads(threads, thread(child))

                return concat_threads([ast], threads)

            case TreeKind.BLOCK:
                threads = []
                for child in ast.children:
                    threads = concat_threads(threads, thread(child))
                return threads

            case TreeKind.IF_INSTRUCTION | TreeKind.IF_ELSE_INSTRUCTION:
                cond, true_block = ast.children[:2]

                threads = concat_threads(thread(cond), [ast])
                true_threads = thread(true_block)
                false_threads = (
                    thread(ast.children[-1])
                    if ast.kind is TreeKind.IF_ELSE_INSTRUCTION
                    else []
                )

                join = Tree(TreeKind.JOIN, [])

                if true_threads:
                    set_thread(ast, "true", true_threads[0])
                    concat_threads(true_threads, [join])
                    threads += true_threads
                else:
                    set_thread(ast, "true", join)

                if false_threads:
                    set_thread(ast, "false", false_threads[0])
                    concat_threads(false_threads, [join])
                    threads += false_threads
                else:
                    set_thread(ast, "false", join)

                return threads + [join]

            case TreeKind.REPEAT_INSTRUCTION:
                count, stat = ast.children
                count_threads = thread(count)
                stat_threads = thread(stat)

                concat_threads(count_threads, [ast])
                set_thread(ast, "loop", stat_threads[0] if stat_threads else ast)

                return count_threads + concat_threads(stat_threads, [ast])

            case TreeKind.WHILE_INSTRUCTION:
                condition, body = ast.children
                condition_threads = thread(condition)
                body_threads = thread(body)

                concat_threads(condition_threads, [ast])
                set_thread(ast, "loop", body_threads[0] if body_threads else ast)
                concat_threads(body_threads, condition_threads)

                return condition_threads + body_threads + [ast]

            case TreeKind.FOREACH_INSTRUCTION:
                id, count, stat = ast.children
                ast.value = id.value
                count_threads = thread(count)
                stat_threads = thread(stat)
                concat_threads(count_threads, [ast])
                set_thread(ast, "loop", stat_threads[0] if stat_threads else ast)
                return count_threads + concat_threads(stat_threads, [ast])

            case TreeKind.FUNCTION_CALL_EXPRESSION:
                function_name = ast.value["name"]

                if function_name not in processed_functions | set(STDLIB.keys()):
                    thread_queue.append(functions[function_name])

                threads = []
                for child in ast.children:
                    threads = concat_threads(threads, thread(child))

                return concat_threads(threads, [ast])

            case _:
                threads = []
                for child in ast.children:
                    threads = concat_threads(threads, thread(child))

                return concat_threads(threads, [ast])

    # A set of processed functions
    processed_functions = set()

    # A list of all functions to be processed
    functions = {}

    # A queue of function that must be processed
    thread_queue = deque()

    if source.kind is not TreeKind.PROGRAM:
        raise Exception("ERROR in threading: TreeKind.PROGRAM required")

    # Identify the main function and all other functions
    for child in source.children:
        func_name = child.value["name"]

        if func_name in functions:
            raise Exception(f"ERROR in threading: {func_name} function already defined")

        functions[func_name] = child

    if "Main" not in functions:
        raise Exception("ERROR in threading: Main function not found")

    # Start processing the main function
    thread_queue.append(functions["Main"])

    # A dictionary to store the threaded function bodies
    threads_dict = {}

    while thread_queue:
        func_ast = thread_queue.popleft()
        func_name = func_ast.value["name"]

        if func_name in processed_functions:
            continue

        # Thread the function and add it to the dictionary
        threaded_func = concat_threads([Tree(TreeKind.BEGIN, [])], thread(func_ast))
        threaded_func = concat_threads(threaded_func, [Tree(TreeKind.END, [])])

        threads_dict[func_name] = threaded_func
        processed_functions.add(func_name)

    return threads_dict

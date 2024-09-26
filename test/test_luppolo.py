import os

import pytest

from src.main import compile_source, run_ir


def collect_test_cases(*src_dirs):
    test_cases = []

    for src_dir in src_dirs:
        for root, _, files in os.walk(src_dir):
            for src_file in files:
                if src_file.endswith(".lpp"):
                    src_path = os.path.join(root, src_file)
                    test_cases.append(src_path)

    return test_cases


@pytest.mark.parametrize(
    "src_file",
    collect_test_cases(
        "test/test_src/expression",
        "test/test_src/instruction",
    ),
)
def test_luppolo(src_file):
    with open(src_file, "r") as file:
        src = file.read()

        ir = compile_source(src)
        output = run_ir(ir)

        assert output == 0

        file.close()

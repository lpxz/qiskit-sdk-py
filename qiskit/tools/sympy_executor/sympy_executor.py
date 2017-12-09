import argparse

import sys
import os
rootFolder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(rootFolder)


from equivalence_checker import check_equivalence
from extensible_gate_domain import _basic_gates_string_IBM, _basic_gates_string_IBM_advanced
from math_executor import math_execute
from circuit_builder import buildAST, buildCircuit
from regression_test import regression_test
import os

# need to refactor the name "basis_gates"

# highlights:
# standalone:
#   visualize a circuit
#   math execution
#   support of measurement, partial view of the complete state
# check equivalence
# regression testing


def makeArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('--basis_gates_option', type=int, default=2,
                           help='1: ibm q, 2: ibm q advanced')

    parser.add_argument('--qasm_files', type=str, default=rootFolder + "/tools/sympy_executor/testcases/test.qasm", #
                       help='paths of the qasm files') # they are separated with


    parser.add_argument('--math_execution', type=int, default=1,
                       help='shall we do math execution')
    parser.add_argument('--return_measured_state', type=int, default=1,
                   help='1 return measured state, 0 return complete state')
    parser.add_argument('--report_after_every_step', type=int, default=1,
                   help='report the state after every step, otherwise, we report the final state only')



    args = parser.parse_args()
    print(vars(args))

    return args

# the string can be file1:file2:dir1:dir2
# if it is a dir, we will look for *.qasm inside the dir
def parse_paths_linux_style(qasm_paths_str):
    qasm_paths = qasm_paths_str.split(':')
    result = []
    for qasm_path in qasm_paths:
        if os.path.isdir(qasm_path):
            for root, directories, files in os.walk(qasm_path):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if filepath.endswith('.qasm') and filepath not in result:
                        result.append(filepath)  # Add it to the list.
        else:
            if os.path.isfile(os.path.abspath(qasm_path)) and qasm_path.endswith('.qasm') and qasm_path not in result:
                result.append(qasm_path)
    return result

from qiskit import qasm, unroll


def qcheckermain(args):
    # important: the argument basis_gates control what gates are basic and can appear in the final assemblied circuit
    # the gates can be found in qiskit/extensions/standard/__init__.py
    if args.basis_gates_option == 1:
        _basic_gates_string = _basic_gates_string_IBM
    else:
        _basic_gates_string = _basic_gates_string_IBM_advanced


    qasm_paths_str = args.qasm_files
    result = parse_paths_linux_style(qasm_paths_str)
    for qasm_file in result:
        print("\n\n\n\n > ANALYZING " + qasm_file)



        ast = buildAST(qasm_file)

        circuit = buildCircuit(ast, basis_gates=_basic_gates_string.split(",")) # as shown in IBM qunatum computing # you can add more
        # save_plot_only(circuit)

        math_execute(args, circuit)







if __name__ == '__main__':
    args = makeArgs()
    qcheckermain(args)


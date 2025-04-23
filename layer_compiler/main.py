# main.py

import os
import sys
# Ensure our compiler modules are found first
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import argparse
from lexer       import Lexer
from parser      import Parser
from semantic    import SemanticAnalyzer
from codegen     import IRGenerator
from optim       import eliminate_dead_code
from vm          import VM

def main():
    argp = argparse.ArgumentParser(
        description="Layer compiler: shows each phase and executes Layer code"
    )
    argp.add_argument(
        'file', nargs='?',
        help="Path to a .layer file (omit to read from stdin)"
    )
    args = argp.parse_args()

    # 1) Read source
    if args.file:
        try:
            with open(args.file, 'r') as f:
                code = f.read()
        except IOError as e:
            print(f"❌ Cannot open file {args.file}: {e}")
            sys.exit(1)
    else:
        print("Enter Layer code, end with Ctrl+D (or Ctrl+Z then Enter on Windows):")
        code = sys.stdin.read()

    # 2) Lexical Analysis
    print("\n🔍 Lexical Analysis:")
    try:
        tokens = Lexer(code).tokenize()
        print([t.value for t in tokens if t.type != 'WHITESPACE'])
    except Exception as e:
        print("❌ Lexical Error:", e)
        sys.exit(1)

    # 3) Syntax Analysis
    print("\n📦 Syntax Analysis:")
    try:
        tree = Parser(code).parse()
        print(tree)
    except Exception as e:
        print("❌ Syntax Error:", e)
        sys.exit(1)

    # 4) Semantic Analysis
    print("\n✅ Semantic Analysis:")
    try:
        SemanticAnalyzer(tree).analyze()
        print("Semantic analysis passed")
    except Exception as e:
        print("❌ Semantic Error:", e)
        sys.exit(1)

    # 5) Intermediate Representation
    print("\n🛠️ Intermediate Representation:")
    try:
        ir_list = IRGenerator().generate(tree)
        for instr in ir_list:
            print(instr)
    except Exception as e:
        print("❌ IR Generation Error:", e)
        sys.exit(1)

    # 5.1) Dead‑Code Elimination
    print("\n🛠️ Optimized IR (dead code eliminated):")
    opt_ir = eliminate_dead_code(ir_list)
    for instr in opt_ir:
        print(instr)

    # 6) VM Execution
    print("\n🖥️ VM Execution:")
    try:
        VM(opt_ir).run()
    except Exception as e:
        print("❌ VM Error:", e)
        sys.exit(1)

if __name__ == '__main__':
    main()

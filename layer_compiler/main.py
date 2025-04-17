# main.py

import sys
import argparse
from parser      import Parser
from semantic    import SemanticAnalyzer
from interpreter import Interpreter

def main():
    argp = argparse.ArgumentParser(
        description="Layer runner: parse, check, and execute Layer code"
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

    # 2) Parse → AST
    try:
        tree = Parser(code).parse()
    except Exception as e:
        print("❌ Syntax Error:", e)
        sys.exit(1)

    # 3) Semantic check
    try:
        SemanticAnalyzer(tree).analyze()
    except Exception as e:
        print("❌ Semantic Error:", e)
        sys.exit(1)

    # 4) Execute
    print("\n▶️ Execution output:")
    Interpreter(tree).run()

if __name__ == '__main__':
    main()

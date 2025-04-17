# main.py

from parser import Parser
from semantic import SemanticAnalyzer

if __name__ == '__main__':
    code = '''
# semantic test
cvar age = 25
ivar name = "Alice"      # ← ivar is now initialized, so semantic check will pass
'''
    # 1) Parse → AST
    try:
        tree = Parser(code).parse()
        print("AST =", tree)
    except Exception as e:
        print("❌ Syntax Error:", e)
        exit(1)

    # 2) Semantic check
    try:
        SemanticAnalyzer(tree).analyze()
        print("✅ Semantic analysis passed")
    except Exception as e:
        print("❌ Semantic Error:", e)

# main.py

from parser      import Parser
from semantic    import SemanticAnalyzer
from interpreter import Interpreter

if __name__ == '__main__':
    code = '''
# full integration test
cvar age = 5
write("Starting age:", age)

loop i for 3 times -> {
    age = age + 2
    write("After", i, "age:", age)
}

if age > 10 -> write("Final age is greater than 10!")
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
        exit(1)

    # 3) Execute the AST
    print("\n▶️ Execution output:")
    Interpreter(tree).run()

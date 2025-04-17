# main.py

from parser import Parser

if __name__ == '__main__':
    code = '''
# this is a comment
cvar age = 25
fwrite("Hello, World!", age)
loop i for 3 times -> {
    write(i)
}
if age > 20 -> {
    write("Age is over 20")
}
'''
    # Parse the source into an AST
    tree = Parser(code).parse()
    # Print the resulting AST
    print(tree)

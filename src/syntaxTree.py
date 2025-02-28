class ASTNode:
    """Base class for all AST nodes."""
    def __repr__(self):
        return str(self.__dict__)

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"

class VariableDeclaration(ASTNode):
    def __init__(self, var_type, identifier, expression=None):
        self.var_type = var_type
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"VariableDeclaration({self.var_type}, {self.identifier}, {self.expression})"

class WriteStatement(ASTNode):
    def __init__(self, arguments):
        self.arguments = arguments

    def __repr__(self):
        return f"WriteStatement({self.arguments})"

class IfStatement(ASTNode):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, block={self.block})"

class LoopForStatement(ASTNode):
    def __init__(self, identifier, count, block):
        self.identifier = identifier
        self.count = count
        self.block = block

    def __repr__(self):
        return f"LoopForStatement({self.identifier}, {self.count}, {self.block})"

class LoopWhileStatement(ASTNode):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f"LoopWhileStatement(condition={self.condition}, block={self.block})"

class Expression(ASTNode):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"Expression({self.left}, {self.operator}, {self.right})"

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class Number(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class String(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Boolean({self.value})"

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

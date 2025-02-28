from syntaxTree import *
from lexer import tokenize  # Ensure you have a working lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def advance(self):
        """Moves to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None  # End of token stream

    def match(self, token_type, value=None):
        """Checks and consumes a token if it matches."""
        if self.current_token and self.current_token[0] == token_type and (value is None or self.current_token[1] == value):
            self.advance()
            return True
        return False

    def parse(self):
        """Main entry point for parsing the program."""
        statements = []
        while self.current_token:
            if self.current_token[0] == "NEWLINE":  # Ignore empty lines
                self.advance()
                continue
            if self.current_token[0] == "COMMENT":  # Ignore comments
                self.advance()
                continue
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self):
        """Parses different statements based on the first token."""
        if self.match("KEYWORD", "cvar") or self.match("KEYWORD", "ivar"):
            var_type = self.tokens[self.position - 1][1]
            return self.parse_variable_declaration(var_type)
        elif self.match("KEYWORD", "write"):
            return self.parse_write_statement()
        elif self.match("KEYWORD", "if"):
            return self.parse_if_statement()
        elif self.match("KEYWORD", "loop"):
            return self.parse_loop_statement()
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def parse_variable_declaration(self, var_type):
        """Parses variable declarations (cvar/ivar)."""
        if self.current_token[0] != "IDENTIFIER":
            raise SyntaxError("Expected identifier after variable type.")
        identifier = Identifier(self.current_token[1])
        self.advance()

        expression = None
        if self.match("OPERATOR", "="):
            expression = self.parse_expression()

        return VariableDeclaration(var_type, identifier, expression)

    def parse_write_statement(self):
        """Parses a write statement."""
        if not self.match("PUNCTUATION", "("):
            raise SyntaxError("Expected '(' after 'write'.")
        
        arguments = []
        while self.current_token and self.current_token[0] != "PUNCTUATION":
            arguments.append(self.parse_expression())
            if not self.match("PUNCTUATION", ","):
                break
        
        if not self.match("PUNCTUATION", ")"):
            raise SyntaxError("Expected ')' to close 'write'.")

        return WriteStatement(arguments)

    def parse_if_statement(self):
        """Parses an if statement."""
        condition = self.parse_expression()
        if not self.match("ARROW", "->"):
            raise SyntaxError("Expected '->' after if condition.")

        block = self.parse_block()
        return IfStatement(condition, block)

    def parse_loop_statement(self):
        """Parses for-loop or while-loop statements."""
        if self.match("KEYWORD", "while"):
            condition = self.parse_expression()
            if not self.match("ARROW", "->"):
                raise SyntaxError("Expected '->' after while condition.")
            block = self.parse_block()
            return LoopWhileStatement(condition, block)

        identifier = None
        if self.current_token[0] == "IDENTIFIER":
            identifier = self.current_token[1]
            self.advance()

        if not self.match("KEYWORD", "for"):
            raise SyntaxError("Expected 'for' in loop statement.")

        count = self.parse_expression()

        if not self.match("KEYWORD", "times"):
            raise SyntaxError("Expected 'times' after loop count.")

        if not self.match("ARROW", "->"):
            raise SyntaxError("Expected '->' before loop body.")

        block = self.parse_block()
        return LoopForStatement(identifier, count, block)

    def parse_block(self):
        """Parses a block of statements (either single-line or enclosed in {})."""
        if self.match("PUNCTUATION", "{"):
            statements = []
            while self.current_token and not self.match("PUNCTUATION", "}"):
                if self.current_token[0] == "NEWLINE":
                    self.advance()
                    continue
                statements.append(self.parse_statement())
            return Block(statements)
        else:
            return Block([self.parse_statement()])

    def parse_expression(self):
        """Parses an expression (e.g., 5 + x)."""
        left = self.parse_primary()
        
        while self.current_token and self.current_token[0] == "OPERATOR":
            operator = self.current_token[1]
            self.advance()
            right = self.parse_primary()
            left = Expression(left, operator, right)

        return left

    def parse_primary(self):
        """Parses primary values (identifiers, numbers, strings, boolean)."""
        if self.current_token[0] == "IDENTIFIER":
            node = Identifier(self.current_token[1])
        elif self.current_token[0] == "NUMBER":
            node = Number(self.current_token[1])
        elif self.current_token[0] == "STRING":
            node = String(self.current_token[1])
        elif self.current_token[0] == "BOOLEAN":
            node = Boolean(self.current_token[1])
        else:
            raise SyntaxError(f"Unexpected token in expression: {self.current_token}")

        self.advance()
        return node

# Example usage
if __name__ == "__main__":
    code = """
    # This is a comment
    cvar x = 10
    ivar y = 20
    write("Hello, Layer!")
    if x < y -> write("x is smaller")
    loop i for 5 times -> write(i)
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print(ast)  # This will now print a readable AST

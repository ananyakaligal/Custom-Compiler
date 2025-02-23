"""
Layer Grammar design,

0. Basics
    0.1. Comments
        comments are ignored by the interpreter
        to comment a line, use the '#' character
        regex: ^\s*#.*$

    0.2. Indentation
        inden tation is used to define blocks
        indentation is 4 spaces
        regex: ^\s{4}.*$

    0.3. Newline
        newline is used to separate statements
        regex: ^\n$

    0.4. Whitespace
        whitespace is ignored by the interpreter
        regex: ^\s+$

    0.5. Identifiers
        identifiers are used to name variables
        identifiers can only contain letters, numbers and underscores
        identifiers cannot start with a number
        regex: ^[a-zA-Z_][a-zA-Z0-9_]*$

    0.6. Numbers
        numbers are used to represent can be integers or floats
        regex: ^[0-9]+(\.[0-9]+)?$

    0.7. Strings
        strings are used to represent text
        strings are surrounded by double quotes
        regex: ^".*"$

    0.8. Operators
        operators are used to perform operations
        operators are: +, -, *, /, %, ^, =, ==, !=, <, >, <=, >=, and, or, not
        regex: ^(\+|-|\*|/|%|\^|=|==|!=|<|>|<=|>=|and|or|not)$

    0.9. Keywords
        keywords are used to define statements
        keywords are: cvar, ivar,if, else, while, for, break, continue, def, return, class, import, from, as
        regex: ^(cvar|ivar|if|else|while|for|break|continue|def|return|class|import|from|as)$

    0.10. Punctuation
        punctuation is used to separate statements
        punctuation is: ., ,, :, (, ), [, ], {, }
        regex: ^(\.|,|:|\(|\)|\[|\]|\{|\})$

    0.11. Boolean
        boolean is used to represent true or false
        boolean is: true, false
        regex: ^(true|false)$


1.0 Statements

    1.1. Variable declaration and initialization

        variable declaration is used to declare variables
        there are two types of variables, cvar and ivar
            cvar is a 'create variable' for which the value assignment is optional
            ivar is a 'initialize variable' for which the value assignment is mandatory

        1.1.1 cvar
            cvar example : cvar age
            or
            cvar age = 5
            :cvar <keyword> <identifier>
            or
            :cvar <keyword> <identifier> = <expression>


    1.2. write statement

        write statement is used to write values to the console
        write statement in layers is as powerful as the write function in python but with some limitations

        1.2.1. write statements
            there are two types of write statements, write and fwrite
            write statement
                write statement is used to write values to the console
                write statement in layers is as powerful as the write function in python
                write statement example : write("Hello World! from layers programming language")
                write statement example : write(5)
                write statement example : write(5 + 5)
                write statement example : write(5 + 5, 5 - 5, 5 * 5, 5 / 5, 5 % 5, 5 ^ 5)

                regex: ^write\((.*)\)$


            fwrite statement
                fwrite statement is formatter write statement just like write(f"Hello {name}!") in python
                fwrite statement example : fwrite("Hello {name}!")
                fwrite statement example : fwrite("Hello {name}!", name = "World")

                regex: ^fwrite\((.*)\)$

    1.3 Loops

        loops are used to repeat a block of code
        there are two type of loops, while and for
        loops in layer is very different from loops in python or other programming languages

        1.3.1 for loop

                for loop example : loop for 5 times -> write("Hello World!")
                for loop example : loop i for 5 times -> write(i)
                for loop example : loop x for 10 times -> { write(x) } or can be multiline also.
                for loop example : loop x for 10 times -> {
                write(x)
                write(x + 1)
                write(x + 2)
                }
                syntax: loop <identifier> for <expression> times -> <block>
                or
                syntax: loop <identifier> for <expression> times -> { <block> }

                regex: ^loop ([a-zA-Z_][a-zA-Z0-9_]*) for ([0-9]+) times -> (.*)$
                or
                regex: ^loop ([a-zA-Z_][a-zA-Z0-9_]*) for ([0-9]+) times -> \{(.*)\}$

        1.3.2 while loop

                while loop example : loop while i < 5 -> write(i)
                while loop example : loop while i < 5 -> { write(i) }
                while loop example : loop while i < 5 -> {
                write(i)
                write(i + 1)
                write(i + 2)
                }
                syntax: loop while <expression> -> <block>
                or
                syntax: loop while <expression> -> { <block> }

                regex: ^loop while (.*) -> (.*)$
                or
                regex: ^loop while (.*) -> \{(.*)\}$

    1.4 Conditional statements

        conditional statements are used to execute a block of code if a condition is true
        there are three types of conditional statements, if, if-else, else

        1.4.1 if statement

            if statement example : if i < 5 -> write(i)
            if statement example : if i < 5 -> { write(i) }
            if statement example : if i < 5 -> {
                write(i)
                write(i + 1)
                write(i + 2)
            }
            syntax: if <expression> -> <block>
            or
            syntax: if <expression> -> { <block> }

            regex: ^if (.*) -> (.*)$
            or
            regex: ^if (.*) -> \{(.*)\}$

            1.4.1.1 break statement

                break statement is used to break out of a loop
                break statement example : if i < 5 -> break
                break statement example : if i < 5 -> { break }
                break statement example : if i < 5 -> {
                break
                }
                syntax: if <expression> -> break
                or
                syntax: if <expression> -> { break }

                regex: ^if (.*) -> break$
                or
                regex: ^if (.*) -> \{ break \}$

"""
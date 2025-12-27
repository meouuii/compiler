#######################################
# CONSTANTS
#######################################

DIGITS         ='0123456789'
LETTERS        ='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# TOKENS
#######################################

TT_INT       = 'INT'
TT_FLOAT     = 'FLOAT'
TT_PLUS      = 'PLUS'
TT_MINUS     = 'MINUS'
TT_MUL       = 'MUL'
TT_DIV       = 'DIV'
TT_LPAREN    = 'LPAREN'
TT_RPAREN    = 'RPAREN'
TT_IDENTIFIER= 'IDENTIFIER'
TT_EQ        = 'EQ'
TT_PRINT     = 'PRINT'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
    
    def __repr__(self):
        if self.value is not None:
            return f'{self.type}:{self.value}'
        return f'{self.type}'

#######################################
# LEXER
#######################################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.idx = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.idx += 1
        self.current_char = self.text[self.idx] if self.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t\n\r':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '=':
                tokens.append(Token(TT_EQ))
                self.advance()

            else:
                raise Exception(f"Illegal character: '{self.current_char}'")

        return tokens
    
    def make_identifier(self):
        id_str = ''

        while self.current_char is not None and self.current_char in LETTERS_DIGITS:
            id_str += self.current_char
            self.advance()
    
        if id_str == "print":
            return Token(TT_PRINT)

        return Token(TT_IDENTIFIER, id_str)

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))

#######################################
# PARSER NODES   #represent meaning not text   #checks grammar
#######################################

class NumberNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left, op_tok, right):
        self.left = left
        self.op_tok = op_tok
        self.right = right
    
    def __repr__(self):
        return f'({self.left} {self.op_tok} {self.right})'
    
class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

    def __repr__(self):
        return f"(var {self.var_name_tok.value})"

class VarAssignNode:
    def __init__(self, var_name_tok, value_node):
        self.var_name_tok = var_name_tok
        self.value_node = value_node

    def __repr__(self):
        return f"({self.var_name_tok.value} = {self.value_node})"
    
class PrintNode:
    def __init__(self, value_node):
        self.value_node = value_node

    def __repr__(self):
        return f"(print {self.value_node})"


#######################################
# PARSER
#######################################

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.current_tok = self.tokens[0] if self.tokens else None


    def advance(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.current_tok = self.tokens[self.idx]
        else:
            self.current_tok = None
        return self.current_tok

    def parse(self): #starts parsing
        if not self.tokens:
            return None

        result = self.expr() #means that text always starts as an expression according to my grammar
        return result

    def expr(self):  #implements grammar rules for expressions(non terminal)
        if self.current_tok.type == TT_PRINT:
            self.advance()
            value_node = self.expr()
            return PrintNode(value_node)

        if self.current_tok.type == TT_IDENTIFIER:
            var_name = self.current_tok
            self.advance()

            if self.current_tok is not None and self.current_tok.type == TT_EQ:
                self.advance()
                value_node = self.expr()
                return VarAssignNode(var_name, value_node)
            else:
                left = VarAccessNode(var_name) #if its a identifier without assignmet, varaccess
        else:
            left = self.term() #if just arithmatic, parse

        while self.current_tok is not None and self.current_tok.type in (TT_PLUS, TT_MINUS):
            op_tok = self.current_tok
            self.advance()
            right = self.term()
            left = BinOpNode(left, op_tok, right)

        return left

    def term(self):
        left = self.factor()

        while self.current_tok is not None and self.current_tok.type in (TT_MUL, TT_DIV):
            op_tok = self.current_tok
            self.advance()
            right = self.factor()
            left = BinOpNode(left, op_tok, right)

        return left

    def factor(self):
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(tok)

        elif tok.type == TT_LPAREN:
            self.advance()
            result = self.expr() #anything after ( must be an espression

            if self.current_tok is None or self.current_tok.type != TT_RPAREN:
                raise Exception("Syntax Error: missing ')'")

            self.advance()
            return result
        elif tok.type == TT_IDENTIFIER:
            self.advance()
            return VarAccessNode(tok)

        else:
            raise Exception(f"Syntax Error: unexpected token '{tok}'")
        
#######################################
# INTERPRETER
#######################################

symbol_table = {}

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method) #looks for method, if not found then error, avoids long if-else
        return method(node)
    
    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return node.tok.value
    
    def visit_BinOpNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)

        if node.op_tok.type == TT_PLUS:
            return left_val + right_val
        elif node.op_tok.type == TT_MINUS:
            return left_val - right_val
        elif node.op_tok.type == TT_MUL:
            return left_val * right_val
        elif node.op_tok.type == TT_DIV:
            return left_val / right_val
        
    def visit_VarAssignNode(self, node):
        value = self.visit(node.value_node) #evaluates the expression and stores result
        symbol_table[node.var_name_tok.value] = value
        return value

    def visit_VarAccessNode(self, node):
        var_name = node.var_name_tok.value
        if var_name not in symbol_table:
            raise Exception(f"Variable '{var_name}' is not defined") #error if var was never defined
        return symbol_table[var_name]
    
    def visit_PrintNode(self, node):
        value = self.visit(node.value_node)
        return value


#######################################
# RUN
#######################################

def run(text):
    lines = text.split('\n')
    outputs = []
    last_expr_result = None

    for line in lines:
        line = line.strip() #remove extra spaces
        if line == "":  #skips empty lines
            continue

        lexer = Lexer(line)
        tokens = lexer.make_tokens()

        parser = Parser(tokens)
        ast = parser.parse()

        interpreter = Interpreter()
        value = interpreter.visit(ast)

        if isinstance(ast, PrintNode): #checks if print, if yes prints if no evaluates and eval expr and prints it
            outputs.append(value)
        else:
            last_expr_result = value

    if len(outputs) == 1:
        return outputs[0] #5 instead of [5]
    if len(outputs) > 1:
        return outputs #a list of outputs

    return last_expr_result if last_expr_result is not None else ""
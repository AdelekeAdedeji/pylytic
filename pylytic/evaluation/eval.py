import pylytic.math_methods.m_eval
from pylytic.storage import EvalConstants
from dataclasses import dataclass
from typing import Any
from pylytic.extras import validate_type


# Evaluating complex expressions

@dataclass
class Token:
    """
    class Tokens represent Token_types created during lexical analysis
    """
    token_type: str | EvalConstants
    value: Any = None

    def __repr__(self):
        return f"{self.token_type}: {self.value}"


class Lexer:
    """
    class Lexer implements lexical analysis to convert complex mathematical expressions into a sequence of tokens
    """

    def __init__(self, expression: str):
        self.expression = iter(expression)
        self.current_char = None
        self.l_count, self.r_count = 0, 0
        self.next_obj()

    def next_obj(self):
        """
        Advances the lexer to the next character
        :return: None
        """
        try:
            self.current_char = next(self.expression)

        except StopIteration:
            self.current_char = None

    def syntax_error(self):
        """
        raises syntax error if expected syntax is broken
        :return: None
        """
        raise Exception("Error: Invalid syntax !!!")

    def function_error(self):
        """
        raises error if unrecognized function is encountered in the expression
        :return: None
        """
        raise Exception("Error: Unrecognized function !!!")

    def tokens(self):
        """
        A generator that yields Tokens from expressions
        :return:
        """
        while self.current_char is not None:
            if (isinstance(self.current_char, str) and self.current_char.isalpha()) or self.current_char == "!":
                create_function = self.create_function()
                yield create_function if isinstance(create_function, Token) else self.create_constants(create_function)

            elif isinstance(self.current_char, str) and self.current_char in EvalConstants.NUMBER.value:
                yield self.create_number()

            elif isinstance(self.current_char, str) and self.current_char in EvalConstants.SPACES.value:
                self.next_obj()

            elif isinstance(self.current_char, str) and self.current_char in EvalConstants.OPERATOR.value:
                if EvalConstants.OPERATOR.value.get(self.current_char) == "L_PAREN":
                    self.l_count += 1

                elif EvalConstants.OPERATOR.value.get(self.current_char) == "R_PAREN":
                    self.r_count += 1

                yield Token(EvalConstants.OPERATOR.name + f"_{EvalConstants.OPERATOR.value.get(self.current_char)}",
                            self.current_char)
                self.next_obj()

    def create_number(self):
        """
        Constructs numeric tokens with its token type and value
        :return: Number token
        """
        number_str = ""
        while isinstance(self.current_char, str) and self.current_char in EvalConstants.NUMBER.value:
            number_str += self.current_char
            self.next_obj()

        return Token(EvalConstants.NUMBER.name, float(number_str))

    def unknown_type_error(self, type_):
        """
        raises an error for unrecognized token types
        :param type_: constant_str
        :return: None
        """
        raise Exception(f"Error: Unrecognized value {type_}")

    def create_constants(self, const_str: str):
        """
        Constructs a constant token with its token type and value
        :param const_str:
        :return: Constant token
        """
        constant_str = const_str
        if constant_str in EvalConstants.CONSTANT.value:
            return Token(EvalConstants.CONSTANT.name + f"_{constant_str}",
                         EvalConstants.CONSTANT.value.get(constant_str)
                         )

        self.unknown_type_error(f"{constant_str}{self.current_char if self.current_char is not None else ''}")

    def create_function(self):
        """
        Constructs a function token with its token type and value
        :return: Function token
        """
        function_str = ""
        while (isinstance(self.current_char, str) and self.current_char.isalpha()) or self.current_char == "!":
            function_str += self.current_char.lower()
            self.next_obj()

            if (function_str in EvalConstants.FUNCTION.value and self.current_char == "(") or function_str == "!":
                return Token(EvalConstants.FUNCTION.name, function_str)

            elif function_str not in EvalConstants.FUNCTION.value and self.current_char == "(":
                self.function_error()

            elif self.current_char is None:
                continue

        return function_str


@dataclass
class AbstractSyntaxTree:
    """
    Super class of BinOpNode, NumberNode, FunctionNode, ConstantNode and UnaryOpNode
    """
    pass


class ConstantNode(AbstractSyntaxTree):
    """
    class ConstantNode represents a constant node in the Abstract Syntax Tree
    """

    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class BinOpNode(AbstractSyntaxTree):
    """
    class BinOpNode represents an operator node in the Abstract Syntax Tree
    """

    def __init__(self, left_node, op, right_node):
        self.left = left_node
        self.op = op
        self.right = right_node


class NumberNode(AbstractSyntaxTree):
    """
    class NumberNode represents a number node in the Abstract Syntax Tree
    """

    def __init__(self, token: Token):
        self.token = token
        self.value = token.value


class FunctionNode(AbstractSyntaxTree):
    """
    class FunctionNode represent a function node in the Abstract Syntax Tree
    """

    def __init__(self, token: Token, argument1, argument2=None):
        self.token = token
        self.value = token.value
        self.first_argument = argument1
        self.second_argument = argument2


class UnaryOpNode(AbstractSyntaxTree):
    """
    class UnaryOpNode represents a unary operator node in the Abstract Syntax Tree
    """

    def __init__(self, token: Token, operand):
        self.token = token
        self.value = operand


class Parser:
    """
    Follows Grammar rules and implements recursive decent parsing to transform a token sequence into an AST
    """
    def __init__(self, lexer: Lexer):
        self.lexer, self.lexer_tokens = lexer, lexer.tokens()
        self.end_of_tokens = Token("EOF", None)
        self.current_token = self.advance()
        self.expected_types = "!", "+", "-", "*", "/", "^", ")", EvalConstants.SPACES.value

    def error(self):
        """
        :return: None
        """
        raise Exception("Invalid Syntax!!!")

    def advance(self):
        """
        function to advance to the next token in the sequence
        :return: None
        """
        try:
            return next(self.lexer_tokens)

        except StopIteration:
            return self.end_of_tokens

    def check_paren(self):
        """
        raises error for unmatched number of parentheses in expression
        :return: None
        """
        if self.lexer.l_count != self.lexer.r_count:
            self.error()

    def consume(self, token_type):
        """
        validates and consumes a token of the specified type
        :param token_type: token_type of Token class
        :return: None
        """
        if self.current_token.token_type == token_type:
            self.current_token = self.advance()
        else:
            self.error()

    def unit(self):
        """
           Implements the unit grammar rule. Parses atomic units of the expression, such as numbers,
           parenthesized sub-expressions, functions, constants, or unary operations.

           Grammar Rule:
            unit ::= NUMBER | CONSTANT | '(' expression ')' | FUNCTION '(' expression ')' | UNARY ('+' | '-')

           :return: AST Node representing the parsed unit (NumberNode, FunctionNode, UnaryOpNode, or ConstantNode).
           :raises: SyntaxError if an invalid token sequence is encountered.
        """

        token = self.current_token

        if token.token_type == EvalConstants.NUMBER.name:
            self.consume(EvalConstants.NUMBER.name)
            return NumberNode(token)

        elif token.token_type == "OPERATOR_L_PAREN":
            self.consume("OPERATOR_L_PAREN")
            node = self.expression()
            self.consume("OPERATOR_R_PAREN")
            return node

        elif token.token_type == EvalConstants.FUNCTION.name:
            self.consume(EvalConstants.FUNCTION.name)
            self.consume("OPERATOR_L_PAREN")
            argument = self.expression()
            self.consume("OPERATOR_R_PAREN")

            if self.current_token.value in self.expected_types or self.current_token == self.end_of_tokens:
                return FunctionNode(token, argument)

        elif token.token_type == "OPERATOR_PLUS" or token.token_type == "OPERATOR_MINUS":
            self.consume(token.token_type)
            return UnaryOpNode(token, self.unit())

        elif token.token_type in ("CONSTANT_e", "CONSTANT_pi"):
            self.consume(token.token_type)

            if self.current_token.value in self.expected_types or self.current_token == self.end_of_tokens:
                return ConstantNode(token)

        self.error()

    def factor(self):
        """
        Implements factor grammar rule. Parses factors, which may include units combined with factorials, permutations,
        or combinations.

        Grammar Rule:
         factor ::= unit | factor '!' | factor ('P' | 'C') '(' expression ')'

        :return: AST Node representing the parsed factor (FunctionNode or unit-based Node).
        :raises: SyntaxError if an invalid token sequence is encountered.
        """

        node = self.unit()
        while (self.current_token.token_type == EvalConstants.FUNCTION.name and
               self.current_token.value.lower() in ("p", "c", "!")):
            token = self.current_token

            if token.value == "!":
                self.consume(token.token_type)
                node = FunctionNode(token, node)

            elif token.value.lower() in ("p", "c"):
                self.consume(token.token_type)
                self.consume("OPERATOR_L_PAREN")
                second_argument = self.expression()
                self.consume("OPERATOR_R_PAREN")
                node = FunctionNode(token, node, second_argument)

        if self.current_token.value in self.expected_types or self.current_token == self.end_of_tokens:
            return node

        self.error()

    def low_term(self):
        """
        Implements low term grammar rule. Parses terms involving exponentiation, where factors are combined with the
        power operator.

        Grammar Rule:
         low_term ::= factor | factor '^' low_term

        :return: BinOpNode representing the parsed exponentiation operation or a factor node.
        :raises: SyntaxError if an invalid token sequence is encountered.
        """

        node = self.factor()
        while self.current_token.token_type == "OPERATOR_POWER":
            token = self.current_token
            self.consume("OPERATOR_POWER")
            node = BinOpNode(node, token, self.low_term())

        return node

    def term(self):
        """
        Implements term grammar rule. Parses terms involving multiplication and division, combining lower precedence
        operations.

        Grammar Rule:
         term ::= low_term | term (('*' | '/') low_term)*

        :return: BinOpNode representing the parsed multiplication or division operation.
        :raises: SyntaxError if an invalid token sequence is encountered.
        """

        node = self.low_term()
        while self.current_token.token_type in ("OPERATOR_MUL", "OPERATOR_DIV"):
            token = self.current_token

            if token.token_type == "OPERATOR_MUL":
                self.consume("OPERATOR_MUL")

            elif token.token_type == "OPERATOR_DIV":
                self.consume("OPERATOR_DIV")

            node = BinOpNode(node, token, self.low_term())

        return node

    def expression(self):
        """
        Embodies expression grammar rule. Parses expressions involving addition and subtraction,
        which are the highest-level operations.

        Grammar Rule:
         expression ::= term (('+' | '-') term)*

        :return: BinOpNode representing the parsed addition or subtraction operation.
        :raises: SyntaxError if an invalid token sequence is encountered.
        """

        node = self.term()
        while self.current_token.token_type in ("OPERATOR_PLUS", "OPERATOR_MINUS"):
            token = self.current_token

            if token.token_type == "OPERATOR_PLUS":
                self.consume("OPERATOR_PLUS")

            elif token.token_type == "OPERATOR_MINUS":
                self.consume("OPERATOR_MINUS")

            node = BinOpNode(node, token, self.term())

        return node

    def parse_expression(self):
        """
        Executes parsing and constructs the AST
        :return:
        """
        expr = self.expression()
        self.check_paren()
        return expr


class Interpreter:
    """
    Traverses the AST to evaluate mathematical expressions.
    """
    def __init__(self, parser: Parser, mode: str, base: int | float):
        self.parser = parser
        self.mode = mode
        self.base = base

    def visit(self, node: BinOpNode | FunctionNode | UnaryOpNode | ConstantNode | NumberNode):
        """
        Employs Generic visitation to dynamically resolve and process nodes efficiently.
        Routes execution to the appropriate visit method based on the node type.
        :param node: AST node types
        :return: int | float
        """
        method_name = "visit_" + type(node).__name__
        method = getattr(self, method_name)
        return method(node)

    def visit_BinOpNode(self, node: BinOpNode) -> int | float:
        """
        Evaluates BinOpNode and performs binary operations
        :param node: node of type BinOpNode
        :return: integer or float
        """
        if node.op.token_type == "OPERATOR_PLUS":
            return self.visit(node.left) + self.visit(node.right)

        elif node.op.token_type == "OPERATOR_MINUS":
            return self.visit(node.left) - self.visit(node.right)

        elif node.op.token_type == "OPERATOR_MUL":
            return self.visit(node.left) * self.visit(node.right)

        elif node.op.token_type == "OPERATOR_DIV":
            try:
                return self.visit(node.left) / self.visit(node.right)

            except ZeroDivisionError:
                raise Exception("ZeroDivisionError: float division by zero")

        elif node.op.token_type == "OPERATOR_POWER":
            return self.visit(node.left) ** self.visit(node.right)

    def visit_NumberNode(self, node: NumberNode) -> int | float:
        """
        returns the numeric value of the NumberNode
        :param node: node of type NumberNode
        :return: integer or float
        """
        return node.value

    def visit_ConstantNode(self, node: ConstantNode) -> float:
        """
        returns the numeric value of the ConstantNode
        :param node: node of type ConstantNode
        :return: integer or float
        """
        return node.value

    def visit_UnaryOpNode(self, node: UnaryOpNode) -> int | float:
        """
        Evaluates UnaryOpNode and performs unary operations
        :param node: node of type UnaryOpNode
        :return: integer or float
        """

        if node.token.token_type == "OPERATOR_PLUS":
            return + self.visit(node.value)
        elif node.token.token_type == "OPERATOR_MINUS":
            return - self.visit(node.value)

    def function_error(self):
        """
        raises error if function is not supported
        :return: None
        """
        raise Exception("Function not found!!!")

    def visit_FunctionNode(self, node: FunctionNode) -> int | float:
        """
        Evaluates FunctionNode and performs operations on function calls with arguments
        :param node: node of type FunctionNode
        :return: integer or float
        """
        if node.token.token_type == EvalConstants.FUNCTION.name:
            try:
                method = getattr(pylytic.math_methods.m_eval, node.value)
                check_mode = "mode" in method.__annotations__.keys()
                check_base = "base" in method.__annotations__.keys()
                if check_mode:
                    return method(self.visit(node.first_argument), self.mode)
                elif check_base:
                    return method(self.visit(node.first_argument), self.base)
                else:
                    return method(self.visit(node.first_argument))

            except AttributeError:
                if node.value.lower() == "p":
                    first_node, second_node = self.visit(node.first_argument), self.visit(node.second_argument)
                    return pylytic.math_methods.m_eval.perm(int(first_node) if not first_node - int(first_node) else
                                                            first_node, int(second_node) if not second_node - int(
                        second_node) else second_node)
                elif node.value.lower() == "c":
                    first_node, second_node = self.visit(node.first_argument), self.visit(node.second_argument)
                    return pylytic.math_methods.m_eval.comb(int(first_node) if not first_node - int(first_node) else
                                                            first_node, int(second_node) if not second_node - int(
                        second_node) else second_node)
                elif node.value == "!":
                    first_node = self.visit(node.first_argument)
                    return pylytic.math_methods.m_eval.factorial(int(first_node) if not first_node - int(first_node)
                                                                 else first_node)

    def evaluate(self) -> int | float:
        """
        Evaluates the parsed expression and returns the computed result
        :return: integer or float
        """
        value_ = self.parser.parse_expression()
        return self.visit(value_)


@validate_type
def eval_complex(expr: str, mode: str = "deg",
                 logarithmic_base: int | float = 10) -> int | float:
    """
    Evaluates mathematical expressions, has optional angle mode and logarithmic base
    :param expr: str -> Required, mathematical expression to evaluate
    :param mode: str ->  Required for expressions containing trig functions,
                options include deg, rad or grad, defaults to deg
    :param logarithmic_base: -> int | float Base for logarithmic functions defaults to base 10
    :return: -> int | float computed result
    """
    interpreter = Interpreter(Parser(Lexer(expr)), mode, logarithmic_base)
    return interpreter.evaluate()


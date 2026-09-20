from dataclasses import dataclass
from enum import Enum


class Keyword(Enum):
    """Palavra-chave"""

    FUNCTION = "function"
    IF = "if"
    ELSE = "else"
    LOOP = "loop"
    IN = "in"
    RETURN = "return"
    VAR = "var"
    INT = "int"
    DECIMAL = "decimal"
    STRING = "string"
    BOOL = "bool"


class Operator(Enum):
    """Operador"""

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"
    PERCENT = "%"
    EQ = "="
    EQ_EQ = "=="
    BANG = "!"
    NOT_EQ = "!="
    LT = "<"
    GT = ">"
    LT_EQ = "<="
    GT_EQ = ">="
    OR = "||"
    AND = "&&"
    AMPERSAND = "&"
    DOT_DOT = ".."
    ARROW = "->"


class Delimiter(Enum):
    """Delimitador"""

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
    LBRACKET = "["
    RBRACKET = "]"
    COMMA = ","
    SEMICOLON = ";"


@dataclass(frozen=True, slots=True)
class Span:
    """Posição do token no arquivo"""

    line: int
    col: int


@dataclass(frozen=True, slots=True)
class TokenInt:
    """Valor inteiro"""

    value: int
    span: Span


@dataclass(frozen=True, slots=True)
class TokenDecimal:
    """Valor decimal (exemplo: 3.14)"""

    value: float
    span: Span


@dataclass(frozen=True, slots=True)
class TokenString:
    """Valor string"""

    value: str
    span: Span


@dataclass(frozen=True, slots=True)
class TokenBool:
    """Valor booleano"""

    value: bool
    span: Span


@dataclass(frozen=True, slots=True)
class TokenIdentifier:
    """Identificador"""

    name: str
    span: Span


@dataclass(frozen=True, slots=True)
class TokenKeyword:
    """Palavra-chave"""

    kind: Keyword
    span: Span


@dataclass(frozen=True, slots=True)
class TokenOperator:
    """Operador"""

    kind: Operator
    span: Span


@dataclass(frozen=True, slots=True)
class TokenDelimiter:
    """Delimitador"""

    kind: Delimiter
    span: Span


@dataclass(frozen=True, slots=True)
class TokenEOF:
    """Fim do arquivo"""

    span: Span


type Token = (
    TokenInt
    | TokenDecimal
    | TokenString
    | TokenBool
    | TokenIdentifier
    | TokenKeyword
    | TokenOperator
    | TokenDelimiter
    | TokenEOF
)

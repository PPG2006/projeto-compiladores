import sys

from lang.errors import LexicalError
from lang.lexer import Lexer
from lang.scanner import Scanner
from lang.symbol_table import SymbolTable
from lang.tokens import (
    Token,
    TokenBool,
    TokenDecimal,
    TokenDelimiter,
    TokenEOF,
    TokenIdentifier,
    TokenInt,
    TokenKeyword,
    TokenOperator,
    TokenString,
)


def formatar_token(t: Token, symbol_table: SymbolTable) -> str:
    nome = type(t).__name__.replace("Token", "")
    pos = f"linha {t.span.line}, coluna {t.span.col}"

    match t:
        case TokenKeyword(kind) | TokenOperator(kind) | TokenDelimiter(kind):
            return f"{nome}({kind.value!r}) @ {pos}"
        case (
            TokenBool(value)
            | TokenInt(value)
            | TokenDecimal(value)
            | TokenString(value)
        ):
            return f"{nome}({value!r}) @ {pos}"
        case TokenIdentifier(id):
            return f"{nome}({symbol_table.consultar(id).name}) @ {pos}"  # pyright: ignore[reportOptionalMemberAccess]
        case TokenEOF():
            return f"EOF @ {pos}"


def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src.main caminho/do/arquivo.txt")
        sys.exit(1)

    scanner = Scanner(sys.argv[1])
    symbol_table = SymbolTable()
    lexer = Lexer(scanner, symbol_table)

    tokens = []
    try:
        while True:
            token = lexer.next_token()
            if isinstance(token, TokenEOF):
                break
            tokens.append(token)
    except LexicalError as e:
        print(str(e))
        sys.exit(1)

    for t in tokens:
        print(formatar_token(t, symbol_table))
    print(f"\n{len(tokens)} tokens reconhecidos.\n")

    print("Tabela de símbolos")
    for s in symbol_table.tabela.values():
        print(f'"{s.name}" (referências: {s.count})')


if __name__ == "__main__":
    main()

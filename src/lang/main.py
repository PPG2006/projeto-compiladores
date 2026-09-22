import sys
from lang.scanner import Scanner
from lang.lexer import Lexer
from lang.tokens import TokenEOF
from lang.errors import LexicalError

def formatar_token(t) -> str:
    nome = type(t).__name__.replace("Token", "")
    pos = f"linha {t.span.line}, coluna {t.span.col}"
    if hasattr(t, "value"):   # Int, Decimal, String, Bool
        return f"{nome}({t.value!r}) @ {pos}"
    if hasattr(t, "name"):    # Identifier
        return f"{nome}({t.name!r}) @ {pos}"
    if hasattr(t, "kind"):    # Keyword, Operator, Delimiter
        return f"{nome}({t.kind.value!r}) @ {pos}"
    return f"{nome} @ {pos}"  # EOF

def main():
    if len(sys.argv) != 2:
        print("Uso: python -m src.main caminho/do/arquivo.txt")
        sys.exit(1)

    scanner = Scanner(sys.argv[1])
    lexer = Lexer(scanner)

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
        print(formatar_token(t))
    print(f"\n{len(tokens)} tokens reconhecidos.")

if __name__ == "__main__":
    main()

from lang.scanner import Scanner

scan = Scanner("examples/a.txt")

while not scan.eof():
    print(
        f"(linha, coluna): ({scan.get_row()}, {scan.get_column()}) -- {scan.advance()!r}"
    )

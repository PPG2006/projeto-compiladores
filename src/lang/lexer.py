from .scanner import Scanner
from .tokens import *

class Lexer:

    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self.char = None  

    def _skip(self):
        # Pular comentarios ou espaços em brancos, quebras de linhas
        while True:
            if self.char in (" ", "\t", "\r", "\n"):
                self.scanner.advance()
                self.char = self.scanner.peek()
            elif self.char == '/' and self.scanner.peek_next() == '/':
                while self.char not in ('\n', Scanner.EOF):
                    self.scanner.advance()
                    self.char = self.scanner.peek()
            else:
                break
                
    def next_token(self) -> Token:
        self.char = self.scanner.peek()
        self._skip()
        self.char = self.scanner.peek()
        
        linha = self.scanner.get_row()
        coluna = self.scanner.get_column()
        span_atual = Span(line=linha, col=coluna)

        if self.char == Scanner.EOF:
            return TokenEOF(span=span_atual) 
        if self.char.isalpha() or self.char == '_': 
            return self._read_letter(span_atual)
        elif self.char.isdigit():
            return self._read_number(span_atual)
        elif self.char == '"':
            return self._read_string(span_atual)
        else:
            return self._read_operator_or_delimiter(span_atual)

    def _read_number(self, span: Span) -> Token:
        #Retorna token decimal ou inteiro
        num_txt  = ''
        dot_count = 0
        
        while self.char != Scanner.EOF and (self.char.isdigit() or self.char == '.'):        
            if self.char == '.':
                if self.scanner.peek_next() == '.':
                    break
                if dot_count == 1: 
                    break     
                dot_count += 1
            
            num_txt += self.char
            self.scanner.advance()
            self.char = self.scanner.peek()

        if dot_count == 0:
            return TokenInt(value=int(num_txt), span=span)
        else:
            return TokenDecimal(value=float(num_txt), span=span)


    def _read_letter(self, span: Span) -> Token:
        #Identifica se é  um booleano, um token Keyword(palavra reservada)
        #ou um token Identifier (nome dado pelo programador(a))

        texto = ""
        while self.char != Scanner.EOF and (self.char.isalnum() or self.char == '_'):
            texto += self.char
            self.scanner.advance()
            self.char = self.scanner.peek()

        if texto == "true":
            return TokenBool(value=True, span=span)
        elif texto == "false":
            return TokenBool(value=False, span=span)

        token_keyword = TokenKeyword.try_from_str(texto, span)    
        if token_keyword is not None:
            return token_keyword
        
        return TokenIdentifier(name=texto, span=span)

    def _read_string(self, span: Span) -> Token:
        #Identifica strings (consome apenas o que está dentro dos "")
        texto = ""
        
        self.scanner.advance()
        self.char = self.scanner.peek()

        while self.char != Scanner.EOF and self.char != '"':
            texto += self.char
            self.scanner.advance()
            self.char = self.scanner.peek()

        if self.char == Scanner.EOF:
            raise Exception(f"Erro Léxico: String não fechada iniciada na linha {span.line}, coluna {span.col}.")

        self.scanner.advance()
        self.char = self.scanner.peek()

        return TokenString(value=texto, span=span)

    def _read_operator_or_delimiter(self, span: Span) -> Token:
        #Tenta operador duplo (ex: =!)
        token_operator = TokenOperator.try_from_str(self.char + self.scanner.peek_next(), span)
        if token_operator is not None:
            self.scanner.advance()
            self.scanner.advance()
            self.char = self.scanner.peek()
            return token_operator

        #Tenta operador com 1 caractere
        token_operator = TokenOperator.try_from_str(self.char, span)
        if token_operator is not None:
            self.scanner.advance()
            self.char = self.scanner.peek()
            return token_operator

        #Tenta delimitador (ex: ';', '(', ')', '{')
        token_delim = TokenDelimiter.try_from_str(self.char, span)
        if token_delim is not None:
            self.scanner.advance()
            self.char = self.scanner.peek()
            return token_delim 

        simbolo_invalido = self.char
        self.scanner.advance()
        self.char = self.scanner.peek()
        raise Exception(f"Erro Léxico: Símbolo inválido '{simbolo_invalido}' na linha {span.line}, coluna {span.col}.")


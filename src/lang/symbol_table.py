from lang.tokens import Keyword

# Essa classe guarda todas as palavras que o lexer encontrou no código,
# tipo uma lista de "quem é quem"
class SymbolTable:
    def __init__(self):
        self.tabela = {}  # dicionario: nome da palavra -> informacoes dela

    def inserir(self, nome, linha, coluna):
        # se a palavra ja apareceu antes, so soma mais uma vez
        if nome in self.tabela:
            self.tabela[nome]["vezes_encontrado"] += 1
            return self.tabela[nome]

        # se for a primeira vez, verifica se é palavra reservada (tipo "var", "if")
        # ou um nome que a pessoa que programou inventou (tipo "x", "soma")
        eh_palavra_reservada = Keyword.try_from_str(nome) is not None

        self.tabela[nome] = {
            "nome": nome,
            "eh_palavra_reservada": eh_palavra_reservada,
            "linha": linha,
            "coluna": coluna,
            "vezes_encontrado": 1,
        }
        return self.tabela[nome]

    def consultar(self, nome):
        # devolve as infos da palavra, ou None se ela nunca apareceu
        return self.tabela.get(nome)

    def existe(self, nome):
        # so responde True ou False
        return nome in self.tabela

    def quantidade_de_nomes(self):
        return len(self.tabela)


if __name__ == "__main__":
    # teste rapido pra ver se ta funcionando
    tabela = SymbolTable()
    tabela.inserir("var", linha=1, coluna=1)
    tabela.inserir("x", linha=1, coluna=5)
    tabela.inserir("x", linha=3, coluna=2)  # "x" apareceu de novo

    print(tabela.consultar("x"))

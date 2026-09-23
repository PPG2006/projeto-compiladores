from dataclasses import dataclass


@dataclass
class SymbolEntry:
    id: int
    name: str
    count: int = 1


# Essa classe guarda todas as palavras que o lexer encontrou no código,
# tipo uma lista de "quem é quem"
class SymbolTable:
    tabela: dict[int, SymbolEntry]

    def __init__(self):
        self.tabela = {}  # dicionario: nome da palavra -> informacoes dela

    def inserir(self, nome) -> SymbolEntry:
        # se a palavra ja apareceu antes, so soma mais uma vez
        id = hash(nome)
        if nome in self.tabela:
            self.tabela[id].count += 1
            return self.tabela[id]

        self.tabela[id] = SymbolEntry(id=id, name=nome)
        return self.tabela[id]

    def consultar(self, id):
        # devolve as infos da palavra, ou None se ela nunca apareceu
        return self.tabela.get(id)

    def consultar_por_nome(self, nome):
        return self.tabela.get(hash(nome))

    def existe(self, id):
        # so responde True ou False
        return id in self.tabela

    def existe_por_nome(self, nome):
        return hash(nome) in self.tabela

    def tamanho(self):
        return len(self.tabela)


if __name__ == "__main__":
    # teste rapido pra ver se ta funcionando
    tabela = SymbolTable()
    tabela.inserir("print")
    tabela.inserir("x")
    tabela.inserir("x")  # "x" apareceu de novo

    print(tabela.consultar("x"))

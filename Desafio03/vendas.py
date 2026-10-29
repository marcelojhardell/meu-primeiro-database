import sqlite3
from rich import print
from datetime import date
try:
    with sqlite3.connect("Vendas.db") as loja:
        loja.row_factory = sqlite3.Row
        cur = loja.cursor()
        while True:
            print("===== SISTEMA DE VENDAS =====")
            op = int(input("""1 - Cadastrar venda
2 - Listar vendas
3 - Pesquisar cliente
4 - Total vendido
5 - Produto mais caro
6 - Remover venda
7 - Relatório de vendas 
0 - Sair do programa: """))
            if op == 1:
                cliente = input("Digite o nome do cliente: ")
                produto = input("Digite o nome do produto: ")
                valor = float(input("Digite o valor do produto: "))
                data_venda = input("Digite a data da venda do produto: ")
                if data_venda == "":
                    print("Data nao informada")
                else:
                    try:
                        data = date.fromisoformat(data_venda)
                        cur.execute("INSERT INTO Vendas (Cliente, Produto, valor, data_venda) VALUES (?, ?, ?, ?)",
                                    (cliente, produto, valor, data_venda))
                        loja.commit()
                    except ValueError:
                        print("Data inválida")

            elif op == 2:
                cur.execute("SELECT * FROM Vendas")
                print("===============================")
                print("[black on yellow]Listando os produtos vendidos[/]")
                print("===============================")
                print("-------------------------------")
                for venda in cur:
                    print(f"Produto: {venda['Produto']} | Valor: R${venda['valor']:.2f}")
                print("-------------------------------")
            elif op == 3:
                search = input("Digite o nome do cliente: ")
                cur.execute("SELECT * FROM Vendas WHERE Cliente LIKE ?", (f"%{search}%",))
                total = 0
                for total, busca in enumerate(cur, start=1):
                    print(f"{busca['Cliente']}")
                if total == 0:
                    print(f"O Cliente que vc procurou com nome {search} não existe!!!")

            elif op == 4:
                cur.execute("SELECT * FROM Vendas")
                total_vendas = 0
                print("As vendas cadastradas foram:", end="")
                for total_vendas, venda in enumerate(cur, start=1):
                    print(f"{venda['Produto']},", end=" ")
                print()
                print(f"O total de produtos vendidos foi [green]{total_vendas}[/]")

            elif op == 5:
                cur.execute("SELECT * FROM Vendas")
                maior = 0
                produto_caro = ''
                for caro in cur:
                    if caro['valor'] > maior:
                        maior = caro['valor']
                        produto_caro = caro['Produto']
                print(f"O produto mais caro dessa tabela é: {produto_caro} que custa [green]R${maior}[/]")

            elif op == 6:
                busca = input("Digite o Id para remover a venda: ")
                cur.execute("DELETE FROM Vendas WHERE Id = ?", (busca,))

                if cur.rowcount > 0:
                    print("[green]Venda excluida com sucesso![/]")
                else:
                    print("[red]Nenhuma venda encontrada com esse Id[/]")
                loja.commit()
            elif op == 7:
                search = str(input("Digite o nome do cliente: "))
                cur.execute("SELECT * FROM Vendas WHERE CLiente LIKE ?", (f"%{search}%",))
                total = 0
                print("=-=-= RELATÓRIO POR CLIENTE =-=-=")
                for total, produto in enumerate(cur, start = 1):
                    print(f"{produto['Cliente']} - Total gasto: R${produto['valor']:.2f}")
                if total == 0:
                    print(f"Erro!!! esse nome {search} é inexistente")
            elif op == 0:
                break




except sqlite3.Error as erro:
    print(f"Erro no banco: {erro}")

except Exception as erro:
    print(f"Algo deu errado: {erro}")

import requests 

BASE_URL = "http://127.0.0.1:5000"


# --------- USUÁRIOS ---------
def criar_usuario():
    nome = input("Nome: ")
    email = input("Email: ")
    payload = {"nome": nome, 
               "email": email}
    r = requests.post(f"{BASE_URL}/usuarios", json=payload)
    print(r.json())


def listar_usuarios():
    r = requests.get(f"{BASE_URL}/usuarios")
    usuarios = r.json()
    print("\n--- USUÁRIOS ---")
    for u in usuarios:
        print(f"ID: {u['id_usuario']} - Nome: {u['nome']} - Email: {u['email']}")


# --------- SETORES ---------
def criar_setor():
    nome = input("Nome do setor: ")
    payload = {"nome": nome}
    r = requests.post(f"{BASE_URL}/setores", json=payload)
    print(r.json())


def listar_setores():
    r = requests.get(f"{BASE_URL}/setores")
    setores = r.json()
    print("\n--- SETORES ---")
    for s in setores:
        print(f"ID: {s['id_setor']} - Nome: {s['nome']}")


# --------- CHAMADOS ---------
def criar_chamado():
    titulo = input("Título: ")
    descricao = input("Descrição: ")

    # Seleciona usuário
    r = requests.get(f"{BASE_URL}/usuarios")
    usuarios = r.json()
    print("\n--- USUÁRIOS ---")
    for u in usuarios:
        print(f"ID: {u['id_usuario']} - Nome: {u['nome']}")
    id_usuario = int(input("Escolha o ID do solicitante: "))

    # Seleciona setor
    r = requests.get(f"{BASE_URL}/setores")
    setores = r.json()
    print("\n--- SETORES ---")
    for s in setores:
        print(f"ID: {s['id_setor']} - Nome: {s['nome']}")
    id_setor = int(input("Escolha o ID do setor: "))

    prioridade = input("Prioridade (alta/media/baixa): ")

    payload = {
        "titulo": titulo,
        "descricao": descricao,
        "id_usuario": id_usuario,
        "id_setor": id_setor,
        "prioridade": prioridade
    }

    r = requests.post(f"{BASE_URL}/chamados", json=payload)
    print("\nResposta:")
    print(r.json())


def listar_chamados():
    r = requests.get(f"{BASE_URL}/chamados")
    chamados = r.json()
    print("\n--- CHAMADOS ---")
    for c in chamados:
        print(f"""
ID: #{c['id_chamado']}
Título: {c['titulo']}
Solicitante: {c['solicitante']}
Setor: {c['setor']}
Prioridade: {c['prioridade']}
Status: {c['status']}
Data: {c['criado_em']}
---------------------------
""")


def atualizar_status():
    id_chamado = input("ID do chamado: ")
    status = input("Novo status (aberto/em_andamento/concluido): ")
    r = requests.put(f"{BASE_URL}/chamados/{id_chamado}", json={"status": status})
    print(r.json())


def atualizar_prioridade():
    id_chamado = input("ID do chamado: ")
    prioridade = input("Nova prioridade (alta/media/baixa): ")
    r = requests.put(f"{BASE_URL}/chamados/{id_chamado}", json={"prioridade": prioridade})
    print(r.json())


def deletar_chamado():
    id_chamado = input("ID do chamado: ")
    r = requests.delete(f"{BASE_URL}/chamados/{id_chamado}")
    print(r.json())


# --------- MENU PRINCIPAL ---------
def menu():
    while True:
        print("""
==== SISTEMA DE CHAMADOS ====
1 - Criar usuário
2 - Listar usuários
3 - Criar setor
4 - Listar setores
5 - Criar chamado
6 - Listar chamados
7 - Atualizar status do chamado
8 - Atualizar prioridade do chamado
9 - Deletar chamado
0 - Sair
""")
        opcao = input("Escolha: ")

        if opcao == "1":
            criar_usuario()
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            criar_setor()
        elif opcao == "4":
            listar_setores()
        elif opcao == "5":
            criar_chamado()
        elif opcao == "6":
            listar_chamados()
        elif opcao == "7":
            atualizar_status()
        elif opcao == "8":
            atualizar_prioridade()
        elif opcao == "9":
            deletar_chamado()
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida")


if __name__ == "__main__":
    menu()

import os



def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def sacar(*, saldo, valor, extrato):
    if valor > saldo:
        print("Você não tem saldo suficiente.")
        input("Pressione ENTER para continuar...")
        return saldo, extrato

    if valor <= 0:
        print("Valor inválido para saque.")
        input("Pressione ENTER para continuar...")
        return saldo, extrato

    saldo -= valor
    extrato.append(f"[ SAQUE ] : R${valor:.2f}")
    print("Saque realizado com sucesso.")
    input("Pressione ENTER para continuar...")
    return saldo, extrato


def depositar(saldo, valor, extrato):
    if valor <= 0:
        print("Valor inválido para depósito")
        input("Pressione ENTER para continuar...")
        return saldo, extrato

    saldo += valor
    extrato.append(f"[DEPOSITO] : R${valor:.2f}")
    print(f"Depósito de R${valor:.2f} realizado com sucesso!")
    input("Pressione ENTER para continuar...")
    return saldo, extrato


def visualizar_historico(saldo, /, *, extrato=None):
    print("\n" + "="*40)
    print("              EXTRATO")
    print("="*40)

    if not extrato:
        print("Nenhuma movimentação registrada.")
    else:
        for linha in extrato:
            print(linha)

    print("="*40)
    print(f"Saldo atual: R${saldo:.2f}")
    print("="*40)
    input("\nPressione ENTER para continuar...")




def criar_usuario():
    print("\n" + "="*40)
    print("     Cadastro de novo usuário")
    print("="*40)

    nome_usuario = input("=> Nome: ")
    data_nascimento = input("=> Data de nascimento (dd/mm/aaaa): ")
    cpf = input("=> CPF (apenas números): ")

    print("\n--- Endereço ---")
    rua = input("=> Rua: ")
    nro = input("=> Nº da casa: ")
    bairro = input("=> Bairro: ")
    cidade = input("=> Cidade: ")
    sigla = input("=> UF (ex: ES): ").upper()

    existe = any(p["cpf"] == cpf for p in usuarios)

    if existe:
        print("Erro: CPF já cadastrado!")
        input("ENTER para continuar...")
        return None

    print("\nUsuário cadastrado com sucesso!\n")
    input("ENTER para continuar...")

    return {
        "nome_usuario": nome_usuario,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": f"{rua}, {nro} - {bairro} - {cidade}/{sigla}"
    }


def criar_conta_corrente(usuario, contas):
    numero_conta = len(contas) + 1
    agencia = "0001"

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": []
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Número: {numero_conta}, Agência: {agencia}")
    input("ENTER para continuar...")
    return conta


def retorna_usuario(usuarios):
    limpar_tela()
    print("\n" + "="*40)
    print("     Digite o CPF do usuário:")
    print("="*40)
    cpf_busca = input("=> ")

    for usuario in usuarios:
        if usuario.get("cpf") == cpf_busca:
            return usuario

    print("Usuário não encontrado!")
    input("ENTER para continuar...")
    return None


def retorna_conta(usuario, contas):
    contas_usuario = [c for c in contas if c["usuario"]["cpf"] == usuario["cpf"]]

    if not contas_usuario:
        print("Usuário não possui contas. Criando nova conta...")
        input("ENTER para continuar...")
        return criar_conta_corrente(usuario, contas)

    elif len(contas_usuario) == 1:
        return contas_usuario[0]

    else:
        print("Selecione uma conta:")
        for c in contas_usuario:
            print(f"[{c['numero_conta']}] Agência: {c['agencia']} - Conta: {c['numero_conta']}")

        while True:
            num = input("Número da conta: ")
            conta = next((c for c in contas_usuario if str(c["numero_conta"]) == num), None)
            if conta:
                return conta
            print("Conta inválida, tente novamente.")



usuarios = []
contas = []
conta = None
usuario = None

if __name__ == "__main__":
    while True:
        limpar_tela()
        if not usuario:
            print("\n" + "="*40)
            print("     Selecione uma opção:")
            print("="*40)
            print("[C] - Cadastrar novo usuário")
            print("[A] - Acessar conta")
            print("[S] - Sair")
            entrada = input(":> ").strip()
            opc = entrada[0].upper() if entrada else ""

            if opc == "A":
                usuario = retorna_usuario(usuarios)
            elif opc == "C":
                novo_usuario = criar_usuario()
                if novo_usuario:
                    usuarios.append(novo_usuario)
            elif opc == "S":
                break

        if usuario:
            conta = retorna_conta(usuario, contas)
            limpar_tela()

            print("\n" + "="*40)
            print(f"    Logado com usuário: {usuario.get('nome_usuario')}")
            print(f"    Conta: {conta.get('numero_conta')}")
            print("="*40)
            print("[C] - Cadastrar Conta")
            print("[T] - Trocar Conta")
            print("[D] - Depositar")
            print("[S] - Sacar")
            print("[E] - Extrato")
            print("[L] - Logout")
            entrada = input(":> ").strip()
            opc = entrada[0].upper() if entrada else ""

            if opc == "C":
                criar_conta_corrente(usuario, contas)

            if opc == "T":
                conta = retorna_conta(usuario, contas)

            if opc == "D":
                valor = float(input("Entre com o valor do depósito: R$"))
                conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])

            if opc == "S":
                try:
                    valor = float(input("Digite um valor para saque R$:"))
                    conta['saldo'], conta['extrato'] = sacar(
                        saldo=conta['saldo'],
                        valor=valor,
                        extrato=conta['extrato']
                    )
                except ValueError:
                    print("Valor inválido.")
                    input("ENTER para continuar...")

            if opc == "E":
                visualizar_historico(conta["saldo"], extrato=conta["extrato"])

            if opc == "L":
                usuario = None
                conta = None

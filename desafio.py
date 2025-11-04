class Contalterador:
    def __init__(self, contas):
        self.contas = contas
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.contas):
            conta = self.contas[self.index]
            self.index += 1
            return conta["numero_conta"], conta["saldo"], conta["usuario"]["nome"]
        else:
            raise StopIteration


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Já existe usuário com esse CPF!")
        return
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("Usuário criado com sucesso!")

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("Conta criada com sucesso!")
        return {
            "agencia": agencia,
            "numero_conta": numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "numero_saques": 0,
            "transacoes": []
        }
    print("Usuário não encontrado, fluxo de criação de conta encerrado!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def operar_conta(conta, limite, LIMITE_SAQUES):
    menu = """
    ======== MENU DE OPERAÇÕES ========
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair
    ===================================
    => """
    while True:
        opcao = input(menu)
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, transacoes = depositar(conta["saldo"], valor, conta["transacoes"])
            conta["saldo"] = saldo
            conta["transacoes"] = transacoes
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, sucesso, numero_saques, transacoes = sacar(
                saldo=conta["saldo"],
                valor=valor,
                limite=limite,
                numero_saques=conta["numero_saques"],
                limite_saques=LIMITE_SAQUES,
                transacoes=conta["transacoes"]
            )
            conta["saldo"] = saldo
            conta["numero_saques"] = numero_saques
            conta["transacoes"] = transacoes
        elif opcao == "e":
            exibir_extrato(conta["saldo"], conta["transacoes"])
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


def depositar(saldo, valor, transacoes):
    if valor > 0:
        saldo += valor
        transacoes.append({"tipo": "d", "valor": valor})
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, transacoes

def sacar(*, saldo, valor, limite, numero_saques, limite_saques, transacoes):
    if valor > saldo:
        print("Operação falhou! Saldo insuficiente.")
        return saldo, False, numero_saques, transacoes
    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, False, numero_saques, transacoes
    if numero_saques >= limite_saques:
        print("Operação falhou! Número máximo de saques diários excedido.")
        return saldo, False, numero_saques, transacoes
    if valor > 0:
        saldo -= valor
        transacoes.append({"tipo": "s", "valor": valor})
        print("Saque realizado com sucesso!")
        numero_saques += 1
        return saldo, True, numero_saques, transacoes
    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, False, numero_saques, transacoes

def exibir_extrato(saldo, transacoes):
    print("\n================ EXTRATO ================")
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for t in transacoes:
            tipo = "Depósito" if t["tipo"] == "d" else "Saque"
            print(f"{tipo}: R$ {t['valor']:.2f}")
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def historico(*, extrato, tipo, valor):
    if tipo == "d":
        extrato += f"Depósito: R$ {valor:.2f}\n"
    elif tipo == "s":
        extrato += f"Saque: R$ {valor:.2f}\n"
    return extrato



#----------------------------------------------------------------------------
def generator(transacoes, tipo=None):
    for transacao in transacoes:
        if tipo is None or transacao["tipo"] == tipo:
            yield transacao

if __name__ == "__main__":

    menu = """
    ======== MENU ========
    [1] Criar usuário
    [2] Criar conta
    [3] Listar contas
    [4] Operar conta
    [5] Contas iterator
    [0] Sair
    =======================
    => """
    usuarios = []
    contas = []
    agencia = "0001"
    numero_conta = 1
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3

    while True:
        opcao = input(menu)

        if opcao == "1":
            criar_usuario(usuarios)

        elif opcao == "2":
            conta = criar_conta(agencia, numero_conta, usuarios)
            if conta:
                contas.append(conta)
                numero_conta += 1

        elif opcao == "3":
            for conta in contas:
                print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")

        elif opcao == "4":
            if not contas:
                print("Nenhuma conta cadastrada. Por favor, crie uma conta primeiro.")
                continue
            print("Selecione a conta para operar:")
            for i, conta in enumerate(contas, start=1):
                print(f"[{i}] Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {conta['usuario']['nome']}")
            conta_selecionada = int(input("Número da conta: ")) - 1
            if 0 <= conta_selecionada < len(contas):
                operar_conta(contas[conta_selecionada], limite, LIMITE_SAQUES)
            else:
                print("Conta inválida. Tente novamente.")
                
        elif opcao == "5":
            contalterador = Contalterador(contas)
            for numero, saldo, nome in contalterador:
                print(f"Conta: {numero} | Saldo: {saldo} | Titular: {nome}")

        elif opcao == "0":
            break

        else:
            print("Opção inválida. Tente novamente.")

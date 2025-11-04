import abc
from datetime import date

class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao:str):
        self._transacoes.append(transacao)

    def obter_transacoes(self):
        return self._transacoes

class Cliente:
    def __init__(self, endereco:str, contas:list=None):
        self._endereco = endereco
        self._contas = contas if contas is not None else []

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class Conta:
    def __init__(self, saldo:float, numero:int, agencia:str, cliente:'Cliente', historico:'Historico'):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    def saldo(self):
        return self._saldo

    def depositar(self, valor:float):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(f"Depósito de R$ {valor:.2f}")
            return True
        else:
            return False
        
    def sacar(self, valor:float):
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            self._historico.adicionar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        else:
            return False
    
class ContaCorrente(Conta):
    def __init__(self, saldo:float, numero:int, agencia:str, cliente:'Cliente', historico:'Historico', limite:float, limite_saques:int=3):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor:float):
        if 0 < valor <= (self._saldo + self._limite):
            self._saldo -= valor
            self._historico.adicionar_transacao(f"Saque de R$ {valor:.2f}")
            return True
        else:
            return False

class PessoaFisica(Cliente):
    def __init__(self, nome:str, cpf:str, data_nascimento: date, endereco:str, contas:list=None):
        super().__init__(endereco, contas)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

class Transacao(abc.ABC):
    def __init__(self, valor:float):
        self._valor = valor

    @abc.abstractmethod
    def registrar(self, conta:'Conta'):
        pass

class Deposito(Transacao):
    def registrar(self, conta:'Conta'):
        if conta.depositar(self._valor):
            conta._historico.adicionar_transacao(f"Depósito de R$ {self._valor:.2f}")
            return True
        else:
            return False

class Saque(Transacao):
    def registrar(self, conta:'Conta'):
        if conta.sacar(self._valor):
            conta._historico.adicionar_transacao(f"Saque de R$ {self._valor:.2f}")
            return True
        else:
            return False

if __name__ == "__main__":
    cliente1 = PessoaFisica("João Silva", "123.456.789-00", date(1990, 5, 20), "Rua A, 123")
    historico1 = Historico()
    conta1 = ContaCorrente(0.0, 1234, "0001", cliente1, historico1, 500.0)
    cliente1.adicionar_conta(conta1)
    deposito1 = Deposito(1000.0)
    saque1 = Saque(200.0)
    cliente1.realizar_transacao(conta1, deposito1)
    cliente1.realizar_transacao(conta1, saque1)
    print(f"Saldo atual: R$ {conta1.saldo():.2f}")
    print("Histórico de transações:")
    for transacao in conta1._historico.obter_transacoes():
        print(transacao)

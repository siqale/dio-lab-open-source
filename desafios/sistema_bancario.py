from datetime import datetime

print("========================= BEM VINDO AO DIO BANC =========================\n")
print("========================= Escolha uma opção abaixo: =====================\n")

menu = """
[a] Abrir Conta
[c] Cadastrar Correntista
[l] Listagem de Correntistas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> """

saldo = 0
extrato = ""
limite = 500
numero_saques = 0
correntistas = {}

def deposito(saldo, /):
    valor = float(input("Informe o valor do depósito: "))
    movimento = ""
    if valor > 0:
        movimento += f"Depósito:            R$ {valor:.2f}\n"
        saldo += valor
        return valor, saldo, movimento
    else:
        print("Operação falhou! O valor informado é inválido.")

def saque(*,saldo_atual, limite, saques):
    valor = float(input("Informe o valor do saque: "))
    movimento = ""
    LIMITE_SAQUES = 3
    saque_maximo = 500
    saldo = saldo_atual
    excedeu_saque_maximo = valor > saque_maximo
    excedeu_saldo = valor > (saldo + limite)
    excedeu_saques = saques >= LIMITE_SAQUES

    if excedeu_saque_maximo:
        valor = -1
        return valor, saldo, saques, f"Operação falhou! Limite máximo por operação de saque é {saque_maximo}."

    elif excedeu_saldo:
        valor = -1
        return valor, saldo, saques, "Operação falhou! Você não tem saldo suficiente."

    elif excedeu_saques:
        valor = -1
        return valor, saldo, saques, "Operação falhou! Número máximo de saques excedido."

    elif valor > 0:
        saques += 1
        saldo -= valor
        movimento += f"Saque:               R$ {valor:.2f}\n"
        print(f"numero de saques restantes: {LIMITE_SAQUES - saques}")
        return valor, saldo, saques, movimento  
    else:
        valor = -1
        return valor, saldo, saques, "Operação falhou! O valor informado é inválido."

def imprimir_extrato(extrato, saldo, /, *, limite):
    total = saldo + limite
    print("\n========================= EXTRATO DIO BANK =========================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:                                               R$ {saldo:.2f}")
    print(f"\nLimite Disponível:                                   R$ {limite:.2f}")
    print(f"\nSaldo Total:                                         R$ {total:.2f}")
    print("=========================== FIM DA MOVIMENTAÇÃO ======================")

def cadastrar_correntista():
    uf_char = 2
    cpf_char = 11
    nome = input("Digite o nome completo do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário (DD/MM/AAAA): ")
    while True:
        if validar_data(data_nascimento):
            print("Data válida!")
            break
        else:
            print("Data inválida. Tente novamente.")
            data_nascimento = input("Digite a data de nascimento do usuário (DD/MM/AAAA): ")
    cpf = input("Digite o CPF do usuário (apenas os números): ")
    while True:
        if cpf.isdigit():
            break
        else:
            cpf = input("Digite apenas os números do cpf: ")
    if len(correntistas) > 0:
        while True:
            if cpf in correntistas or cpf == "":
                print("CPF encontrado!")
                cpf = input("Digite um CPF único: ")
            else:
                break
    logradouro = input("Digite o logradouro do usuário (somente a rua, avenida, etc): ")
    numero = input("Digite o número da casa: ")
    bairro = input("Digite o bairro: ")
    cidade = input("Digite a cidade ; ")
    uf = input("Digite o estado (sigla): ")
    endereco = logradouro+', '+numero+'. '+bairro+' - '+cidade+'/'+uf.upper()
    correntista = {cpf: {"Nome": nome, "Data Nascimento": data_nascimento, "Endereço": endereco}}
    print(f"Correntista Cadastrado com sucesso")
    return correntista   

def listar_correntistas():
    print("===========================  LISTAGEM DE CORRENTISTAS ===========================")
    for cpf in correntistas:
        print("CPF: ", cpf)
        print("Nome: ", correntistas[cpf]["Nome"])
        print("Data de Nascimento: ",correntistas[cpf]["Data Nascimento"])
        print("Endereço: ",correntistas[cpf]["Endereço"])
        print("******************************************************************************\n")
    print("===========================  FIM DA LISTAGEM ====================================")

def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False

while True:
    opcao = input(menu) 
    if opcao == "c":
        print('Opção CADASTRAR CORRENTISTA selecionada\n')
        novo_correntista = cadastrar_correntista()
        for chave, valor in novo_correntista.items():
            if chave not in correntistas:
                correntistas[chave] = valor
    elif opcao == "l":
        print('Opção LISTAR CORRENTISTAS selecionada\n')
        listar_correntistas()
    elif opcao == "d":
        print('Opção DEPÓSITO selecionada\n')
        valor, saldo, movimento = deposito(saldo)
        extrato += movimento
        print(movimento)   
    elif opcao == "s":
        print('Opção SAQUE selecionada\n')
        valor, saldo, numero_saques, movimento = saque(saldo_atual=saldo, limite=limite, saques=numero_saques)
        if valor != -1:
            extrato += movimento
            print(movimento)
            print(f"\nSaques restantes: {3-numero_saques}")  
        else:
            print(movimento)
    elif opcao == "e":
        print('Opção EXTRATO selecionada\n')
        imprimir_extrato(extrato, saldo, limite=limite)

    elif opcao == "q":
        print("=========================  OBRIGADO POR UTILIZAR OS SERVIÇOS DIO BANK  =========================")
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
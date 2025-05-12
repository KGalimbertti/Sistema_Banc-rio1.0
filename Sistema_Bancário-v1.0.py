import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))
#função dedent deixar os espaços alinhados e organizados


def depositar(saldo, valor, extrato, /):
    #tudo que está antecedendo a / significa que os argumentos
    #tem que ser passados por posição
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        #usei o \t para deixar as informações tabuladas
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\nERRO!!! Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    #tudo que colocamos depois do * tem que ser passados por keyword
    #que foram definidas no main
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nERRO!!! Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("\nERRO!!! Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("\nERRO!!! Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        #usei o \t para deixar as informações tabuladas
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===")

    else:
        print("\nERRO!!! Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    #recebemos o valor de saldo de forma possicional
    #recebemos o valor de extrato por keywords
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    # if ternario, onde verifica se o extrato está vazio e caso não esteja, exibi o valor da variavel
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    #exibi todas as operações e depois coloca o valor total do saldo
    #usei o \t para deixar as informações tabuladas
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    #criamos umas lista de usúarios e passamos ele pra função criar usuário
    
    if usuario:
        #usamos a função filtrar usuario, caso encontre o usuario vem a msg que ja existe o cpf cadastrado
        print("\nERRO!!! Já existe usuário com esse CPF!")
        return
    #caso o funcionário não existe, ele vai pedir as informações para cadastro
    #seguindo o padrão informado
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    #preenchendo as informações corretamente o usuario vai ser cadastrado em um dicionário
    #usuarios nesse caso é a lista que está no main
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    #usamos uma compressão de listas, pegamos a lista de usuarios e filtramos se o usuario que estamos percorrendo naquele momento
    #se o cpf dele é igual ao cof que passamos, se for igual ele retorna o cpf se não for a lista fica vazia
    return usuarios_filtrados[0] if usuarios_filtrados else None
    #verificando se usuario filtrados tem algum conteudo, se ele não for uma lista vazia
    #ele retorna o primeiro elemento pq como não podemos cadastrar 2 usuarios com mesmo cpf
    #e se ele não encontrar tem que retornar none

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
   #pedimos o cpf para saber com qual usuario vamos vincular a conta
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
    #se econtrar o usuario ele cria a conta e ja vincula o usuario
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    #agencia e o numero da conta ja vem por argumento e vincula o usuario
    #diferença entre o cria conta e criar usuario é q não passo a lista de contas pra minha função criar conta
    # eu retorno o dicionário que vai ser a representação da conta 
    print("\nERRO!!! Usuário não encontrado, fluxo de criação de conta encerrado!")
    # se não encontrar o usuário vem a mensagem de erro

def listar_contas(contas):
    #recebe o array de contas
    for conta in contas:
    #iteração onde fazemos a formatação da conta
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        #usei o \t para deixar as informações tabuladas
        print("=" * 100)
        print(textwrap.dedent(linha))
        #função dedent deixar os espaços alinhados e organizados


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":           
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            # a conta está sendo armazenada em uma lista
            #numero da agencia vai ser fixo: 0001
            if conta:
            #verificar para não adicioanr contas vazias
                contas.append(conta)
                numero_conta += 1
                #caso a gente implemente uma solição para excluir conta
                #o contador não voltaria e impediria duplicidade
        
        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()

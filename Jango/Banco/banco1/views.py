from django.shortcuts import render
from django.http import HttpResponse
from .models import Conta
#from .models import ContaPoupanca
# Create your views here.

def index(request):
    contas = Conta.objects.all()

    return render(request, "banco1/index.html", {"contas":contas})

def cadastro(request):
    if request.method == "POST":
        conta = request.POST['conta']
        agencia = request.POST['agencia']
        saldo = request.POST['saldo']
        print("Conta: ", conta)
        print("Agencia: ", agencia)
        print("Saldo: ", saldo)
        try:
            c = Conta.objects.get(numero=conta, agencia=agencia)
            return render(request, "banco1/cadastro.html", {"message":"Conta já existente!"})
        except:
            if conta == ' ' or agencia == ' ':
                print("Conta não pode ser vazia")
                return HttpResponse("Campo vazio!")

            else:
                result = Conta.objects.filter(numero=conta)
                print(result)
            c = Conta(numero=conta, agencia=agencia, saldo=saldo)
            c.save()
            contas = Conta.objects.all()
            print("Contas: ", contas)

            return render(request, "banco1/mensagem.html", {"message":"Cadastro efetuado com sucesso!"})

    else:
        return render(request, "banco1/cadastro.html")


def transferencia(request):
    if request.method == "POST":
        contaOrigem = request.POST['conta_origem']
        agenciaOrigem = request.POST['agencia_origem']
        contaDestino = request.POST['conta_destino']
        agenciaDestino = request.POST['agencia_destino']
        valor = float(request.POST['valor'])
        if contaOrigem == contaDestino:
            return HttpResponse("Digite uma conta diferenre!")
        try:
            cOrigem = Conta.objects.get(numero=contaOrigem, agencia=agenciaOrigem)
            print("Conta: ", cOrigem)

        except:
            #return HttpResponse("Erro, conta origem inexistente")
            return render(request, "banco1/transferencia.html", {"message": "Erro, conta origem inexistente"})
        try:
           cDestino = Conta.objects.get(numero=contaDestino, agencia=agenciaDestino)

        except:
            #return HttpResponse("Erro, conta de destino inexistente")
            return render(request, "banco1/transferencia.html", {"message": "Erro, conta destino inexistente"})

        if float(valor) <= cOrigem.get_saldo():
            cOrigem.debito(valor)
            cDestino.credito(valor)
            cOrigem.save()
            cDestino.save()
            print("Origem: ", cOrigem.get_saldo())
            print("Destino: ", cDestino.get_saldo())
            #return HttpResponse(f'Conta de origem:\n Numero da Conta: {cOrigem.numero}\n Agencia: {cOrigem.agencia}\n Conta destino: \n Numero da conta: {cDestino.numero}\n agencia: {cDestino.agencia}\n Valor Transferido: {valor}')
            return render(request, "banco1/mensagem.html", {"message":"Transferencia efetuada com sucesso!"})
        else:
            return render(request, "banco1/transferencia.html", {"message":"Saldo insuficiente!"})

    return render(request, "banco1/transferencia.html")

def poupanca(request):
    if request.method == "POST":
        conta2 = request.POST['conta']
        agencia2 = request.POST['agencia']
        valor2 = float(request.POST['valor'])
        try:

            c = Conta.objects.get(numero=conta2, agencia=agencia2)
            print("Conta: ", c)

        except:

            return render(request, "banco1/poupanca.html", {"message": "Erro, conta inexistente"})

        if valor2 <= c.get_saldo():
            taxa = float(0.01 * 30.0)
            c.guardar(valor2)
            c.render_juros(c.get_cofre(), taxa)
            c.save()

            print("Poupança: ", c.get_cofre())

            return render(request, "banco1/mensagem.html", {"message": "Sucesso"})

        else:

            return render(request, "banco1/poupanca.html", {"message": "Valor maior que seu saldo"})

    else:
        return render(request, "banco1/poupanca.html")



def inicial(request):
    return render(request, "banco1/pagina inicial.html")


def depositar(request):
    if request.method == "POST":
        conta = request.POST['conta']
        agencia = request.POST['agencia']
        valor = float(request.POST['valor'])
        try:
             c = Conta.objects.get(numero=conta, agencia=agencia)
             print("Conta: ", c)

        except:
            return render(request, "banco1/depositar.html", {"message": "Erro, conta inexistente"})

        if valor > 0.0:
            c.credito(valor)
            c.save()
            return render(request, "banco1/mensagem.html", {"message": "Deposito efetuado!"})
        else:
            return render(request, "banco1/depositar.html", {"message": "Valor não inserido"})
    else:
        return render(request, "banco1/depositar.html")

def sacar(request):
    if request.method == "POST":
        conta = request.POST['conta']
        agencia = request.POST['agencia']
        valor = float(request.POST['valor'])
        try:
             c = Conta.objects.get(numero=conta, agencia=agencia)
             print("Conta: ", c)

        except:
            return render(request, "banco1/sacar.html", {"message": "Erro, conta inexistente"})

        if valor <= c.get_saldo():
            c.debito(valor)
            c.save()
            return render(request, "banco1/mensagem.html", {"message": "Saque efetuado com sucesso!"})
        else:
            return render(request, "banco1/sacar.html", {"message": "Saldo insuficiente"})
    else:
        return render(request, "banco1/sacar.html")



def resgatar(request):
    if request.method == "POST":
        conta2 = request.POST['conta']
        agencia2 = request.POST['agencia']
        valor2 = float(request.POST['valor'])
        try:

            c = Conta.objects.get(numero=conta2, agencia=agencia2)
            print("Conta: ", c)

        except:

            return render(request, "banco1/resgatar.html", {"message": "Erro, conta inexistente"})

        if valor2 <= c.get_cofre():
            print("antes de retirar!")
            c.retirada(valor2)
            c.save()
            print("Depois de retirar!")
            c.credito(valor2)
            c.save()

            print("Poupança: ", c.get_cofre())

            return render(request, "banco1/mensagem.html", {"message": "Valor resgatado com Sucesso"})

        else:

            return render(request, "banco1/resgatar.html", {"message": "Valor maior que seu saldo"})

    else:
        return render(request, "banco1/resgatar.html")


def mostrar(request):
    if request.method == "POST":
        conta = request.POST['conta']
        agencia = request.POST['agencia']
        try:
             c = Conta.objects.get(numero=conta, agencia=agencia)
             print("Conta: ", c)
             return render(request, "banco1/saldo.html", {"conta": c})
        except:
            return render(request, "banco1/pegar dados.html", {"message": "Erro, conta inexistente"})

        #saldo(c)

    else:
        return render(request, "banco1/pegar dados.html")

def saldo(request, c):
    return render("banco1/saldo.html", {"contas": c})
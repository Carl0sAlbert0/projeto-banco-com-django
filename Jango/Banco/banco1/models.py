from django.db import models

# Create your models here.

class Conta(models.Model):
    numero = models.CharField("Número da Conta", max_length=255, unique="True")
    agencia = models.CharField("Agência", max_length=10)
    saldo = models.FloatField("Saldo da Conta")
    cofre = models.FloatField("Valor Guardado", default=0.0)

    def __str__(self):
        return "Conta: " + self.numero + "  Agencia: " + self.agencia + "  Saldo: " + str(self.saldo) + "  Poupança: " + str(self.cofre)

    def get_saldo(self):
        return self.saldo

    def get_cofre(self):
        return self.cofre

    def debito(self, valor):
        self.saldo -= valor

    def credito(self, valor):
        self.saldo += valor

    def guardar(self, valor):
        self.cofre += valor



    def render_juros(self, var, taxa):
        #print("Saldo: ", self.get_saldo())
        self.guardar(var *taxa)

        # self.debito(var)
    def retirada(self, valor):
        print("Valor a ser debitado: ", valor)
        self.cofre -= valor


"""class ContaPoupanca(Conta):
    def __int__(self, numero):
        super().__init__(numero)


    def render_juros(self, s, taxa):
        print("valor:", s)
        #s *= float(taxa)
        super().credito(s * taxa)"""




#from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.inicial, name='pagina inicial'),
    path('index/', views.index, name='index'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('transf/', views.transferencia, name='transferencia'),
    path('poupanca/', views.poupanca, name='poupanca'),
    path('depositar/', views.depositar, name='depositar'),
    path('sacar/', views.sacar, name='sacar'),
    path('resgatar/', views.resgatar, name='resgatar'),
    path('pegardados/', views.mostrar, name='pegardados'),
    path('saldo/', views.saldo, name='saldo'),

]
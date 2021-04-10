"""
Feito para testar em desenvolvimento e popular banco de dados
Instruções:
Executar o seguinte comando no terminal ou cmd:
python manage.py runscript zeraDB_cria_admin
Digitar sim para apagar todos os dados e criar superuser ou ENTER para cancelar
"""

import subprocess
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from controle_usuarios.models import Funcionario


def run():
    print(f"\n\t{'*' * 75}")
    print(f"\t{'*'}{' ' * 73}*")
    print("\t* Esse script deleta todos os dados do banco de dados e cria um superuser *")
    print(f"\t{'*'}{' ' * 73}*")
    print(f"\t{'*' * 75}")
    if input("\n***** DELETAR TODOS OS DADOS DO BANCO DE DADOS? *****"
             "\n\nDigite sim para confirmar ou Enter para cancelar: ").lower() == "sim":
        print("\nApagando dados do banco de dados ...")
        subprocess.call(["python manage.py flush --no-input"], shell=True)
        print("\nVerificando se existe alguma alteração no banco de dados ...")
        subprocess.call(["python manage.py makemigrations"], shell=True)
        print("\nAplicando as migrações, se houver ...")
        subprocess.call(["python manage.py migrate"], shell=True)

        print("\nCriando superuser ...")
        user = User.objects.create(username="admin", password=make_password("admin"), is_staff=True, is_active=True,
                                   is_superuser=True)
        Funcionario.objects.create(funcionario=user)
        print("\nConcluído")
        print("\n\nAgora você já pode acessar o sistema com os dados abaixo:"
              "\n\t=======> user=admin <======="
              "\n\t=====> password=admin <=====")
    else:
        exit()

import subprocess
from django.contrib.auth.models import User


def run():
    print("*" * 75)
    print(f"{'*'}{' ' * 73}*")
    print("* Esse script deleta todos os dados do banco de dados e cria um superuser *")
    print(f"{'*'}{' ' * 73}*")
    print("*" * 75)
    if input("\nDeletar os dados do banco de dados?"
             "\nDigite sim para confirmar ou Enter para cancelar: ").lower() == "sim":
        print("\nApagando dados do banco de dados ...")
        subprocess.call(["python manage.py flush --no-input"], shell=True)
        print("\nVerificando se existe alguma alteração no banco de dados ...")
        subprocess.call(["python manage.py makemigrations"], shell=True)
        print("\nAplicando as migrações, se houver ...")
        subprocess.call(["python manage.py migrate"], shell=True)

        print("\nCriando superuser ...\nusername=admin\npassword=admin")
        User.objects.create(username="admin", password="admin", is_staff=True, is_active=True, is_superuser=True)
        print("\nConcluído")
    else:
        exit(0)

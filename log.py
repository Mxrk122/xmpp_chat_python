import cliente
from cliente import Cliente
import asyncio
import delete

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def log_in():
    print("Iniciando sesion")
    # @alumchat.xyz
    jid = input('JID: ')

    # Verificar si el JID ingresado contiene el símbolo "@" que indica la presencia de un dominio
    if "@" not in jid:
        print("No has ingresado un dominio.")
        return
    
    password = input('Password: ')

    # Iniciamos el cliente y se inicia el event handler
    client = Cliente(jid, password)
    client.connect(disable_starttls=True, use_ssl=False)
    client.process(forever=False)

def register():
    print("Registrando nuevo usuario")
    jid = input('JID: ')

    # Verificar si el JID ingresado contiene el símbolo "@" que indica la presencia de un dominio
    if "@" not in jid:
        print("No has ingresado un dominio.")
        return
    
    password = input('Password: ')

    # reallizar el registro
    if Cliente.register(jid, password):
        print("Registro exitoso")
    else:
        print("Registro fallido")

def dev_mode():
    # Modo para no iniciar sesion, huevaaaaaaaaaaaaaaaaaaaaaaaaa
    client = Cliente("oro20857@alumchat.xyz", "Childrenof00")
    client.connect(disable_starttls=True, use_ssl=False)
    client.process(forever=False)

def eliminate():
    print("Iniciando sesion")
    # @alumchat.xyz
    jid = input('JID: ')

    # Verificar si el JID ingresado contiene el símbolo "@" que indica la presencia de un dominio
    if "@" not in jid:
        print("No has ingresado un dominio.")
        return
    
    password = input('Password: ')

    # Funciona igual que el iniciar sesion
    # pero esta vez creamos una instancia de delete account
    client = delete.Del_acc(jid, password)
    client.connect(disable_starttls=True, use_ssl=False)
    client.process(forever=False)
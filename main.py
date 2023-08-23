from log import *
from cliente import Cliente
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# oro20857@alumchat.xyz
# Childrenof00
while True:
    print("\nBienvenido al chat. A continuacion de muestran las opciones sin iniciar sesion")
    print("1 --> Iniciar sesion")
    print("2 --> Registrarse")
    print("3 --> Eliminar cuenta existente")
    print("4 --> Salir")
    print("5 --> Developer Mode")
    opcion = input("Ingresa tu opción: ")
    
    if opcion == "1":
        log_in()
    elif opcion == "2":
        register()
    elif opcion == "3":
        eliminate()
    elif opcion == "4":
        break
    elif opcion == "5":
        print("Modo desarrollador --> ingresar cuenta en el codigo")
        dev_mode()
    else:
        print("Ingresaste algo incorrecto")
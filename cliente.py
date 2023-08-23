#Importar librerias externas
import xmpp
import slixmpp
from slixmpp.exceptions import IqError
from aioconsole import ainput
from aioconsole.stream import aprint
import asyncio
from base64 import *

#   CLASE CLIENTE ======================================================================================================================================================
class Cliente(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        # SEccion generada con chatgpt
        # Registrar plugins necesarios para funcionalidades específicas
        self.register_plugin('xep_0085')   # Mensajes de chat diferido (Message Archiving)
        self.register_plugin('xep_0004')   # Formularios de datos (Data Forms)
        self.register_plugin('xep_0030')   # Información de nodos de servicio (Service Discovery) Chats grupales
        self.register_plugin('xep_0060')   # Publicación-Suscripción (PubSub)
        self.register_plugin('xep_0066')   # Bandeja de entrada fuera de línea (Out of Band Data)
        self.register_plugin('xep_0363')   # Carga de archivos (HTTP File Upload)
        self.register_plugin('xep_0199')   # Ping de mantenimiento de conexión (XMPP Ping)
        self.register_plugin('xep_0045')   # Salas de chat multiusuario (Multi-User Chat)

        # Manejadores de eventos para diferentes situaciones
        self.add_event_handler('session_start', self.log_in)        # Inicio de sesión en la sesión XMPP
        self.add_event_handler('message', self.dm)                  # Manejador de mensajes directos (chat 1 a 1)
        self.add_event_handler('disco_items', self.show_rooms)      # Manejador para mostrar salas de chat disponibles
        self.add_event_handler('groupchat_message', self.rmsg)      # Manejador de mensajes en salas de chat
        self.add_event_handler('presence', self.presence_handler)   # Manejador de eventos de presencia (en línea, fuera de línea, etc.)

        # ambas secciones son necesarias para el funcionamiento del chat

        self.jid = jid
        self.name, self.domain= jid.split('@')
        self.online = False
        self.cc = '' # chat en el que se encuentra
        self.room = '' # sala en la que se encunetra chateando
        self.nikcname = '' # variable para el nickname en un grupo
        self.op = -1 # variable para elegir opciones en el menu
        self.rooms = [] # variable para almacenar las salas de chat disponibles
    
    async def log_in(self, e):
        try:
            # iniciar sesión
            self.send_presence()
            await self.get_roster()

            # indicar que estamos conectados
            self.online = True
            asyncio.create_task(self.main_menu())
        
        except IqError:
            print("Ha habido un error al iniciar sesion")
            self.disconnect()
    
    # Main loop
    async def main_menu(self):
        
        while self.online:
            print("Bienvenido", self.name, "estas en el dominio: ",self.domain)
            print("\nBienvenido al tu sesion de chat")
            print("1 -> Mostrar todos los contactos y su estado")
            print("2 -> Agregar un usuario a los contactos")
            print("3 -> Mostrar destalles de un contacto")
            print("4 -> Charlar con 1 usuario")
            print("5 -> Charlar en grupo")
            print("6 -> Definir mi descripcion")
            print("7 -> Enviar archivos")
            print("8 -> Cerrar sesion")
            self.op = await ainput("\n--> ")

            if self.op == "1":
                await self.get_contacts()

            elif self.op == "2":
                await self.add_user()

            elif self.op == "3":
                await self.get_details()

            elif self.op == "4":
                await self.send_dm()
                
            elif self.op == "5":
                print(" ")
                print("Selecciona el estado que deseas mostrar:")
                print("1 --> Crear una sala")
                print("2 --> Unirse a una sala")
                print("3 --> Mostrar todas las salas disponibles")
                print("4 --> Regresar")
                self.op = await ainput("\nIngresa tu opción: ")

                if self.op == "1":
                    await self.create_room()

                elif self.op == "2":
                    # test test20017@conference.alumchat.xyz
                    await self.join_room()
                    
                elif self.op == "3":
                    await self.get_rooms()
                    
                elif self.op == "4":
                    print("volviendo")
                    pass

            elif self.op == "6":
                await self.new_presence()

            elif self.op == "7":
                await self.send_file()
        
            # Funcion para cerrar sesion ====================================================================================================================================
            elif self.op == "8":
                print("Opción 8 seleccionada: Cerrar sesion")
                self.disconnect()
                self.online = False
            else:
                print("ingresaste algo incorrecto")

            await asyncio.sleep(0.1)  # se espera 0.1 segundos
    
    def register(client, password):
        # Convierte el nombre del cliente en un objeto JID
        jid = xmpp.JID(client)
        
        # Crea un cliente XMPP utilizando el dominio del JID y activa el modo de depuración
        account = xmpp.Client(jid.getDomain(), debug=[])
        
        # Establece una conexión con el servidor XMPP
        account.connect()
        
        # Crea una solicitud de registro proporcionando información de cuenta
        registration_info = {
            'username': jid.getNode(),
            'password': password
        }
        
        # Mandar registro al seridor XMPP
        return bool(xmpp.features.register(account, jid.getDomain(), registration_info))
    
    async def  get_contacts(self):
        # obtener el roster de contactos
        roster = self.client_roster
        # extraemos los contactos
        contacts = roster.keys()

        # obtener informacion de cada contacto
        print("lista de contactos: ")
        for contact in contacts:

            # extraemos el jid del contacto
            jid = contact
            # print(jid)

            # extraer información de cada contacto
            info = roster.presence(jid)
            desc = 'disponible'
            status = ''
            for _, presence in info.items():
                # print(answer)
                print(presence)
                # extraer informacion de presencia del contacto
                # accedemos a la informacion del objeto resultante
                p = presence['show']
                s = presence['status']
                # print("desc: ", p)
                # print(s)
                if p != "":
                    desc = p
                if s != "":
                    status = s
                else:
                    # Si no tiene descrcipcion mostrar un empty
                    status = " --- "

            # mostrar la informacion de cada contacto
            print("JID -- ", jid)
            print("Estado -- ", desc)
            print("Desripcion -- ", status, "\n")
    
    async def add_user(self):
        # Solicitar al usuario ingresar un JID (Identificador de Usuario Jabber)
        new_contact = input("Ingresa el JID: ")

        # Verificar si el JID ingresado contiene el símbolo "@" que indica la presencia de un dominio
        if "@" not in new_contact:
            print("No has ingresado un dominio.")
            return

        try:
            # Enviar una solicitud de amistad al nuevo contacto
            self.send_presence_subscription(pto=new_contact)
            print("Solicitud de amistad enviada.")

            # Actualizar la lista de contactos después de enviar la solicitud
            await self.get_roster()
        except IqError:
            print("Error al enviar la solicitud de suscripción.")


    async def get_details(self):
        # obtener el roster de contactos
        roster = self.client_roster
        # extraemos los contactos
        contacts = list(roster.keys())

        # mostrar los contactos disponibles
        for index, contact in enumerate(contacts):
            print(index, " --> ", contact)
        print(" ")
        try:
            i = int(input("Ingresa el numero de usuario: "))
            # Extraer ell contacto
            user = contacts[i]

            # Obtener presencia del contacto
            # extraer información de cada contacto
            info = roster.presence(user)
            desc = 'disponible'
            status = ''
            for _, presence in info.items():
                # print(answer)
                print(presence)
                # extraer informacion de presencia del contacto
                # accedemos a la informacion del objeto resultante
                p = presence['show']
                s = presence['status']
                # print("desc: ", p)
                # print(s)
                if p != "":
                    desc = p
                if s != "":
                    status = s
                else:
                    # Si no tiene descrcipcion mostrar un empty
                    status = " --- "
            print("JID -- ", user)
            print("Estado -- ", desc)
            print("Desripcion -- ", status, "\n")
        except:
            print("no has ingresado algo valido")

    async def send_dm(self):
        # Obtener el roster de contactos del usuario
        roster = self.client_roster
        # Extraer los nombres de los contactos y convertirlos en una lista
        contacts = list(roster.keys())

        # Mostrar la lista de contactos disponibles junto con sus índices
        for index, contact in enumerate(contacts):
            print(index, " --> ", contact)
        print(" ")

        try:
            # Solicitar al usuario ingresar el número correspondiente al contacto con el que desea chatear
            i = int(input("Ingresa el número de usuario: "))
            
            # Extraer el nombre del contacto seleccionado
            user = contacts[i]
            print("\n ----------------------- CHAT ------------------------------")
            print("Estás chateando con --> ", user)
            
            # Mostrar un mensaje indicando cómo salir del chat
            await aprint('Escribe \\ para salir')
            still = True
            self.cc = user

            # Iniciar el bucle de chat
            while still:
                # Solicitar al usuario que ingrese un mensaje
                message = await ainput('')
                
                # Verificar si el usuario desea salir del chat
                # Utilizare un caracter loco jeje
                if message == '\\':
                    still = False
                    self.cc = ''
                else:
                    # Enviar el mensaje al contacto seleccionado utilizando el tipo de mensaje 'chat'
                    self.send_message(mto=user, mbody=message, mtype='chat')
        except:
            print("Has ingresado algo inválido")
            return

        
    async def dm(self, message):
        # Verificar que el mensaje que llega al usuario es de tipo chat
        if message['type'] == 'chat':
            # Obtener el JID completo del remitente del mensaje
            jid = str(message['from'])
            # Extraer el nombre de usuario del JID (sin el dominio)
            user = jid.split('@')[0]
            
            # Comprobar si el remitente es el mismo que el usuario con el que se está chateando actualmente
            if jid.split("/")[0] == self.cc:

                msg = message["body"]
                # Mostrar el mensaje en la consola
                print(user, ": ", msg)

            else:
                # Mostrar una notificación de que hay un nuevo mensaje
                print(" --> Recibiste un mensaje de ", user, message['body'])

    async def rmsg(self, message=''):

        # obtener el emisor y el mensaje
        user = message['mucnick']
        msg = message["body"]

        # verificar que el usuario forma parte de la sala, sino solo avisar que se recibio un mensaje
        if self.room in str(message['from']):
            print(user, ":", msg)
        else:
            print("Tienes un mensaje en la sala: ", self.room)
    
    async def new_presence(self):
        status = ''
        option = 5
        while(option >= 5):
            print("\nSelecciona tu estado:")
            print("1 --> Disponible")
            print("2 --> Ausente")
            print("3 --> Ocupado")
            print("4 --> No molestar")
            option = int(input(' -- '))
            # DEfinimos los nombres de variables correspondientes al protocolo
            if option == 1:
                status = 'chat'
            elif option == 2:
                status = 'away'
            elif option == 3:
                status = 'xa'
            elif option == 4:
                status = 'dnd'
            else:
                print('Ingresaste algo incorrecto')
            
        print('Escribe tu mensaje de estado: ')
        status_message = input('')
        self.status = status
        self.status_message = status_message
        # envimaos la presencia al server
        self.send_presence(pshow=self.status, pstatus=self.status_message) 
        await self.get_roster()

    # reallizado con ayuda de chaatgpt
    async def presence_handler(self, presence):
        # LAs solicitudfes de amistad se aceptan automaticamente
        if presence['type'] == 'subscribe':
            try:
                # Obtener el usaurio que la envio
                new_friend = str(presence['from'])
                # Enviar una respuesta de suscripción aprobada al remitente
                self.send_presence_subscription(pto=presence['from'], ptype='subscribed')
                # Actualizar el roster después de aceptar la solicitud
                print("Solicitud de: ", new_friend, " aceptada")
                await self.get_roster()
                print()
            except IqError:
                print("Error al recibir la solicitud")

        # Si se recibe una presencia de otro usuario (disponible, no disponible, etc.)
        else:
            if self.online:
                self.presence_notification(presence) 

    def presence_notification(self, presence):

        # Enviar la notificacion si se trata de otro usuario
        if str(presence['from']).split("/")[0] != self.boundjid.bare:
            if "conference" not in str(presence['from']):
                # el usuario que manda la info tiene 3 posibbles estados
                t = presence['type']

                # obtener el usuario
                user = (str(presence['from']).split('/')[0])


                #obtener presencia
                status = presence['status']

                if t != "":
                    msg = user + " is " + t + " --> " + status
                    print(msg) # se muestra la notificacion

    async def create_room(self):
        try:
            n = input("Ingresa el nombre --> ")

            #  construir el nombre del chat
            room = n + "@conference.alumchat.xyz"

            # Unirse a la sala de chat utilizando el plugin xep_0045 (MUC)
            self.plugin['xep_0045'].join_muc(room, self.boundjid.user)

            
            
            # Esperar unos segundos para la conexion
            await asyncio.sleep(3)

            # Generado por chatgpt
            # Configurar los parámetros de la sala de chat
            form = self.plugin['xep_0004'].make_form(ftype='submit', title='Configuracion de sala de chat')
            form['muc#roomconfig_roomname'] = room
            form['muc#roomconfig_roomdesc'] = 'Chat creado'
            form['muc#roomconfig_roomowners'] = [self.boundjid.user]
            form['muc#roomconfig_membersonly'] = '0'
            form['muc#roomconfig_allowinvites'] = '0'
            form['muc#roomconfig_persistentroom'] = '1'
            form['muc#roomconfig_maxusers'] = '100'
            form['muc#roomconfig_publicroom'] = '1'
            form['muc#roomconfig_enablelogging'] = '1'
            form['muc#roomconfig_changesubject'] = '1'
            form['muc#roomconfig_whois'] = 'anyone'

            # Enviar la configuración a la sala de chat utilizando el plugin xep_0045
            await self.plugin['xep_0045'].set_room_config(room, config=form)

            # Enviar un mensaje de confirmación a la sala de chat
            self.send_message(mto=room, mbody="Sala de chat creada", mtype='groupchat')

            print("Sala creada correctamente")
        except IqError:
            print("Error al crear la sala")
    
    # generada con chatgpt
    # basicamente madna a descubrir elementos
    # llos elementos descubiertos se reciben como parametro en la funcion print rooms
    async def get_rooms(self):
        try:
            # obtener lista de salas de chat
            await self['xep_0030'].get_items(jid = "conference.alumchat.xyz")
        except (IqError):
            print("There was an error, please try again later")
    
    # esta es la funcion que recibee lo que solicita la de arriba
    async def show_rooms(self, response):
        # REcibimos las salas disponibles
        # Si el envio fue exitoso obtendremos el resultado
        if response['type'] == 'result':
            print('Rooms disponibles:')
            # revisar los elemntos descubiertos
            for room in response["disco_items"]:
                room_name = room["name"]
                jid = room["jid"]
                print("Sala --> ", room_name)
                print("JID  --> ", jid, "\n")
        self.rooms = response["disco_items"]
                
    async def join_room(self):
        # la metodologia es igual a la del usuario
        # DEbio a la complejidad de obtener las salas de chat, no 
        # sera posible hacer la verificacion como la del usuario
        room = input("Ingresa el JID de la sala: ")
        self.room = room
        self.nikcname = self.boundjid.user

        try:
            # unirse a la sala de chat
            await self.plugin['xep_0045'].join_muc(room, self.nikcname)
        except IqError:
            print("Error al unirse")
        # sala de chat
        await aprint("\n ----------------------- CHAT ------------------------------")
        # Mostrar un mensaje indicando cómo salir del chat
        await aprint('Escribe \\ para salir')
        still = True

        # el chat es un ciclo
        while still:
            # Solicitar al usuario que ingrese un mensaje
            message = await ainput('')
            
            # Verificar si el usuario desea salir del chat
            # Utilizare un caracter loco jeje
            if message == '\\':
                still = False
                self.cc = ''
            else:
                # Enviar el mensaje al contacto seleccionado utilizando el tipo de mensaje 'chat'
                self.send_message(self.room, message, mtype='groupchat')

    # Generado con ayuda de chatgpt
    def exit_room(self):
        self['xep_0045'].leave_muc(self.room, self.nikcname)
        self.room = None
        self.nikcname = None

    async def send_file(self):

        # informacion de envio
        jid = input("Ingresa el JID dele usuario: ")
        path = input("Path del archivo: ")

        # obtenre la extension
        extension = path.split(".")[-1]
        file = open(path, "rb")
        data = file.read()

        # Enviar el meensaje
        data_64 = b64encode(data).decode()
        self.send_message(mto=jid, mbody=f"file://{extension}://{data_64}", mtype="chat")
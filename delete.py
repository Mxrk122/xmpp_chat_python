from cliente import *
import xml.etree.ElementTree as ET

# El proceso de borrar una cuenta dee hacerse en otra clase
# ESto debido a que para borrarlo necesitamos tener la sesion iniciada
# pero no podemos asignar 2 metodos al event handler
class Del_acc(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.start)
        
    async def start(self, event):
        # Enviar una presencia al servidor
        self.send_presence()
        # Obtener el roster (lista de contactos)
        await self.get_roster()
        # Iniciar el proceso de desregistro
        await self.delete()     
        # Desconectar después de completar las operaciones
        self.disconnect()
        
    async def delete(self):
        # Crear una respuesta al servidor
        response = self.Iq(type='set', from_=self.boundjid.user)

        # Crear el elemento XML utilizando ElementTree (ET)
        fragment = ET.Element('query')
        fragment.set('xmlns', 'jabber:iq:register')
        remove_element = ET.SubElement(fragment, 'remove')
        response.append(fragment)

        # Enviar la solicitud de eliminación de cuenta
        try:
            await response.send()
            deleted_user = self.boundjid.jid.split("/")[0]
            print("La cuenta se ha borrado")
        except IqError:
            print("Error al borrar la cuenta")

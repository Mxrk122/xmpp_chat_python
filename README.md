# xmpp_chat_python

# Descripción
El presente repositorio contiene un cliente para un servidor de xmpp.

# Características
- Iniciar sesión
- Registrar cuentas
- Eliminar cuentas
- Mostrar y añadir contactos
- Chat 1 a 1 entre contactos
- Creación de salas de chat
- Participación en salas de chat
- Envio de archivos permitidos

# Instalación
Se necesitan instalar y actualizar las siguientes librerias:
```
pip install xmpppy slixmpp asyncio aiohttp aioconsole
pip install --upgrade xmpppy slixmpp asyncio aiohttp aioconsole
```
# Uso
Se debe correr el archivo main:
```
python main.py
```
El programa incluye un menú para cada opción con el debido manejo de errores y excepciones.
Basta con especificar el número de opción en los inputs del programa.

# Explicación de archivos:
### cliente.py
Se trata del cliente del proyecto. Es el que tiene la mayor parte del código y se encarga de la mayoría de las características del proyecto.
### delete.py
Clase dedicada a la eliminación de cuentas.
### env.txt
Ejemplo de un archivo para enviar
### log.py
Clase dedicada al manejo de funciones al tratar de iniciar sesión.
### main.py
Clase que se encarga de correr el programa.

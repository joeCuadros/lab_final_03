# Documentacion
## Archivo Message.py
### Clase Message
Atributos:
- mensaje_tipo = Donde se guarda que tipo de mensaje se manda
- mensaje = contenido del mensaje
Metodos:
- **to_dict** = retorna en json de la clase message 
- **from_dict** = convierte un json a una clase message 

## Archivo ClientGUI.py
### Clase ChatInterface
Atributos:
- cliente = Contiene la clase cliente
- root = ventana principal
- message_count = contador de mensaje
- max_messages = maxima cantidad de mensaje
- connected = Si esta conectado (True/False)
- username = nombre de usuario

Metodos:
- **setup_styles** = Contiene el estilo de las ventanas
- **create_login_frame** = Crear frame de inicio de sesion
- **create_chat_frame** = Crear frame del chat
- **show_login** = Mostrar pantalla de login y ocultar de chat
- **show_chat** = Mostrar pantalla de chat y ocultar de login
- **connect_to_chat** = Se encargar de validar si el usuario para que se conecte al chat y activa el hilo para recepcionar mensajes
- **exit_chat** = Se encarga de salir del chat al login 
- **send_message** = Se encarga de mandar un mensaje aca se mantiene la logica si mandar un mensaje global o privado
- **_manage_message_history** = Se encarga de eliminar los mensaje de arriba despues de llegar al limite
- **add_sent_message** = Agregar mensaje enviado al chat
- **add_received_message** = Agregar mensaje enviado del chat
- **add_system_message** = Agregar mensaje del sistema
- **add_error_message** = Agregar mensaje de error
- **clear_chat** = Limpiar el área de chat
- **add_user_to_list** = Agregar usuario a la lista de conectados
- **remove_user_from_list** = Agregar usuario a la lista de conectados
- **update_users_list** = Actualizar toda la lista de usuarios
- **exit_chat_error** = Salir del chat por un error
- **run** = Ejecutar la aplicación
- **center_window** = entrar la ventana en la pantalla
- **on_closing** = cerrar todos lo recursos para terminar su ejecucion
### Clase Cliente
Atributos:
- username = Nombre del cliente
- puerto = Puerto para conectarse
- host = Host o ip a donde conectarse
- cliente_socket = crear un cliente socket
- ejecutando = Valor booleano para determinar si se ejecuta
- hilo = Que se usara para la recepcion de datos

Metodos:
- **start** = Retorna (True/False) si se pudo conectar adecuadamente 
- **_mandar_mensajes** = Retorna (True/False) si se puedo mandar mensaje
- **_recibir_mensaje** = Retorna (Message/None) retorna el mensaje
- **procesando_mensajes** = Aca se procesa y recepciona los mensajes recibidas 
- **iniciar_hilo** = Crea un hilo para procesando_mensajes
- **_salir** = Se encarga de liberar los recursos y cerrar el socket

## Archivo ServerGUI.py
### Clase ServerGUI
Atributos:
- cliente = Contiene la clase Server
- root = ventana principal

Metodos:
- **setup_styles** = Contiene el estilo de las ventanas
- **create_interface** = Crear la interfaz principal
- **iniciar_servidor** = Se encarga de iniciar el servidor
- **apagar_servidor** = Se encarga de apagar el servidor
- **mostrar_info_cliente** = Mostrar información del cliente seleccionado
- **mostrar_ventana_info_cliente** = Ventana emergente con información del cliente
- **imprimir_logs** = Método para imprimir logs en la interfaz
- **colocar_cliente** = Método para agregar un cliente a la lista visual
- **eliminar_cliente** = Método para eliminar un cliente de la lista visual
- **actualizar_estadisticas** = Actualizar contador de clientes
- **run** = Ejecutar la aplicación
- **center_window** = Centrar la ventana en la pantalla
- **on_closing** = cerrar todos lo recursos para terminar su ejecucion 

### Clase Server
Atributos:
- puerto = Puerto para conectarse
- clientes = diccionario de clientes
- server_socket = socket del servidor
- hilo = Que se usara para la recepcion de datos

Metodos:
- **start** = Retorna (True/False) si se pudo conectar adecuadamente 
- **stop** = Cierra el socket general
- **esperar_conexion** = Espera la conexion y si se encuentra en un socket lo guarda en ClientThread
- **iniciar_hilo** = Crea un hilo para procesando_mensajes
- **agregar_cliente** = Agregar un cliente
- **eliminar_cliente** = Eliminar un cliente
- **extraer_cliente** = Extraer un cliente para imprimir sus datos
- **mensaje_general** = Se encarga de mandar a todo los clientes excepto el cliente_emisor
- **mensaje_privado** = Se encarga de mandar un mensaje privado al usuario
- **lista_usuarios** = Retorna una copia de los nombres de los clientes

### Clase ClientThread
Atributos:
- client_socket = Socket del cliente 
- direccion = direccion donde recibe y manda mensajes
- server = clase Server
- username = nombre del cliente
- ejecutando = (True/False) Estado de ejecucion
- ingreso = Fecha de ingreso

Metodos:
- **_direccion** = Convierte en string el arreglo de 2 que es direccion
- **_recibir_mensaje** = Retorna (Message/None) retorna el mensaje
- **_mandar_mensajes** = Retorna (True/False) si se puedo mandar mensaje
- **_imprimir_info** = Retorna un texto con la informacion necesaria
- **run** = Aca se encarga de recibir mensajes y procesarlas adecuadamente 


# Posibles mensajes 
## Servidor a Cliente
- Mensaje general = *(**msg**=message,**tipo**=Message.CHAT_GENERAL)*
- Mensaje privado = *(**msg**=[username, message],**tipo**=Message.CHAT_PRIVADO)*
- Mensaje del servidor = *(**msg**=message,**tipo**=Message.SERVER)*
- Mandar lista actual de usuarios = *(**msg**=[username1, username2, etc],**tipo**=Message.ACTUALIZAR_USUARIOS)*
- Salir = *(**msg**=,**tipo**=Message.SALIR)*
- Nuevo usuario = *(**msg**=username,**tipo**=Message.NUEVO_USUARIO)
- Eliminar usuario = *(**msg**=username,**tipo**=Message.ELIMINAR_USUARIO)
- Aceptar el logeo = *(**msg**=,**tipo**=Message.ENTRAR)*


## Cliente a Servidor
- Inicio de sesion = *(**msg**=username,**tipo**=Message.ENTRAR)*
- Mensaje general = *(**msg**=message,**tipo**=Message.CHAT)*
- Mensaje privado = *(**msg**=[username, message],**tipo**=Message.CHAT_PRIVADO)*
- Salir = *(**msg**=,**tipo**=Message.SALIR)*
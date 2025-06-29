ENTRAR = 0                  # msg="<username>"
SALIR = 1                   # msg=""
CHAT = 2                    # msg="<message>"
CHAT_GENERAL = 3            # msg=["<username>","<message>"]
CHAT_PRIVADO = 4            # msg=["<username>","<message>"]
SERVER = 5                  # msg=""
NUEVO_USUARIO = 6           # msg="<username>"
ELIMINAR_USUARIO = 7        # msg="<username>"
ACTUALIZAR_USUARIOS = 8     # msg=["<username1>","<username2>",..]


class Message:

    def __init__(self, mensaje_tipo, mensaje=""):
        self.mensaje_tipo = mensaje_tipo
        self.mensaje = mensaje

    def to_dict(self):
        return {
            'mensaje_tipo': self.mensaje_tipo,
            'mensaje': self.mensaje
        }

    @staticmethod
    def from_dict(data):
        return Message(data['mensaje_tipo'], data['mensaje'])

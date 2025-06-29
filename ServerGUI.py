import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket, threading, json
import Message
from datetime import datetime


def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80)) 
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except:
        return "127.0.0.1" 

class ServerGUI:
    def __init__(self):
        self.server = None
        self.root = tk.Tk()
        self.root.title("Servidor de Chat")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)
        
        # Variables de estado visual
        self.server_running = False
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear la interfaz
        self.create_interface()
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del tema
        style.configure("Custom.TFrame", background="#1e1e2e")
        style.configure("Custom.TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Arial", 10))
        style.configure("Title.TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Arial", 16, "bold"))
        style.configure("Custom.TEntry", fieldbackground="#313244", foreground="#cdd6f4", font=("Arial", 11))
        style.configure("Start.TButton", background="#a6e3a1", foreground="#1e1e2e", font=("Arial", 10, "bold"))
        style.configure("Stop.TButton", background="#f38ba8", foreground="#1e1e2e", font=("Arial", 10, "bold"))
        style.configure("Custom.TLabelframe", background="#1e1e2e", foreground="#cdd6f4")
        style.configure("Custom.TLabelframe.Label", background="#1e1e2e", foreground="#fab387")
        
    def create_interface(self):
        """Crear la interfaz principal"""
        # Header del servidor
        header_frame = ttk.Frame(self.root, style="Custom.TFrame")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Título
        title_label = ttk.Label(
            header_frame,
            text="🖥️ Servidor de Chat",
            style="Title.TLabel"
        )
        title_label.pack(side="left")
        
        # Estado del servidor
        self.status_label = ttk.Label(
            header_frame,
            text="⭕ Servidor Detenido",
            style="Custom.TLabel"
        )
        self.status_label.pack(side="right")
        
        # Frame de configuración
        config_frame = ttk.LabelFrame(
            self.root,
            text="Configuración del Servidor",
            style="Custom.TLabelframe"
        )
        config_frame.pack(fill="x", padx=10, pady=5)
        
        # Configuración interna
        config_inner = ttk.Frame(config_frame, style="Custom.TFrame")
        config_inner.pack(fill="x", padx=10, pady=10)
        
        # Campo Puerto
        ttk.Label(config_inner, text="Puerto:", style="Custom.TLabel").pack(side="left")
        self.port_entry = ttk.Entry(config_inner, style="Custom.TEntry", width=10)
        self.port_entry.pack(side="left", padx=(5, 20))
        self.port_entry.insert(0, "1500")
        
        # Botones de control
        self.start_button = ttk.Button(
            config_inner,
            text="🚀 Iniciar Servidor",
            style="Start.TButton",
            command=self.iniciar_servidor
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ttk.Button(
            config_inner,
            text="🛑 Apagar Servidor",
            style="Stop.TButton",
            command=self.apagar_servidor,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, style="Custom.TFrame")
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame izquierdo - Logs
        left_frame = ttk.LabelFrame(
            main_frame,
            text="Logs del Servidor",
            style="Custom.TLabelframe"
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Área de logs
        self.logs_display = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#313244",
            fg="#cdd6f4",
            font=("Consolas", 9),
            selectbackground="#585b70",
            selectforeground="#cdd6f4"
        )
        self.logs_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame derecho - Clientes conectados
        right_frame = ttk.LabelFrame(
            main_frame,
            text="Clientes Conectados",
            style="Custom.TLabelframe"
        )
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        
        # Lista de clientes
        self.clients_listbox = tk.Listbox(
            right_frame,
            bg="#313244",
            fg="#cdd6f4",
            font=("Arial", 10),
            width=25,
            selectbackground="#585b70",
            selectforeground="#cdd6f4",
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#89b4fa"
        )
        self.clients_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Bind para doble click en cliente
        self.clients_listbox.bind("<Double-Button-1>", self.mostrar_info_cliente)
        
        # Información de estadísticas
        stats_frame = ttk.Frame(right_frame, style="Custom.TFrame")
        stats_frame.pack(fill="x", padx=5, pady=5)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="Clientes: 0",
            style="Custom.TLabel"
        )
        self.stats_label.pack()
        
        # Mensaje inicial
        self.imprimir_logs("Sistema iniciado. Listo para configurar servidor.")
        
   
    def iniciar_servidor(self):
        """Botón iniciar servidor"""
        port = self.port_entry.get()
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número válido entre 1 y 65535")
            return
        
        self.server = Server(port_num, self)
        estado = self.server.start()
        # Fallo la comexion 
        if estado != True:
            messagebox.showerror("Error",f"No se pudo abrir el puerto {port}")
            return
    
        
        # Actualizar interfaz visual
        self.server_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.port_entry.config(state="disabled")
        self.status_label.config(text="🟢 Servidor Activo")
        
        self.imprimir_logs(f"Servidor iniciado en puerto {port}")
        self.server.iniciar_hilo()
        
            
    def apagar_servidor(self):
        """Botón apagar servidor - AQUÍ IMPLEMENTAR LÓGICA"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro que quieres apagar el servidor?"):
            
            self.server.stop()
            
            # Limpiar interfaz visual
            self.clients_listbox.delete(0, tk.END)
            self.server_running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
            self.port_entry.config(state="normal")
            self.status_label.config(text="⭕ Servidor Detenido")
            self.stats_label.config(text="Clientes: 0")
            
            self.imprimir_logs("Servidor detenido")
            
    def mostrar_info_cliente(self, event):
        """Mostrar información del cliente seleccionado - AQUÍ IMPLEMENTAR LÓGICA"""
        selection = self.clients_listbox.curselection()
        if selection:
            cliente_text = self.clients_listbox.get(selection[0])
            # Extraer nombre del cliente (quitar el emoji)
            cliente_nombre = cliente_text.replace("👤 ", "")
            informacion = self.server.extraer_cliente(cliente_nombre)
            if informacion is None:
                return

            self.mostrar_ventana_info_cliente(cliente_nombre, informacion)
            
    def mostrar_ventana_info_cliente(self, nombre_cliente, informacion):
        """Ventana emergente con información del cliente"""
        info_window = tk.Toplevel(self.root)
        info_window.title(f"Información - {nombre_cliente}")
        info_window.geometry("400x300")
        info_window.configure(bg="#1e1e2e")
        info_window.resizable(False, False)
        
        # Centrar ventana
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(info_window, style="Custom.TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(
            main_frame,
            text=f"📋 Información de {nombre_cliente}",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 20))
        
        # Información del cliente
        info_frame = ttk.LabelFrame(
            main_frame,
            text="Detalles del Cliente",
            style="Custom.TLabelframe"
        )
        info_frame.pack(fill="both", expand=True)
        
        # Por ahora datos de ejemplo
        info_text = scrolledtext.ScrolledText(
            info_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#313244",
            fg="#cdd6f4",
            font=("Consolas", 10),
            height=10
        )
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
                       
        info_text.config(state=tk.NORMAL)
        info_text.insert(tk.END, informacion)
        info_text.config(state=tk.DISABLED)
        
        # Botón cerrar
        close_button = ttk.Button(
            main_frame,
            text="Cerrar",
            command=info_window.destroy
        )
        close_button.pack(pady=(10, 0))
        
           
    def imprimir_logs(self, mensaje):
        """Método para imprimir logs en la interfaz"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {mensaje}\n"
        
        self.logs_display.config(state=tk.NORMAL)
        
        # Configurar colores según el tipo de mensaje
        if "Error" in mensaje or "error" in mensaje:
            self.logs_display.tag_configure("error", foreground="#f38ba8")
            self.logs_display.insert(tk.END, log_entry, "error")
        elif "desconectado" in mensaje or "detenido" in mensaje:
            self.logs_display.tag_configure("warning", foreground="#f9e2af")
            self.logs_display.insert(tk.END, log_entry, "warning")
        elif "conectado" in mensaje or "iniciado" in mensaje:
            self.logs_display.tag_configure("success", foreground="#a6e3a1")
            self.logs_display.insert(tk.END, log_entry, "success")
        else:
            self.logs_display.tag_configure("info", foreground="#89b4fa")
            self.logs_display.insert(tk.END, log_entry, "info")
            
        self.logs_display.see(tk.END)
        self.logs_display.config(state=tk.DISABLED)
        
    def colocar_cliente(self, username):
        """Método para agregar un cliente a la lista visual"""
        self.clients_listbox.insert(tk.END, f"👤 {username}")
        self.actualizar_estadisticas()
        self.imprimir_logs(f"Cliente conectado: {username}")
        
    def eliminar_cliente(self, username):
        """Método para eliminar un cliente de la lista visual"""
        items = self.clients_listbox.get(0, tk.END)
        for i, item in enumerate(items):
            if username in item:
                self.clients_listbox.delete(i)
                break
                
        self.actualizar_estadisticas()
        self.imprimir_logs(f"Cliente desconectado: {username}")
            
    def actualizar_estadisticas(self):
        """Actualizar contador de clientes"""
        total_clients = self.clients_listbox.size()
        self.stats_label.config(text=f"Clientes: {total_clients}")
        
    def run(self):
        """Ejecutar la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.center_window()
        self.root.mainloop()
        
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def on_closing(self):
        """Manejar cierre de ventana"""
        if self.server_running:
            if messagebox.askyesno("Confirmar", "¿Estás seguro que quieres cerrar el servidor?"):
                self.server.stop()
                self.root.destroy()
        else:
            self.root.destroy()
#######################################################
class Server:
    def __init__(self, puerto, pantalla):
        self.puerto = puerto
        self.clientes = {}
        self.lock = threading.Lock()
        self.server_socket = None
        self.hilo = None
        self.pantalla = pantalla

    def start(self):
        try:
            self.quedarse = True
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('', self.puerto)) 
            self.server_socket.listen()
            return True
        except Exception as e:
            self.quedarse = False
            return False

    def stop(self):
        self.quedarse = False
        self.mensaje_general("Cerrando la sala",tipo=Message.SALIR)
        self.server_socket.close()
        

    def esperar_conexion(self):
        while self.quedarse:
            try:
                client_socket, direccion = self.server_socket.accept()
                ClientThread(client_socket, direccion, self).start()
            except:
                continue

    def iniciar_hilo(self):
        if self.hilo and self.hilo.is_alive():
            return  # ya esta corriendo
        self.ejecutando = True
        self.hilo = threading.Thread(
            target=self.esperar_conexion,
            args=(),
            name="HiloAceptador",
            daemon=True
        )
        self.hilo.start()            

    # Gestion de clientes
    def agregar_cliente(self, nombre, cliente):
        if not nombre:
            return False # en caso de nombre vacio
        with self.lock:
            if nombre in self.clientes:
                return False # si existe el usuario
            self.clientes[nombre] = cliente
            self.pantalla.colocar_cliente(nombre)
            return True

    def eliminar_cliente(self, nombre):
        if not nombre:
            return False # en caso de nombre vacio
        with self.lock:
            if nombre not in self.clientes:
                return False # si no existe el usuario
            del self.clientes[nombre]
            self.pantalla.eliminar_cliente(nombre)
            return True
           
    def extraer_cliente(self, nombre):
        if not nombre:
            return None # en caso de nombre vacio
        with self.lock:
            if nombre not in self.clientes:
                return None # si no existe el usuario
            return self.clientes[nombre]._imprimir_info()

    def mensaje_general(self,msg, cliente_emisor=None, tipo=Message.CHAT_GENERAL):
        with self.lock:
            for cliente in self.clientes.values():
                if cliente_emisor != cliente:
                    cliente._mandar_mensajes(msg, tipo)

    def mensaje_privado(self,msg, cliente_receptor):
        with self.lock:
            if cliente_receptor in self.clientes:
               self.clientes[cliente_receptor]._mandar_mensajes(msg, Message.CHAT_PRIVADO) 
               return True
            else:
                return False

    def lista_usuarios(self):
        with self.lock:
            return list(self.clientes.keys())


class ClientThread(threading.Thread):
    def __init__(self, client_socket, direccion, server):
        super().__init__()
        self.client_socket = client_socket
        self.direccion = direccion
        self.server = server
        self.username = None
        self.ejecutando = True
        self.ingreso = datetime.now()

    def _direccion(self):
        return f"{self.direccion[0]}:{self.direccion[1]}"

    def _recibir_mensaje(self):
        data = self.client_socket.recv(4096)
        msg_dict = json.loads(data.decode())
        mensaje = Message.Message.from_dict(msg_dict)
        return mensaje
    
    def _mandar_mensajes(self, msg, tipo=Message.CHAT_GENERAL):
        mensaje = Message.Message(tipo, msg)
        try:
            self.client_socket.sendall(json.dumps(mensaje.to_dict()).encode())
        except:
            pass

    def _imprimir_info(self):
        ahora = datetime.now()
        duracion = ahora - self.ingreso
        segundos_totales = int(duracion.total_seconds())
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60
        info_conectado = f"{horas} horas, {minutos} minutos y {segundos} segundos"
        
        return f"""Usuario: {self.username}
IP: {self.direccion[0]}
Puerto: {self.direccion[1]}
Tiempo conectado: {info_conectado}
Estado: Conectado
Hora de conexión: {self.ingreso.strftime("%a %b %d %H:%M:%S")}"""        


    def run(self):
        try:
            mensaje = self._recibir_mensaje()
            self.ejecutando = False
            # esperar el nombre de usuario
            if mensaje.mensaje_tipo == Message.ENTRAR:
                self.ejecutando = self.server.agregar_cliente(
                    nombre=mensaje.mensaje,
                    cliente=self)
                
            else:
                self._mandar_mensajes("Logeo invalido",Message.SERVER)

            # saber si se logeo correctamente con un usuario nuevo
            if self.ejecutando:
                self.server.mensaje_general(mensaje.mensaje, cliente_emisor=self, tipo=Message.NUEVO_USUARIO) #avisar de nuevo usuario
                self.username = mensaje.mensaje
                self._mandar_mensajes("",Message.ENTRAR) #acepto conexion
                self._mandar_mensajes(self.server.lista_usuarios(),Message.ACTUALIZAR_USUARIOS)
            else:
                self._mandar_mensajes("Usuario ya existente",Message.SERVER)

            # esperar mensajes   
            while self.ejecutando:
                mensaje = self._recibir_mensaje()
                # mandar mensajes
                if mensaje.mensaje_tipo == Message.CHAT:
                    self.server.pantalla.imprimir_logs(f"({self.username}): {mensaje.mensaje}")
                    self.server.mensaje_general(msg=[self.username,mensaje.mensaje], cliente_emisor=self)

                elif mensaje.mensaje_tipo == Message.CHAT_PRIVADO:
                    estado = self.server.mensaje_privado(msg=[self.username,mensaje.mensaje[1]], cliente_receptor=mensaje.mensaje[0])
                    if estado == False:
                        self._mandar_mensajes("No se puede mandar un mensaje privado a un usuario desconocido",Message.SERVER)

                elif mensaje.mensaje_tipo == Message.SALIR:
                    self.ejecutando = False

                else:
                    self._mandar_mensajes(
                        msg=f"No esta permitido el mensaje mandado tipo {mensaje.mensaje_tipo}",
                        tipo=Message.SERVER)
            
        except:
            pass
        
        finally:
            if self.username != None:
                self.server.eliminar_cliente(nombre=self.username)
            self.server.mensaje_general(self.username, tipo=Message.ELIMINAR_USUARIO) #avisar de nuevo usuario
            self.client_socket.close()


if __name__ == "__main__":
    app = ServerGUI()
    app.run()
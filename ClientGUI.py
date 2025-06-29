import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import socket, json, threading
import Message

class ChatInterface:
    def __init__(self):
        self.cliente = None
        self.root = tk.Tk()
        self.root.title("Chat Cliente")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(True, True)
        self.message_count = 0
        self.max_messages = 1000

        # Variables de estado
        self.connected = False
        self.username = ""
        
        # Configurar estilos
        self.setup_styles()
        
        # Crear frames principales
        self.create_login_frame()
        self.create_chat_frame()
        
        # Mostrar pantalla de login inicialmente
        self.show_login()
        
    def setup_styles(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores del tema
        style.configure("Custom.TFrame", background="#1e1e2e")
        style.configure("Custom.TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Arial", 10))
        style.configure("Title.TLabel", background="#1e1e2e", foreground="#cdd6f4", font=("Arial", 16, "bold"))
        style.configure("Custom.TEntry", fieldbackground="#313244", foreground="#cdd6f4", font=("Arial", 11))
        style.configure("Connect.TButton", background="#a6e3a1", foreground="#1e1e2e", font=("Arial", 10, "bold"))
        style.configure("Send.TButton", background="#89b4fa", foreground="#1e1e2e", font=("Arial", 10))
        style.configure("Exit.TButton", background="#f38ba8", foreground="#1e1e2e", font=("Arial", 10))
        style.configure("Custom.TLabelframe", background="#1e1e2e", foreground="#cdd6f4")
        style.configure("Custom.TLabelframe.Label", background="#1e1e2e", foreground="#fab387")
        
    def create_login_frame(self):
        """Crear frame de inicio de sesion"""
        self.login_frame = ttk.Frame(self.root, style="Custom.TFrame")
        
        # Container centrado
        container = ttk.Frame(self.login_frame, style="Custom.TFrame")
        container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo/Título
        title_label = ttk.Label(
            container,
            text="💬 Bienvenido al Chat",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 30))
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(
            container,
            text="Configuración de Conexión",
            style="Custom.TLabelframe",
            padding=20
        )
        form_frame.pack(pady=10)
        
        # Campo Usuario
        ttk.Label(form_frame, text="Nombre de usuario:", style="Custom.TLabel").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.username_entry = ttk.Entry(form_frame, style="Custom.TEntry", width=25)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Campo IP
        ttk.Label(form_frame, text="Dirección (IP):", style="Custom.TLabel").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.ip_entry = ttk.Entry(form_frame, style="Custom.TEntry", width=25)
        self.ip_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        self.ip_entry.insert(0, "127.0.0.1")
        
        # Campo Puerto
        ttk.Label(form_frame, text="Puerto:", style="Custom.TLabel").grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.port_entry = ttk.Entry(form_frame, style="Custom.TEntry", width=25)
        self.port_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.port_entry.insert(0, "1500")
        
        # Botón conectar
        self.connect_button = ttk.Button(
            form_frame,
            text="🔗 Conectar al Chat",
            style="Connect.TButton",
            command=self.connect_to_chat
        )
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Bind Enter para conectar
        self.username_entry.bind("<Return>", lambda e: self.connect_to_chat())
        self.ip_entry.bind("<Return>", lambda e: self.connect_to_chat())
        self.port_entry.bind("<Return>", lambda e: self.connect_to_chat())
        
    def create_chat_frame(self):
        """Crear frame del chat"""
        self.chat_frame = ttk.Frame(self.root, style="Custom.TFrame")
        
        # Header del chat
        header_frame = ttk.Frame(self.chat_frame, style="Custom.TFrame")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        # Título con usuario
        self.chat_title = ttk.Label(
            header_frame,
            text="💬 Chat - Conectado como: Usuario",
            style="Title.TLabel"
        )
        self.chat_title.pack(side="left")
        
        # Botón salir
        self.exit_button = ttk.Button(
            header_frame,
            text="Salir del Chat",
            style="Exit.TButton",
            command=self.exit_chat
        )
        self.exit_button.pack(side="right")
        
        # Frame principal del chat
        main_chat_frame = ttk.Frame(self.chat_frame, style="Custom.TFrame")
        main_chat_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame izquierdo - Chat
        left_frame = ttk.LabelFrame(
            main_chat_frame,
            text="Conversación",
            style="Custom.TLabelframe"
        )
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Área de mensajes
        self.chat_display = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#313244",
            fg="#cdd6f4",
            font=("Consolas", 10),
            height=20,
            selectbackground="#585b70",
            selectforeground="#cdd6f4"
        )
        self.chat_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame de entrada de mensaje
        input_frame = ttk.Frame(left_frame, style="Custom.TFrame")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Campo de mensaje
        self.message_entry = ttk.Entry(
            input_frame,
            style="Custom.TEntry",
            font=("Arial", 11)
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.message_entry.bind("<Return>", lambda e: self.send_message())
        
        # Botón enviar
        self.send_button = ttk.Button(
            input_frame,
            text="📤 Enviar",
            style="Send.TButton",
            command=self.send_message
        )
        self.send_button.pack(side="right")
        
        # Frame derecho - Usuarios conectados
        right_frame = ttk.LabelFrame(
            main_chat_frame,
            text="Usuarios Conectados",
            style="Custom.TLabelframe"
        )
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        
        # Lista de usuarios
        self.users_listbox = tk.Listbox(
            right_frame,
            bg="#313244",
            fg="#cdd6f4",
            font=("Arial", 10),
            width=20,
            height=20,
            selectbackground="#585b70",
            selectforeground="#cdd6f4",
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#89b4fa"
        )
        self.users_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        
       
    def show_login(self):
        """Mostrar pantalla de login"""
        self.chat_frame.pack_forget()
        self.login_frame.pack(fill="both", expand=True)
        self.username_entry.focus()
        
    def show_chat(self):
        """Mostrar pantalla de chat"""
        self.login_frame.pack_forget()
        self.chat_frame.pack(fill="both", expand=True)
        self.message_entry.focus()
        
    def connect_to_chat(self):
        """Conectar al chat"""
        username = self.username_entry.get().strip()
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        # Validaciones basicas
        if not username:
            messagebox.showerror("Error", "Debes ingresar un nombre de usuario")
            return
            
        if not ip:
            messagebox.showerror("Error", "Debes ingresar una dirección IP")
            return
            
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número válido entre 1 y 65535")
            return
            
        self.cliente = Cliente(username,port_num,ip)
        estado = self.cliente.start()
        # Fallo la comexion 
        if estado != True:
            messagebox.showerror("Error", estado)
            return
        # mandar nuestro inicio 
        self.cliente._mandar_mensajes(msg=username,tipo=Message.ENTRAR)
        # denegacion por parte del servidor
        estado = self.cliente._recibir_mensaje()
        try:
            if estado.mensaje_tipo != Message.ENTRAR:  
                messagebox.showerror("Error", estado.mensaje)
                return
        except:
            return

        # Aceptado
        self.username = username
        self.connected = True
        
        self.chat_title.config(text=f"💬 Chat - Conectado como: {username}")
        self.add_system_message(f"¡Bienvenido {username}! Te has conectado al servidor {ip}:{port}")
        self.show_chat()

        self.cliente.iniciar_hilo(self) #recepcionando mensajes
        
    def exit_chat(self):
        """Salir del chat"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro que quieres salir del chat?"):
            self.cliente._salir() #salir del socket
            self.connected = False
            self.username = ""
            
            # Limpiar chat
            self.clear_chat()
            
            # Volver a login
            self.show_login()
            
    def send_message(self):
        """Enviar mensaje"""
        message = self.message_entry.get().strip()
        if message:
            message_content = message
            estado = False
            if message.startswith("@") and " " in message:
                message_content = message[1:].split(" ", 1)
                message = f"({message_content[0]}) {message_content[1]}"
                estado = self.cliente._mandar_mensajes(msg=message_content,tipo=Message.CHAT_PRIVADO) #mandar mensaje por socket
            else:
                estado = self.cliente._mandar_mensajes(msg=message_content) #mandar mensaje por socket
            
            if estado:
                self.add_sent_message(message)   # Agregar mensaje enviado   
                self.message_entry.delete(0, tk.END) # Limpiar campo       
            else:
                self.add_error_message(error="no mandado",message=message) 
            
    def _manage_message_history(self):
        self.message_count += 1
        if self.message_count > self.max_messages:
            self.chat_display.config(state=tk.NORMAL)
            lines = self.chat_display.get("1.0", tk.END).split('\n')
            if len(lines) > 100:
                self.chat_display.delete("1.0", f"{min(100, len(lines)//2)}.0")
                self.message_count = self.max_messages - 100
            self.chat_display.config(state=tk.DISABLED)

    def add_sent_message(self, message):
        """Agregar mensaje enviado al chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        
        # Configurar tag para mensaje enviado
        self.chat_display.tag_configure("sent", foreground="#a6e3a1")
        self.chat_display.tag_configure("timestamp", foreground="#9399b2")
        
        # Insertar mensaje
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"🚀 Tú: ", "sent")
        self.chat_display.insert(tk.END, f"{message}\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._manage_message_history()
        
    def add_received_message(self, username, message):
        """Agregar mensaje recibido del chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        
        # Configurar tag para mensaje recibido
        self.chat_display.tag_configure("received", foreground="#89b4fa")
        self.chat_display.tag_configure("timestamp", foreground="#9399b2")
        
        # Insertar mensaje
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"💬 {username}: ", "received")
        self.chat_display.insert(tk.END, f"{message}\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._manage_message_history()
        
    def add_system_message(self, message):
        """Agregar mensaje del sistema"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        
        # Configurar tag para mensaje del sistema
        self.chat_display.tag_configure("system", foreground="#f9e2af")
        self.chat_display.tag_configure("timestamp", foreground="#9399b2")
        
        # Insertar mensaje
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, "🔔 Sistema: ", "system")
        self.chat_display.insert(tk.END, f"{message}\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._manage_message_history()
        
    def add_error_message(self, error, message):
        """Agregar mensaje de error"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.config(state=tk.NORMAL)
        
        # Configurar tag para mensaje de error
        self.chat_display.tag_configure("error", foreground="#f38ba8")
        self.chat_display.tag_configure("timestamp", foreground="#9399b2")
        
        # Insertar mensaje
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"❌ {error}: ", "error")
        self.chat_display.insert(tk.END, f"{message}\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self._manage_message_history()
        
    def clear_chat(self):
        """Limpiar el área de chat"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
    def add_user_to_list(self, username):
        """Agregar usuario a la lista de conectados"""
        if username not in self.users_listbox.get(0, tk.END):
            self.users_listbox.insert(tk.END, f"👤 {username}")
            
    def remove_user_from_list(self, username):
        """Agregar usuario a la lista de conectados"""
        items = self.users_listbox.get(0, tk.END)
        for i, item in enumerate(items):
            if username in item:
                self.users_listbox.delete(i)
                break
                
    def update_users_list(self, users_list):
        """Actualizar toda la lista de usuarios"""
        self.users_listbox.delete(0, tk.END)
        for user in users_list:
            self.users_listbox.insert(tk.END, f"👤 {user}")

    def exit_chat_error(self, message):
        messagebox.showerror("❌ Error",  message)
        self.cliente._salir() #salir del socket
        self.connected = False
        self.username = ""
        # Limpiar chat
        self.clear_chat()
            
        # Volver a login
        self.show_login()        
           
    def run(self):
        """Ejecutar la aplicación"""
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centrar ventana
        self.center_window()
        
        # Iniciar loop principal
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
        if self.connected:
            if messagebox.askyesno("Confirmar", "¿Estás seguro que quieres cerrar la aplicación?"):
                self.cliente._salir() #salir del socket
                self.root.destroy()
        else:
            self.root.destroy()
################################################
class Cliente():
    def __init__(self, username, puerto, host):
        super().__init__()
        self._socket_lock = threading.Lock()
        self.username = username
        self.puerto = puerto
        self.host = host
        self.cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ejecutando = True
        self.hilo = None

    def start(self):
        try:
            self.cliente_socket.connect((self.host, self.puerto))
            return True
        except Exception as e:
            return f"Error al enviar mensaje: {e}"

    # mandar mensaje
    def _mandar_mensajes(self, msg, tipo=Message.CHAT):
        mensaje = Message.Message(tipo, msg)
        try:
            with self._socket_lock:
                self.cliente_socket.sendall(json.dumps(mensaje.to_dict()).encode())
                return True
        except:
            return False
    
    # recibir mensaje
    def _recibir_mensaje(self):
        try:
            data = self.cliente_socket.recv(4096)
            if not data:
                return None
            mensaje_dict = json.loads(data.decode())
            return Message.Message.from_dict(mensaje_dict)
        except:
            return None
        
    # procesar mensajes
    def procesando_mensajes(self, pantalla):
        while self.ejecutando:
            try:
                data = self.cliente_socket.recv(4096)
                if not data:
                    break
                mensaje_dict = json.loads(data.decode())
                mensaje =  Message.Message.from_dict(mensaje_dict)
                if mensaje.mensaje_tipo == Message.CHAT_GENERAL:
                    pantalla.add_received_message(username=f"{mensaje.mensaje[0]}",message=mensaje.mensaje[1])
                elif mensaje.mensaje_tipo == Message.CHAT_PRIVADO:
                    pantalla.add_received_message(username=f"{mensaje.mensaje[0]}**",message=mensaje.mensaje[1]) 
                elif mensaje.mensaje_tipo == Message.SERVER:
                    pantalla.add_system_message(message=mensaje.mensaje)
                elif mensaje.mensaje_tipo == Message.ACTUALIZAR_USUARIOS:
                    pantalla.update_users_list(users_list=mensaje.mensaje)
                elif mensaje.mensaje_tipo == Message.NUEVO_USUARIO:
                    pantalla.add_user_to_list(username=mensaje.mensaje)
                    pantalla.add_system_message(message=f"El usuario '{mensaje.mensaje}' ha entrado a la sala.")
                elif mensaje.mensaje_tipo == Message.ELIMINAR_USUARIO:
                    pantalla.remove_user_from_list(username=mensaje.mensaje)   
                    pantalla.add_system_message(message=f"El usuario '{mensaje.mensaje}' ha salido de la sala.") 
                elif mensaje.mensaje_tipo == Message.SALIR:
                    pantalla.exit_chat_error(message=mensaje.mensaje)
            except:
                continue

    def iniciar_hilo(self, pantalla):
        if self.hilo and self.hilo.is_alive():
            return  # ya esta corriendo
        self.ejecutando = True
        self.hilo = threading.Thread(
            target=self.procesando_mensajes,
            args=(pantalla,),
            name="HiloMensajes",
            daemon=True
        )
        self.hilo.start()
    


    # salir 
    def _salir(self):
        if not self.ejecutando:
            return
        self.ejecutando = False
        try:
            self._mandar_mensajes("", Message.SALIR)
            self.cliente_socket.shutdown(socket.SHUT_RDWR)
        except:
            pass
        finally:
            self.cliente_socket.close()

if __name__ == "__main__":
    # Crear la interfaz
    chat_app = ChatInterface()
    chat_app.run()
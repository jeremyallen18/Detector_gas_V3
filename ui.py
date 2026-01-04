import tkinter as tk
from tkinter import ttk, messagebox
import asyncio
import threading
from ws_client import conectar_ws
from database import obtener_todos_usuarios, registrar_usuario


class GasAlertUI:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("GasAlert D.A.T - Dashboard")
        self.win.geometry("900x750")
        self.win.configure(bg="#0a0e1a")
        self.win.resizable(False, False)

        # Paleta de colores moderna
        self.colors = {
            'bg_primary': '#0a0e1a',
            'bg_secondary': '#151b2e',
            'bg_tertiary': '#1e2842',
            'bg_card': '#1a2332',
            'accent_blue': '#4f86f7',
            'accent_blue_hover': '#3b6dd6',
            'accent_green': '#00d9a3',
            'accent_green_hover': '#00b88a',
            'accent_purple': '#a78bfa',
            'accent_purple_hover': '#8b5cf6',
            'accent_orange': '#ff8c42',
            'text_primary': '#f8fafc',
            'text_secondary': '#94a3b8',
            'text_accent': '#60a5fa',
            'border': '#2d3748',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444'
        }

        # ============================================
        # HEADER CON GRADIENTE VISUAL
        # ============================================
        header = tk.Frame(self.win, bg=self.colors['bg_secondary'], height=120)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Indicador visual superior
        indicator = tk.Frame(header, bg=self.colors['accent_blue'], height=4)
        indicator.pack(fill="x")

        # Contenedor del título con padding
        titulo_container = tk.Frame(header, bg=self.colors['bg_secondary'])
        titulo_container.pack(expand=True, pady=(15, 0))

        # Título principal
        titulo = tk.Label(
            titulo_container, 
            text="⚡ GasAlert D.A.T",
            font=("Segoe UI", 36, "bold"),
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_secondary']
        )
        titulo.pack()

        # Subtítulo con estilo
        subtitulo = tk.Label(
            titulo_container,
            text="Sistema Inteligente de Monitoreo de Gas en Tiempo Real",
            font=("Segoe UI", 12),
            fg=self.colors['text_accent'],
            bg=self.colors['bg_secondary']
        )
        subtitulo.pack(pady=(5, 0))

        # Badge de estado
        status_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        status_frame.pack(pady=(8, 10))
        
        self.status_badge = tk.Label(
            status_frame,
            text="● Sistema Listo",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['success'],
            bg=self.colors['bg_secondary']
        )
        self.status_badge.pack()

        # ============================================
        # CONTENEDOR PRINCIPAL
        # ============================================
        main_container = tk.Frame(self.win, bg=self.colors['bg_primary'])
        main_container.pack(fill="both", expand=True, padx=30, pady=20)

        # ============================================
        # CARD DE CONEXIÓN MEJORADO
        # ============================================
        card_conexion = self._crear_card(main_container, "🌐 CONEXIÓN ESP32")
        card_conexion.pack(fill="x", pady=(0, 20))

        frame_input = tk.Frame(card_conexion, bg=self.colors['bg_card'])
        frame_input.pack(pady=20, padx=25, fill="x")

        # Label con icono
        label_ip = tk.Label(
            frame_input, 
            text="📡 Dirección IP:",
            font=("Segoe UI", 11, "bold"), 
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        )
        label_ip.pack(anchor="w", pady=(0, 10))

        # Frame para input y botón en línea
        input_group = tk.Frame(frame_input, bg=self.colors['bg_card'])
        input_group.pack(fill="x")

        # Input mejorado con borde
        entry_container = tk.Frame(input_group, bg=self.colors['border'], bd=1)
        entry_container.pack(side="left", fill="x", expand=True, padx=(0, 15))

        self.entry_ip = tk.Entry(
            entry_container, 
            font=("Segoe UI", 12), 
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            relief="flat",
            bd=0
        )
        self.entry_ip.pack(padx=2, pady=2, ipady=10, fill="x")
        self.entry_ip.insert(0, "192.168.1.100")

        # Botón de conexión con efecto hover
        self.btn_conectar = self._crear_boton(
            input_group,
            text="CONECTAR",
            bg=self.colors['accent_blue'],
            hover_bg=self.colors['accent_blue_hover'],
            command=self.iniciar_conexion,
            width=18
        )
        self.btn_conectar.pack(side="left")

        # ============================================
        # PANEL DE ACCIONES CON GRID
        # ============================================
        acciones_card = self._crear_card(main_container, "⚙️ PANEL DE CONTROL")
        acciones_card.pack(fill="x", pady=(0, 20))

        botones_container = tk.Frame(acciones_card, bg=self.colors['bg_card'])
        botones_container.pack(pady=20, padx=25, fill="x")

        # Grid de botones
        btn_frame_left = tk.Frame(botones_container, bg=self.colors['bg_card'])
        btn_frame_left.pack(side="left", fill="x", expand=True)

        btn_registrar = self._crear_boton_accion(
            btn_frame_left,
            text="👤 REGISTRAR USUARIO",
            bg=self.colors['accent_green'],
            hover_bg=self.colors['accent_green_hover'],
            command=self.abrir_registro_usuario
        )
        btn_registrar.pack(side="left", padx=(0, 10))

        btn_users = self._crear_boton_accion(
            btn_frame_left,
            text="📋 VER USUARIOS",
            bg=self.colors['accent_purple'],
            hover_bg=self.colors['accent_purple_hover'],
            command=self.abrir_lista_usuarios
        )
        btn_users.pack(side="left")

        # ============================================
        # MONITOR DE EVENTOS MEJORADO
        # ============================================
        monitor_card = self._crear_card(main_container, "📊 MONITOR DE EVENTOS EN TIEMPO REAL")
        monitor_card.pack(fill="both", expand=True)

        # Contenedor del monitor
        monitor_container = tk.Frame(monitor_card, bg=self.colors['bg_card'])
        monitor_container.pack(pady=20, padx=25, fill="both", expand=True)

        # Textbox con diseño de terminal
        text_container = tk.Frame(monitor_container, bg=self.colors['border'], bd=1)
        text_container.pack(fill="both", expand=True)

        self.textbox = tk.Text(
            text_container, 
            height=8,
            bg='#0d1117', 
            fg=self.colors['success'],
            font=("Consolas", 11),
            insertbackground=self.colors['accent_blue'],
            relief="flat",
            bd=0,
            wrap="word",
            padx=15,
            pady=15
        )
        self.textbox.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Mensaje inicial
        self.textbox.insert(tk.END, "💡 Sistema iniciado. Esperando conexión...\n")
        self.textbox.config(state="disabled")

        # ============================================
        # FOOTER MEJORADO
        # ============================================
        footer = tk.Frame(self.win, bg=self.colors['bg_secondary'], height=50)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)

        footer_label = tk.Label(
            footer,
            text="© 2024 GasAlert D.A.T | Sistema de Detección Avanzada | Todos los derechos reservados",
            font=("Segoe UI", 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        footer_label.pack(expand=True)

    def _crear_card(self, parent, titulo):
        """Crea un card estilizado con header"""
        card = tk.Frame(parent, bg=self.colors['bg_card'], bd=0)
        
        # Header del card
        header = tk.Frame(card, bg=self.colors['bg_tertiary'], height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(
            header, 
            text=titulo,
            font=("Segoe UI", 13, "bold"), 
            fg=self.colors['text_primary'],
            bg=self.colors['bg_tertiary']
        ).pack(side="left", pady=12, padx=25)
        
        return card

    def _crear_boton(self, parent, text, bg, hover_bg, command, width=15):
        """Crea un botón estilizado con efecto hover"""
        btn = tk.Button(
            parent, 
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=bg, 
            fg="white",
            activebackground=hover_bg,
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            bd=0,
            width=width,
            pady=12,
            command=command
        )
        
        # Efectos hover
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn

    def _crear_boton_accion(self, parent, text, bg, hover_bg, command):
        """Crea un botón de acción grande"""
        btn = tk.Button(
            parent, 
            text=text,
            bg=bg, 
            fg="white",
            font=("Segoe UI", 11, "bold"),
            activebackground=hover_bg,
            activeforeground="white",
            cursor="hand2",
            relief="flat",
            bd=0,
            padx=30,
            pady=15,
            command=command
        )
        
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        
        return btn

    def iniciar_conexion(self):
        ip = self.entry_ip.get().strip()

        if not ip:
            messagebox.showwarning("Advertencia", "Por favor ingresa la IP del ESP32.")
            return

        self._log_message(f"🔄 Conectando a {ip}...", "info")
        self.status_badge.config(text="● Conectando...", fg=self.colors['warning'])

        threading.Thread(
            target=lambda: asyncio.run(conectar_ws(ip, self.recibir_log)),
            daemon=True
        ).start()

    def recibir_log(self, texto):
        self.win.after(0, self._actualizar_log, texto)
    
    def _actualizar_log(self, texto):
        self.textbox.config(state="normal")
        self.textbox.delete('1.0', tk.END)
        self.textbox.insert('1.0', f"📡 {texto.strip()}")
        self.textbox.config(state="disabled")
        self.status_badge.config(text="● Conectado", fg=self.colors['success'])

    def _log_message(self, mensaje, tipo="info"):
        """Agrega mensaje al log con formato"""
        self.textbox.config(state="normal")
        self.textbox.insert(tk.END, f"{mensaje}\n")
        self.textbox.see(tk.END)
        self.textbox.config(state="disabled")

    def abrir_registro_usuario(self):
        win_reg = tk.Toplevel(self.win)
        win_reg.title("Registrar Usuario")
        win_reg.geometry("550x350")
        win_reg.configure(bg=self.colors['bg_primary'])
        win_reg.resizable(False, False)
        win_reg.grab_set()
        win_reg.transient(self.win)

        # Header con estilo
        header_reg = tk.Frame(win_reg, bg=self.colors['bg_secondary'], height=90)
        header_reg.pack(fill="x")
        header_reg.pack_propagate(False)

        tk.Label(
            header_reg, 
            text="👤 Registrar Nuevo Usuario",
            font=("Segoe UI", 22, "bold"),
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_secondary']
        ).pack(expand=True)

        # Formulario con card
        form_card = tk.Frame(win_reg, bg=self.colors['bg_card'])
        form_card.pack(pady=25, padx=40, fill="both", expand=True)

        tk.Label(
            form_card, 
            text="📧 Correo Electrónico",
            font=("Segoe UI", 12, "bold"), 
            fg=self.colors['text_primary'],
            bg=self.colors['bg_card']
        ).pack(pady=(20, 10), anchor="w", padx=20)

        # Input con borde
        entry_container = tk.Frame(form_card, bg=self.colors['border'], bd=1)
        entry_container.pack(fill="x", padx=20)

        entry_correo = tk.Entry(
            entry_container, 
            font=("Segoe UI", 13),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            relief="flat",
            bd=0
        )
        entry_correo.pack(padx=2, pady=2, ipady=12, fill="x")
        entry_correo.focus()

        def guardar_usuario():
            correo = entry_correo.get().strip()
            
            if not correo:
                messagebox.showwarning("Campo Vacío", "Por favor ingresa un correo electrónico.")
                return
            
            if "@" not in correo or "." not in correo:
                messagebox.showwarning("Formato Inválido", "Ingresa un correo electrónico válido.")
                return

            try:
                registrar_usuario(correo)
                messagebox.showinfo("✅ Éxito", f"Usuario '{correo}' registrado correctamente.")
                self._log_message(f"✅ Usuario registrado: {correo}", "success")
                win_reg.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo registrar el usuario:\n{e}")

        btn_guardar = self._crear_boton(
            form_card,
            text="✓ GUARDAR USUARIO",
            bg=self.colors['accent_green'],
            hover_bg=self.colors['accent_green_hover'],
            command=guardar_usuario,
            width=25
        )
        btn_guardar.pack(pady=30)

        entry_correo.bind("<Return>", lambda e: guardar_usuario())

    def abrir_lista_usuarios(self):
        win_u = tk.Toplevel(self.win)
        win_u.title("Usuarios Registrados")
        win_u.geometry("800x600")
        win_u.configure(bg=self.colors['bg_primary'])
        win_u.resizable(False, False)

        # Header
        header_users = tk.Frame(win_u, bg=self.colors['bg_secondary'], height=90)
        header_users.pack(fill="x")
        header_users.pack_propagate(False)

        tk.Label(
            header_users, 
            text="📋 Usuarios Registrados",
            font=("Segoe UI", 24, "bold"),
            fg=self.colors['text_primary'], 
            bg=self.colors['bg_secondary']
        ).pack(expand=True)

        # Card contenedor
        tabla_card = tk.Frame(win_u, bg=self.colors['bg_card'])
        tabla_card.pack(pady=25, padx=30, fill="both", expand=True)

        # Estilos Treeview mejorados
        estilo = ttk.Style()
        estilo.theme_use("default")

        estilo.configure(
            "Custom.Treeview",
            background=self.colors['bg_tertiary'],
            foreground=self.colors['text_primary'],
            fieldbackground=self.colors['bg_tertiary'],
            rowheight=40,
            font=("Segoe UI", 11),
            borderwidth=0
        )

        estilo.configure(
            "Custom.Treeview.Heading",
            background=self.colors['bg_secondary'],
            foreground=self.colors['text_primary'],
            font=("Segoe UI", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )

        estilo.map("Custom.Treeview",
            background=[("selected", self.colors['accent_blue'])],
            foreground=[("selected", "white")]
        )

        tabla_container = tk.Frame(tabla_card, bg=self.colors['border'], bd=1)
        tabla_container.pack(pady=20, padx=20, fill="both", expand=True)

        columnas = ("correo", "enviados")
        tabla = ttk.Treeview(
            tabla_container, 
            columns=columnas, 
            show="headings", 
            height=12,
            style="Custom.Treeview"
        )

        tabla.heading("correo", text="📧 CORREO ELECTRÓNICO")
        tabla.heading("enviados", text="📨 CORREOS ENVIADOS")

        tabla.column("correo", width=500)
        tabla.column("enviados", width=230, anchor="center")

        scrollbar = ttk.Scrollbar(tabla_container, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        tabla.pack(side="left", fill="both", expand=True, padx=2, pady=2)
        scrollbar.pack(side="right", fill="y")

        try:
            usuarios = obtener_todos_usuarios()

            if not usuarios:
                tk.Label(
                    tabla_card,
                    text="📭 No hay usuarios registrados",
                    font=("Segoe UI", 13),
                    fg=self.colors['text_secondary'],
                    bg=self.colors['bg_card']
                ).pack(pady=15)
            else:
                for u in usuarios:
                    correo = u.get("correo", "")
                    enviados = u.get("enviados", 0)
                    tabla.insert("", tk.END, values=(correo, enviados))

                # Estadística
                total_label = tk.Label(
                    tabla_card,
                    text=f"👥 Total de usuarios: {len(usuarios)}",
                    font=("Segoe UI", 12, "bold"),
                    fg=self.colors['accent_blue'],
                    bg=self.colors['bg_card']
                )
                total_label.pack(pady=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los usuarios:\n{e}")

        # Botón actualizar
        btn_actualizar = self._crear_boton(
            win_u,
            text="🔄 ACTUALIZAR",
            bg=self.colors['accent_purple'],
            hover_bg=self.colors['accent_purple_hover'],
            command=lambda: [win_u.destroy(), self.abrir_lista_usuarios()],
            width=20
        )
        btn_actualizar.pack(pady=20)

    def run(self):
        self.win.mainloop()
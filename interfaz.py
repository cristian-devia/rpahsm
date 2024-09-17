# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app_manager import AppManager

class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Automatización de Mensajes HSM")

        self.app_manager = AppManager()

        self.entries_parametros = []

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", padding=6)
        style.configure("TButton", padding=6)

        frame = tk.Frame(self.root, padx=10, pady=10, bg="#f0f0f0")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)

        ttk.Label(frame, text="Usuario", background="#f0f0f0").grid(row=0, column=0, sticky="e")
        self.entry_usuario = ttk.Entry(frame)
        self.entry_usuario.grid(row=0, column=1, sticky="we")

        ttk.Label(frame, text="Contraseña", background="#f0f0f0").grid(row=1, column=0, sticky="e")
        self.entry_password = ttk.Entry(frame, show="*")
        self.entry_password.grid(row=1, column=1, sticky="we")

        ttk.Label(frame, text="Selecciona la campaña", background="#f0f0f0").grid(row=2, column=0, sticky="e")
        self.combo_campania = ttk.Combobox(frame, values=[
            "COMFANDI", "Americas business process service", "Derco ABPS", "Cafam", "Cruz Roja ABPS", "MederilPS",
            "BienestarIPS", "Cafam", "anmv", "Americas Demos", "ICETEX", "MinEducacion",
            "Departamento para la Prosperidad Social DPS", "Autoridad Nacional de Licencias Ambientales", "ETB",
            "Comfandi", "Servicio Occidental de Salud EPS", "test", 
            "UNIDAD ADMINISTRATIVA ESPECIAL DE GESTIÓN PENSIONAL Y CONTRIBUCIONES PARAFISCALES DE LA PROTECCIÓN SOCIAL - UGPP",
            "HPE Hewlett Packard Enterprise", "HPE Contacto Latinoamérica", "Ecopetrol", "CITAS CAFAM BPS", "Chilco",
            "Equida Seguros", "Nueva EPS", "CARVAJAL TECNOLOGÍA Y SERVICIOS T&S", "Thomas Greg", "POSITIVA",
            "Derco ABPS", "Credivalores", "Credifinanciera", "QNT", "WOM Colombia", "Banco de Occidente ABPS",
            "Proceraseo ABPS", "Transformación Digital ABPS", "Banco de Bogotá ABPS", "CallBot Credibanco",
            "Famisanar ABPS"    
        ], state="readonly")
        self.combo_campania.grid(row=2, column=1, sticky="we")

        ttk.Label(frame, text="Ingresa el nombre del HSM", background="#f0f0f0").grid(row=3, column=0, sticky="e")
        self.entry_hsm = ttk.Entry(frame)
        self.entry_hsm.grid(row=3, column=1, sticky="we")

        ttk.Label(frame, text="Es HSM?", background="#f0f0f0").grid(row=4, column=0, sticky="e")
        self.combo_es_hsm = ttk.Combobox(frame, values=["Si", "No"], state="readonly")
        self.combo_es_hsm.grid(row=4, column=1, sticky="we")

        ttk.Label(frame, text="Administrado por Cari?", background="#f0f0f0").grid(row=5, column=0, sticky="e")
        self.combo_administrado_por_cari = ttk.Combobox(frame, values=["Si", "No"], state="readonly")
        self.combo_administrado_por_cari.grid(row=5, column=1, sticky="we")

        ttk.Label(frame, text="Esperar entrada?", background="#f0f0f0").grid(row=6, column=0, sticky="e")
        self.combo_esperar_entrada = ttk.Combobox(frame, values=["Si", "No"], state="readonly")
        self.combo_esperar_entrada.grid(row=6, column=1, sticky="we")

        ttk.Label(frame, text="¿Este mensaje tiene parámetros?", background="#f0f0f0").grid(row=7, column=0, sticky="e")
        self.combo_parametros = ttk.Combobox(frame, values=["Si", "No"], state="readonly")
        self.combo_parametros.grid(row=7, column=1, sticky="we")

        # Crear los widgets para parámetros y ocultarlos inicialmente
        self.param_frame = tk.Frame(frame, bg="#f0f0f0")
        self.param_frame.grid(row=9, column=0, columnspan=2, sticky="we")

        ttk.Label(self.param_frame, text="Seleccione la cantidad de parámetros", background="#f0f0f0").grid(row=0, column=0, sticky="e")
        self.combo_cantidad_parametros = ttk.Combobox(self.param_frame, values=list(range(1, 11)), state="readonly")
        self.combo_cantidad_parametros.grid(row=0, column=1, sticky="we")

        # Contenedor para los parámetros
        self.parametros_container = tk.Frame(self.param_frame, bg="#f0f0f0")
        self.parametros_container.grid(row=1, column=0, columnspan=2, sticky="we")

        self.label_instrucciones = ttk.Label(frame, text="La forma correcta de utilizar los parámetros en el mensaje es la siguiente: [0], [1], etc. Por ejemplo, 'Hola [0], esto es una prueba.'", background="#f0f0f0")
        self.label_instrucciones.grid(row=8, column=0, columnspan=2, sticky="we")
        self.label_instrucciones.grid_remove()

        self.combo_parametros.bind("<<ComboboxSelected>>", self.actualizar_parametros)
        self.combo_cantidad_parametros.bind("<<ComboboxSelected>>", self.mostrar_campos_parametros)

        ttk.Label(frame, text="Ingresar mensaje", background="#f0f0f0").grid(row=10, column=0, sticky="e")
        self.text_mensaje = tk.Text(frame, height=10, width=50)
        self.text_mensaje.grid(row=10, column=1, sticky="we")

        button_style = ttk.Style()
        button_style.configure("Salto.TButton", background="#1E90FF", foreground="white", font=("Helvetica", 10, "bold"))
        button_style.configure("Ejecutar.TButton", background="#000000", foreground="white", font=("Helvetica", 10, "bold"))

        salto_button = ttk.Button(frame, text="Salto de Línea", command=lambda: self.insertar_salto_linea(self.text_mensaje), style="Salto.TButton")
        salto_button.grid(row=11, column=1, sticky="we", padx=10, pady=5)

        ejecutar_button = ttk.Button(frame, text="EJECUTAR", command=self.validar_y_ejecutar, style="Ejecutar.TButton")
        ejecutar_button.grid(row=12, column=0, columnspan=2, pady=10, sticky="we")

    def actualizar_parametros(self, event):
        if self.combo_parametros.get() == "Si":
            self.param_frame.grid()
            self.combo_cantidad_parametros.grid()
            self.label_instrucciones.grid(row=8, column=0, columnspan=2, sticky="we")
        else:
            self.param_frame.grid_remove()
            self.label_instrucciones.grid_remove()

    def mostrar_campos_parametros(self, event):
        for widget in self.parametros_container.winfo_children():
            widget.destroy()
        self.entries_parametros.clear()

        num_params = int(self.combo_cantidad_parametros.get())
        for i in range(num_params):
            ttk.Label(self.parametros_container, text=f"Parámetro {i+1}").grid(row=i, column=0, sticky="e")
            entry_param = ttk.Entry(self.parametros_container)
            entry_param.grid(row=i, column=1, sticky="we")
            self.entries_parametros.append(entry_param)

    def insertar_salto_linea(self, text_widget):
        text_widget.insert(tk.INSERT, "\\n")

    def validar_y_ejecutar(self):
        username = self.entry_usuario.get()
        password = self.entry_password.get()
        campaign = self.combo_campania.get()
        hsm_name = self.entry_hsm.get()
        is_hsm = self.combo_es_hsm.get() == "Si"
        is_auto_managed = self.combo_administrado_por_cari.get() == "Si"
        awaiting_input = self.combo_esperar_entrada.get() == "Si"
        has_parameters = self.combo_parametros.get() == "Si"
        entries_parametros = self.entries_parametros
        params_count = len(entries_parametros)
        message = self.text_mensaje.get("1.0", tk.END).strip()  # Eliminar espacios en blanco y líneas innecesarias

        # Validar saltos de línea en el mensaje
        if "\\n" not in message and "\n" not in message:
            messagebox.showerror("Error", "Te faltan los saltos de línea para tu mensaje")
            return

        # Convertir las entradas de parámetros a una lista de texto
        parametros = [entry.get() for entry in entries_parametros]

        # Ejecutar la automatización si la validación es exitosa
        self.app_manager.ejecutar_automatizacion(username, password, campaign, hsm_name, params_count, message, parametros, is_hsm, is_auto_managed, awaiting_input)

# Crear la ventana principal
root = tk.Tk()
app = Interfaz(root)
root.mainloop()

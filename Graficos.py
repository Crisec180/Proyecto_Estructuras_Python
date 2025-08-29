import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
clases_base_path = os.path.join(current_dir, "Clases_Base")
sys.path.append(clases_base_path)
estructuras_path = os.path.join(current_dir, "Estructuras")
sys.path.append(estructuras_path)
Proyecto_Estructuras_Python_path= os.path.join(current_dir,"Proyecto_Estructuras_Python")
sys.path.append(Proyecto_Estructuras_Python_path)
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk
from Clases_Base.Cliente import Cliente
from Estructuras.GestionClientes import GestionClientes
from Estructuras.Carrodecompra import CarroDeCompra
from Estructuras.inventario import PilaArticulos, ListaInventario, Nodo
from Clases_Base.articulo import Articulo
from Procesar_Pago import ProcesarPago
from Estructuras.GestionTarjetas import GestionTarjetas
from Estructuras.GestionClientes import GestionClientes
class SistemaCompraModerno:
    def __init__(self):
        
        ctk.set_appearance_mode("light")  
        ctk.set_default_color_theme("blue")  
        self.root = ctk.CTk()
        self.root.title("🛒 Sistema de Compra Profesional")
        self.root.geometry("1200x800")
        self.centrar_ventana()
        self.usuario_actual = None
        self.carrito = None
        self.inventario = ListaInventario()
        self.gestion_clientes = GestionClientes("clientes.csv")
        self.gestion_tarjetas = GestionTarjetas("tarjetas.csv",self.gestion_clientes)
        self.inicializar_inventario()
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True)
        
        self.crear_interfaz_principal()
        
    def centrar_ventana(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        ancho = 1200
        alto = 800
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def crear_interfaz_principal(self):
        """Crear la interfaz principal del sistema"""
        
        
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        self.crear_sidebar()
       
        self.crear_area_contenido()
        
        self.mostrar_bienvenida()
    
    def crear_sidebar(self):
        """Crear el menú lateral"""
        self.sidebar = ctk.CTkFrame(self.main_container, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(
            self.sidebar, 
            text="🛒 Sistema Compra", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        botones_menu = [
            ("🏠 Inicio", self.mostrar_bienvenida),
            ("👤 Gestión Clientes", self.mostrar_gestion_clientes),
            ("📦 Inventario", self.mostrar_inventario),
            ("🛍️ Nueva Compra", self.mostrar_nueva_compra),
            ("💳 Gestión Tarjetas", self.mostrar_gestion_tarjetas),
            ("📊 Reportes", self.mostrar_reportes),
            ("⚙️ Configuración", self.mostrar_configuracion)
        ]
        
        self.botones_menu = []
        for i, (texto, comando) in enumerate(botones_menu, 1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=texto,
                command=comando,
                height=40,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
            self.botones_menu.append(btn)
        
        self.btn_salir = ctk.CTkButton(
            self.sidebar,
            text="🚪 Salir",
            command=self.salir_aplicacion,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("gray75", "gray25"),
            hover_color=("gray65", "gray35")
        )
        self.btn_salir.grid(row=10, column=0, padx=20, pady=(20, 20), sticky="ew")
    
    def crear_area_contenido(self):
        """Crear el área principal de contenido"""
        self.content_frame = ctk.CTkFrame(self.main_container)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def limpiar_contenido(self):
        """Limpiar el área de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def mostrar_bienvenida(self):
        """Mostrar pantalla de bienvenida"""
        self.limpiar_contenido()
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        title_label = ctk.CTkLabel(
            welcome_frame,
            text="¡Bienvenido al Sistema de Compra!",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=50)
        subtitle_label = ctk.CTkLabel(
            welcome_frame,
            text="Gestiona clientes, inventario y procesa pagos de manera eficiente",
            font=ctk.CTkFont(size=16)
        )
        subtitle_label.pack(pady=10)
        
       
        stats_frame = ctk.CTkFrame(welcome_frame)
        stats_frame.pack(pady=40, padx=40, fill="x")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.crear_stat_card(stats_frame, "👥", "Clientes", "0", 0, 0)
        self.crear_stat_card(stats_frame, "📦", "Productos", "0", 0, 1)
        self.crear_stat_card(stats_frame, "💰", "Ventas Hoy", "$0", 0, 2)
        quick_access_frame = ctk.CTkFrame(welcome_frame)
        quick_access_frame.pack(pady=20, padx=40, fill="x")
        
        quick_label = ctk.CTkLabel(
            quick_access_frame,
            text="Accesos Rápidos",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        quick_label.pack(pady=10)
        quick_buttons_frame = ctk.CTkFrame(quick_access_frame)
        quick_buttons_frame.pack(pady=10, padx=20, fill="x")
        quick_buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        btns_rapidos = [
            ("🛍️ Nueva Venta", self.mostrar_nueva_compra),
            ("👤 Nuevo Cliente", self.mostrar_gestion_clientes),
            ("📦 Ver Inventario", self.mostrar_inventario)
        ]
        
        for i, (texto, comando) in enumerate(btns_rapidos):
            btn = ctk.CTkButton(
                quick_buttons_frame,
                text=texto,
                command=comando,
                height=50,
                font=ctk.CTkFont(size=14, weight="bold")
            )
            btn.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
    
    def crear_stat_card(self, parent, icono, titulo, valor, row, col):
        """Crear una tarjeta de estadística"""
        card = ctk.CTkFrame(parent)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        icon_label = ctk.CTkLabel(card, text=icono, font=ctk.CTkFont(size=30))
        icon_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(card, text=valor, font=ctk.CTkFont(size=24, weight="bold"))
        value_label.pack(pady=5)
        
        title_label = ctk.CTkLabel(card, text=titulo, font=ctk.CTkFont(size=12))
        title_label.pack(pady=(0, 15))

    def inicializar_inventario(self):
     """Cargar productos predefinidos al inventario"""
    # Agregar productos de prueba
     productos_iniciales = [
          ("Laptop", "Electrónica", 1500.00, 10),
          ("Teléfono", "Electrónica", 800.00, 5),
          ("Silla", "Muebles", 120.00, 20),
          ("Mesa", "Muebles", 200.00, 15),
          ("Libro", "Educación", 30.00, 50),
          ("Cámara", "Fotografía", 600.00, 7)
          ]
    
     for nombre, tipo, precio, cantidad in productos_iniciales:
        articulo = Articulo(nombre, tipo, precio, cantidad)
        self.inventario.agregar_articulo(articulo)
    
     print(f"Inventario inicializado con {len(productos_iniciales)} productos")    
    
    def mostrar_inventario(self):
       """Mostrar la interfaz del inventario con productos y controles"""
       self.limpiar_contenido()
    
    # Título
       title_label = ctk.CTkLabel(
        self.content_frame,
        text="📦 Gestión de Inventario",
        font=ctk.CTkFont(size=24, weight="bold")
        )
       title_label.pack(pady=20)
    
    # Frame principal del inventario
       inv_frame = ctk.CTkFrame(self.content_frame)
       inv_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Frame de controles
       controls_frame = ctk.CTkFrame(inv_frame)
       controls_frame.pack(fill="x", padx=20, pady=10)
    
    # Botones de control
       btn_agregar = ctk.CTkButton(
        controls_frame,
        text="➕ Agregar Producto",
        command=self.agregar_producto,
        height=35
       )
       btn_agregar.pack(side="left", padx=5)
    
    # Frame de ordenamiento
       sort_frame = ctk.CTkFrame(controls_frame)
       sort_frame.pack(side="right", padx=10)
    
       sort_label = ctk.CTkLabel(sort_frame, text="Ordenar por:")
       sort_label.pack(side="left", padx=5)
    
       self.sort_var = ctk.StringVar(value="nombre")
       sort_menu = ctk.CTkOptionMenu(
        sort_frame,
        values=["nombre", "precio", "cantidad", "tipo"],
        variable=self.sort_var,
        command=self.ordenar_inventario
          )
       sort_menu.pack(side="left", padx=5)
    
    # Frame de búsqueda
       search_frame = ctk.CTkFrame(controls_frame)
       search_frame.pack(side="right", padx=10)
    
       self.search_var = ctk.StringVar()
       search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Buscar producto...",
        textvariable=self.search_var,
        width=200
         )
       search_entry.pack(side="left", padx=5)
       search_entry.bind("<KeyRelease>", self.buscar_producto)
    
       btn_buscar = ctk.CTkButton(
        search_frame,
        text="🔍",
        command=self.buscar_producto,
        width=30
        )
       btn_buscar.pack(side="left", padx=5)
    
    # Frame scrollable para la lista de productos
       self.productos_frame = ctk.CTkScrollableFrame(
        inv_frame, 
        label_text="Lista de Productos",
        height=400
         )
       self.productos_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Cargar y mostrar productos
       self.cargar_productos_en_interfaz()

    def cargar_productos_en_interfaz(self, productos_filtrados=None):
      """Cargar productos en la interfaz gráfica"""
    # Limpiar productos existentes
      for widget in self.productos_frame.winfo_children():
        widget.destroy()
    
    # Obtener lista de nodos del inventario
      try:
         lista_nodos = self.inventario.pasar_a_lista_nodos(self.inventario)
         print(f"DEBUG: Se encontraron {len(lista_nodos)} productos en el inventario")
        
        # Usar productos filtrados si se proporcionan
         if productos_filtrados is not None:
            lista_nodos = productos_filtrados
            print(f"DEBUG: Usando productos filtrados: {len(lista_nodos)}")
        
        # Si no hay productos
         if not lista_nodos:
            no_products_label = ctk.CTkLabel(
                self.productos_frame,
                text="No se encontraron productos",
                font=ctk.CTkFont(size=16)
            )
            no_products_label.pack(pady=50)
            return
        
        # Crear tarjetas para cada producto
         print(f"DEBUG: Creando tarjetas para {len(lista_nodos)} productos...")
         for i, nodo in enumerate(lista_nodos):
            print(f"DEBUG: Creando tarjeta {i+1}: {nodo.dato.nombre}")
            self.crear_tarjeta_producto(nodo)
            
      except Exception as e:
        print(f"ERROR en cargar_productos_en_interfaz: {e}")
        error_label = ctk.CTkLabel(
            self.productos_frame,
            text=f"Error al cargar productos: {str(e)}",
            font=ctk.CTkFont(size=16),
            text_color=("red", "lightcoral")
        )
        error_label.pack(pady=50)

    def crear_tarjeta_producto(self, nodo):
      """Crear una tarjeta visual para un producto"""
      articulo = nodo.dato
      cantidad_disponible = len(nodo.pila.items)
    
    # Frame principal de la tarjeta
      card_frame = ctk.CTkFrame(self.productos_frame)
      card_frame.pack(fill="x", padx=10, pady=5)
    
    # Configurar grid
      card_frame.grid_columnconfigure(1, weight=1)
    
    # Icono del producto (basado en tipo)
      iconos_tipo = {
        "Electrónica": "💻",
        "Muebles": "🪑", 
        "Educación": "📚",
        "Fotografía": "📷"
       }
      icono = iconos_tipo.get(articulo.tipo, "📦")
    
      icon_label = ctk.CTkLabel(
        card_frame,
        text=icono,
        font=ctk.CTkFont(size=30)
      )
      icon_label.grid(row=0, column=0, rowspan=2, padx=15, pady=15)
    
    # Información del producto
      info_frame = ctk.CTkFrame(card_frame)
      info_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
      info_frame.grid_columnconfigure(1, weight=1)
    
    # Nombre del producto
      nombre_label = ctk.CTkLabel(
        info_frame,
        text=articulo.nombre,
        font=ctk.CTkFont(size=18, weight="bold")
       )
      nombre_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)
    
    # Tipo
      tipo_label = ctk.CTkLabel(
        info_frame,
        text=f"Categoría: {articulo.tipo}",
        font=ctk.CTkFont(size=12)
       )
      tipo_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
    
    # Precio
      precio_label = ctk.CTkLabel(
        info_frame,
        text=f"Precio: ${articulo.precio:.2f}",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=("green", "lightgreen")
     )
      precio_label.grid(row=1, column=1, sticky="e", padx=10, pady=2)
    
    # Cantidad disponible
      color_cantidad = ("red", "lightcoral") if cantidad_disponible < 5 else ("blue", "lightblue")
      cantidad_label = ctk.CTkLabel(
        info_frame,
        text=f"Stock: {cantidad_disponible} unidades",
        font=ctk.CTkFont(size=12),
        text_color=color_cantidad
      )
      cantidad_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)
    
    # Botones de acción
      buttons_frame = ctk.CTkFrame(card_frame)
      buttons_frame.grid(row=0, column=2, padx=10, pady=10)
    
      btn_editar = ctk.CTkButton(
        buttons_frame,
        text="✏️",
        width=30,
        command=lambda a=articulo: self.editar_producto(a)
       )
      btn_editar.pack(pady=2)
    
      btn_eliminar = ctk.CTkButton(
        buttons_frame,
        text="🗑️",
        width=30,
        fg_color=("red", "darkred"),
        hover_color=("darkred", "red"),
        command=lambda n=articulo.nombre: self.confirmar_eliminar_producto(n)
      )
      btn_eliminar.pack(pady=2)

    def ordenar_inventario(self, criterio):
       """Ordenar productos según el criterio seleccionado"""
       lista_nodos = self.inventario.pasar_a_lista_nodos(self.inventario)
    
       if criterio == "nombre":
        productos_ordenados = self.inventario.ordenarAlfabeticamente(lista_nodos)
       elif criterio == "precio":
        productos_ordenados = self.inventario.ordenarPorPrecios(lista_nodos)
       elif criterio == "cantidad":
        productos_ordenados = self.inventario.ordenarPorCantidad(lista_nodos)
       elif criterio == "tipo":
        # Ordenar por tipo (implementación básica)
        productos_ordenados = sorted(lista_nodos, key=lambda x: x.dato.tipo.lower())
       else:
        productos_ordenados = lista_nodos
    
       self.cargar_productos_en_interfaz(productos_ordenados)

    def buscar_producto(self, event=None):
      """Buscar productos que coincidan con el término de búsqueda"""
      termino = self.search_var.get().strip().lower()
    
      if not termino:
        # Si no hay término de búsqueda, mostrar todos
        self.cargar_productos_en_interfaz()
        return
    
    # Buscar productos que contengan el término
      lista_nodos = self.inventario.pasar_a_lista_nodos(self.inventario)
      productos_filtrados = []
    
      for nodo in lista_nodos:
        articulo = nodo.dato
        if (termino in articulo.nombre.lower() or 
            termino in articulo.tipo.lower() or
            termino in str(articulo.precio)):
            productos_filtrados.append(nodo)
    
      self.cargar_productos_en_interfaz(productos_filtrados)

    def agregar_producto(self):
      """Abrir modal para agregar nuevo producto"""
      messagebox.showinfo("Agregar Producto", "Funcionalidad de agregar producto en desarrollo...")

    def editar_producto(self, articulo):
      """Editar un producto existente"""
      messagebox.showinfo("Editar Producto", f"Editando: {articulo.nombre}")

    def confirmar_eliminar_producto(self, nombre_producto):
       """Confirmar eliminación de producto"""
       if messagebox.askyesno("Confirmar Eliminación", 
                          f"¿Estás seguro de eliminar '{nombre_producto}' del inventario?"):
        # Aquí iría la lógica de eliminación
         messagebox.showinfo("Producto Eliminado", f"'{nombre_producto}' ha sido eliminado del inventario")
         self.cargar_productos_en_interfaz()  # Refrescar vista
    
    def mostrar_nueva_compra(self):
        """Mostrar la interfaz para nueva compra"""
        self.limpiar_contenido()
        
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="🛍️ Nueva Compra",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        compra_frame = ctk.CTkFrame(self.content_frame)
        compra_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        placeholder = ctk.CTkLabel(
            compra_frame,
            text="Módulo de compra en construcción...",
            font=ctk.CTkFont(size=16)
        )
        placeholder.pack(pady=100)
    
    def mostrar_gestion_tarjetas(self):
        """Mostrar gestión de tarjetas"""
        self.limpiar_contenido()
        
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="💳 Gestión de Tarjetas",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        tarjetas_frame = ctk.CTkFrame(self.content_frame)
        tarjetas_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        placeholder = ctk.CTkLabel(
            tarjetas_frame,
            text="Módulo de tarjetas en construcción...",
            font=ctk.CTkFont(size=16)
        )
        placeholder.pack(pady=100)
    
    def mostrar_reportes(self):
        """Mostrar reportes del sistema"""
        self.limpiar_contenido()
        
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="📊 Reportes del Sistema",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        reportes_frame = ctk.CTkFrame(self.content_frame)
        reportes_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        placeholder = ctk.CTkLabel(
            reportes_frame,
            text="Módulo de reportes en construcción...",
            font=ctk.CTkFont(size=16)
        )
        placeholder.pack(pady=100)
    
    def mostrar_configuracion(self):
        """Mostrar configuración del sistema"""
        self.limpiar_contenido()
        
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="⚙️ Configuración del Sistema",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=20)
        
        config_frame = ctk.CTkFrame(self.content_frame)
        config_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        
        theme_label = ctk.CTkLabel(config_frame, text="Tema de la aplicación:", font=ctk.CTkFont(size=14))
        theme_label.pack(pady=10)
        
        theme_var = ctk.StringVar(value="light")
        theme_menu = ctk.CTkOptionMenu(
            config_frame,
            values=["light", "dark"],
            variable=theme_var,
            command=self.cambiar_tema
        )
        theme_menu.pack(pady=5)
    
    def cambiar_tema(self, nuevo_tema):
        """Cambiar el tema de la aplicación"""
        ctk.set_appearance_mode(nuevo_tema)
    
    def nuevo_cliente(self):
        self.modal_cliente = ctk.CTkToplevel(self.root)
        self.modal_cliente.title("➕ Nuevo Cliente")
        self.modal_cliente.geometry("500x600")
        self.modal_cliente.transient(self.root)
        self.modal_cliente.grab_set()
    
     # Centrar la ventana modal
        self.modal_cliente.update_idletasks()
        x = (self.modal_cliente.winfo_screenwidth() // 2) - (250)
        y = (self.modal_cliente.winfo_screenheight() // 2) - (300)
        self.modal_cliente.geometry(f"500x600+{x}+{y}")
    
     # Frame principal
        main_frame = ctk.CTkFrame(self.modal_cliente)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
     # Título
        title_label = ctk.CTkLabel(
        main_frame,
        text="Registrar Nuevo Cliente",
        font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(10, 30))
    
     # Frame para el formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="x", padx=22, pady=17)
    
     # Variables para los campos
        self.nombre_var = ctk.StringVar()
        self.apellido_var = ctk.StringVar()
        self.telefono_var = ctk.StringVar()
        self.correo_var = ctk.StringVar()
        self.direccion_var = ctk.StringVar()
        self.id_cliente_var = ctk.StringVar()
        self.fecha_registro_var=ctk.StringVar()
        self.password_var=ctk.StringVar()
     # Campos del formulario
        fields=[
            ("Nombre:", self.nombre_var),
            ("Apellido:", self.apellido_var),
            ("Teléfono:", self.telefono_var),
            ("Correo:", self.correo_var),
            ("Dirección:", self.direccion_var),
            ("ID Cliente:", self.id_cliente_var),
            ("Fecha de Registro",self.fecha_registro_var),
            ("Contraseña",self.password_var)
        ]
    
     # Crear los campos
        for i, (label_text, var) in enumerate(fields):
        # Label
            label = ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(size=14))
            label.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Entry
            entry = ctk.CTkEntry(
                form_frame, 
                textvariable=var,
                height=35,
                font=ctk.CTkFont(size=12)
            )
            entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Si es el primer campo, darle foco
            if i == 0:
                entry.focus()
    
     # Frame para botones
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=20, pady=20)
    
     # Botón Cancelar
        btn_cancelar = ctk.CTkButton(
          buttons_frame,
          text="❌ Cancelar",
          command=self.modal_cliente.destroy,
          height=40,
          fg_color=("gray70", "gray30"),
          hover_color=("gray60", "gray40")
           )
        btn_cancelar.pack(side="right", padx=(10, 20), pady=15)
    
    # Botón Guardar
        btn_guardar = ctk.CTkButton(
          buttons_frame,
          text="💾 Guardar Cliente",
          command=self.guardar_cliente,
          height=40,
          font=ctk.CTkFont(size=14, weight="bold")
          )
        btn_guardar.pack(side="right", padx=20, pady=15)

    def guardar_cliente(self):
      """Validar y guardar el nuevo cliente"""
    
    # Obtener valores
      nombre = self.nombre_var.get().strip()
      apellido = self.apellido_var.get().strip()
      telefono = self.telefono_var.get().strip()
      correo = self.correo_var.get().strip()
      direccion = self.direccion_var.get().strip()
      id_cliente = self.id_cliente_var.get().strip()
      fecha_registro=self.fecha_registro_var.get().strip()
      password=self.password_var.get().strip()
    
    # Validaciones básicas
      errores = []
    
      if not nombre:
        errores.append("• El nombre es obligatorio")
    
      if not apellido:
        errores.append("• El apellido es obligatorio")
        
      if not telefono:
        errores.append("• El teléfono es obligatorio")
      elif not telefono.isdigit() or len(telefono) < 8:
        errores.append("• El teléfono debe tener al menos 8 dígitos")
    
      if not correo:
        errores.append("• El correo es obligatorio")
      elif "@" not in correo or "." not in correo.split("@")[-1]:
        errores.append("• El formato del correo no es válido")
    
      if not direccion:
        errores.append("• La dirección es obligatoria")
        
      if not id_cliente:
        errores.append("• El ID del cliente es obligatorio")
    
    # Si hay errores, mostrarlos
      if errores:
        mensaje_error = "Por favor corrige los siguientes errores:\n\n" + "\n".join(errores)
        messagebox.showerror("Errores de validación", mensaje_error)
        return
    
    # Intentar registrar el cliente
      try:
        # Crear objeto cliente con fecha actual
         from Fechas import Tiempo
         fecha_registro = Tiempo.Ahora()

        
        # Intentar registrar en el sistema
         if self.gestion_clientes.registrar_cliente(nombre,id_cliente,password,apellido, telefono, correo,direccion,fecha_registro):
            messagebox.showinfo(
                "Cliente Registrado", 
                f"Cliente {nombre} {apellido} registrado exitosamente!\nID: {id_cliente}"
            )
            
            # Cerrar modal
            self.modal_cliente.destroy()
            
            # Actualizar la vista de clientes si está activa
            self.actualizar_lista_clientes()
            
         else:
            messagebox.showerror(
                "Error de Registro", 
                f"Ya existe un cliente con el ID: {id_cliente}\nPor favor usa un ID diferente."
            )
            
      except Exception as e:
        messagebox.showerror("Error", f"Error al registrar cliente: {str(e)}")
    def mostrar_gestion_clientes(self):
      """Mostrar la interfaz de gestión de clientes"""
    # Limpiar el contenido actual
      self.limpiar_contenido()
    
    # Título principal
      title_label = ctk.CTkLabel(
        self.content_frame,
        text="👥 Gestión de Clientes",
        font=ctk.CTkFont(size=24, weight="bold")
       )
      title_label.pack(pady=20)
    
    # Frame principal para clientes
      clientes_frame = ctk.CTkFrame(self.content_frame)
      clientes_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Frame para botones superiores (más completo que el primero)
      buttons_frame = ctk.CTkFrame(clientes_frame)
      buttons_frame.pack(fill="x", padx=20, pady=10)
    
    # Botón Nuevo Cliente
      btn_nuevo = ctk.CTkButton(
         buttons_frame,
         text="➕ Nuevo Cliente",
         command=self.nuevo_cliente,
         height=40,
         font=ctk.CTkFont(size=14, weight="bold")
         )
      btn_nuevo.pack(side="left", padx=20, pady=15)
    
    # Botón Buscar Cliente
      btn_buscar = ctk.CTkButton(
         buttons_frame,
         text="🔍 Buscar Cliente",
         command=self.buscar_cliente,
         height=40
          )
      btn_buscar.pack(side="left", padx=10, pady=15)
    
    # Botón Actualizar Lista (funcionalidad del segundo método)
      btn_actualizar = ctk.CTkButton(
         buttons_frame,
         text="🔄 Actualizar",
         command=self.actualizar_lista_clientes,
         height=40,
         fg_color=("gray70", "gray30"),
         hover_color=("gray60", "gray40")
         )
      btn_actualizar.pack(side="right", padx=20, pady=15)
    
    # Título de la lista
      list_title = ctk.CTkLabel(
        clientes_frame,
        text="Lista de Clientes",
        font=ctk.CTkFont(size=16, weight="bold")
         )
      list_title.pack(pady=(20, 10))
    
    # Frame scrollable para la lista de clientes
      self.lista_frame = ctk.CTkScrollableFrame(clientes_frame, height=400)
      self.lista_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Cargar la lista inicial de clientes
      self.actualizar_lista_clientes()

    def actualizar_lista_clientes(self):
      """Actualizar la lista visual de clientes"""
    # Verificar que lista_frame existe
      if not hasattr(self, 'lista_frame'):
        return
    
    # Limpiar la lista actual
      for widget in self.lista_frame.winfo_children():
         widget.destroy()

    # Verificar si hay clientes registrados
      if not hasattr(self, 'gestion_clientes') or not self.gestion_clientes.clientes:
        # Mostrar mensaje cuando no hay clientes
          placeholder = ctk.CTkLabel(
            self.lista_frame,
            text="No hay clientes registrados. Haz clic en 'Nuevo Cliente' para comenzar.",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
            )
          placeholder.pack(pady=50)
          return

    # Headers de la tabla
      headers_frame = ctk.CTkFrame(self.lista_frame)
      headers_frame.pack(fill="x", padx=10, pady=(5, 15))

      headers = ["ID Cliente", "Nombre", "Apellido", "Teléfono", "Correo", "Fecha Registro", "Acciones"]
      header_widths = [100, 120, 120, 100, 180, 120, 120]

      for i, (header, width) in enumerate(zip(headers, header_widths)):
          header_label = ctk.CTkLabel(
             headers_frame,
             text=header,
             font=ctk.CTkFont(size=12, weight="bold"),
             width=width
             )
          header_label.grid(row=0, column=i, padx=5, pady=10, sticky="w")

    # Mostrar cada cliente
      for i, cliente in enumerate(self.gestion_clientes.clientes):
         # Frame para cada cliente
         cliente_frame = ctk.CTkFrame(self.lista_frame)
         cliente_frame.pack(fill="x", padx=10, pady=2)
        
        # Datos del cliente
         datos = [
            getattr(cliente, 'id_cliente', 'N/A'),
            getattr(cliente, 'nombre', 'N/A'),
            getattr(cliente, 'apellido', 'N/A'),
            getattr(cliente, 'telefono', 'N/A'),
            getattr(cliente, 'correo', 'N/A'),
            str(getattr(cliente, 'fecha_registro', 'N/A'))[:10],  # Solo la fecha
           ]
        
        # Mostrar datos en columnas
         for j, (dato, width) in enumerate(zip(datos, header_widths[:-1])):
            dato_label = ctk.CTkLabel(
                cliente_frame,
                text=str(dato),
                font=ctk.CTkFont(size=11),
                width=width,
                anchor="w"
              )
            dato_label.grid(row=0, column=j, padx=5, pady=8, sticky="w")
        
        # Botones de acción
         acciones_frame = ctk.CTkFrame(cliente_frame)
         acciones_frame.grid(row=0, column=len(datos), padx=5, pady=5)
        
        # Botón Ver/Editar
         btn_ver = ctk.CTkButton(
            acciones_frame,
            text="👁️",
            width=30,
            height=25,
            command=lambda c=cliente: self.ver_cliente(c),
            font=ctk.CTkFont(size=12)
            )
         btn_ver.pack(side="left", padx=2)
        
        # Botón Eliminar
         btn_eliminar = ctk.CTkButton(
            acciones_frame,
            text="🗑️",
            width=30,
            height=25,
            fg_color=("red", "darkred"),
            hover_color=("darkred", "red"),
            command=lambda c=cliente: self.confirmar_eliminar_cliente(c),
            font=ctk.CTkFont(size=12)
           )
         btn_eliminar.pack(side="left", padx=2)

    # Contador total de clientes
      total_label = ctk.CTkLabel(
         self.lista_frame,
         text=f"Total de clientes: {len(self.gestion_clientes.clientes)}",
         font=ctk.CTkFont(size=12, weight="bold")
         )
      total_label.pack(pady=10)

# Método auxiliar para asegurar que limpiar_contenido existe
    def limpiar_contenido(self):
      """Limpiar el contenido del frame principal"""
      if hasattr(self, 'content_frame'):
         for widget in self.content_frame.winfo_children():
             widget.destroy()
      else:
        # Si content_frame no existe, créarlo
         self.content_frame = ctk.CTkFrame(self.root)
         self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
    def ver_cliente(self, cliente):
      """Mostrar detalles del cliente"""
      from tkinter import messagebox
    
      info = f"""
        ID Cliente: {cliente.id_cliente}
        Nombre: {cliente.nombre} {cliente.apellido}
        Teléfono: {cliente.telefono}
        Correo: {cliente.correo}
        Dirección: {cliente.direccion_envio}
        Fecha Registro: {cliente.fecha_registro}
        """
    
      messagebox.showinfo(f"Cliente: {cliente.nombre}", info)

    def confirmar_eliminar_cliente(self, cliente):
     """Confirmar eliminación de cliente"""
     from tkinter import messagebox
    
     respuesta = messagebox.askyesno(
        "Confirmar Eliminación",
        f"¿Estás seguro de que deseas eliminar al cliente?\n\n"
        f"Nombre: {cliente.nombre} {cliente.apellido}\n"
        f"ID: {cliente.id_cliente}\n\n"
        f"Esta acción no se puede deshacer."
        )
    
     if respuesta:
        
        if cliente in self.gestion_clientes.clientes:
            self.gestion_clientes.clientes.remove(cliente)
            self.gestion_clientes.guardar_clientes()
            messagebox.showinfo("Cliente Eliminado", f"Cliente {cliente.nombre} eliminado exitosamente")
            self.actualizar_lista_clientes()  # Refrescar la lista
    def buscar_cliente(self):
      """Abrir diálogo para buscar cliente"""
    # Crear ventana modal para búsqueda
      self.modal_busqueda = ctk.CTkToplevel(self.root)
      self.modal_busqueda.title("🔍 Buscar Cliente")
      self.modal_busqueda.geometry("700x500")
      self.modal_busqueda.transient(self.root)
      self.modal_busqueda.grab_set()
    
    # Centrar la ventana modal
      self.modal_busqueda.update_idletasks()
      x = (self.modal_busqueda.winfo_screenwidth() // 2) - (350)
      y = (self.modal_busqueda.winfo_screenheight() // 2) - (250)
      self.modal_busqueda.geometry(f"700x500+{x}+{y}")
    
    # Frame principal
      main_frame = ctk.CTkFrame(self.modal_busqueda)
      main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
      title_label = ctk.CTkLabel(
         main_frame,
         text="Buscar Cliente",
         font=ctk.CTkFont(size=20, weight="bold")
          )
      title_label.pack(pady=(10, 20))
    
    # Frame para búsqueda
      search_frame = ctk.CTkFrame(main_frame)
      search_frame.pack(fill="x", padx=20, pady=10)
    
    # Variable para el término de búsqueda
      self.busqueda_var = ctk.StringVar()
      self.busqueda_var.trace("w", lambda name, index, mode: self.filtrar_clientes_tiempo_real())
    
    # Campo de búsqueda
      search_label = ctk.CTkLabel(
         search_frame, 
         text="Buscar por nombre, apellido, ID o correo:",
         font=ctk.CTkFont(size=14)
          )
      search_label.pack(anchor="w", padx=20, pady=(15, 5))
    
      self.entry_busqueda = ctk.CTkEntry(
         search_frame,
         textvariable=self.busqueda_var,
         height=35,
         font=ctk.CTkFont(size=12),
         placeholder_text="Escribe para buscar..."
         )
      self.entry_busqueda.pack(fill="x", padx=20, pady=(0, 15))
      self.entry_busqueda.focus()
    
    # Frame para opciones de búsqueda
      options_frame = ctk.CTkFrame(search_frame)
      options_frame.pack(fill="x", padx=20, pady=(0, 15))
    
    # Variables para filtros
      self.filtro_activo = ctk.BooleanVar(value=True)
      self.tipo_busqueda = ctk.StringVar(value="todos")
    
    # Checkbox para mostrar solo activos
      checkbox_activos = ctk.CTkCheckBox(
         options_frame,
         text="Solo clientes activos",
         variable=self.filtro_activo,
         command=self.filtrar_clientes_tiempo_real
         )
      checkbox_activos.pack(side="left", padx=20, pady=10)
    
    # Selector de tipo de búsqueda
      tipo_label = ctk.CTkLabel(options_frame, text="Buscar en:")
      tipo_label.pack(side="left", padx=(40, 10), pady=10)
    
      tipo_menu = ctk.CTkOptionMenu(
         options_frame,
         values=["Todos los campos", "Solo nombre", "Solo ID", "Solo correo"],
         variable=self.tipo_busqueda,
         command=lambda x: self.filtrar_clientes_tiempo_real()
         )
      tipo_menu.pack(side="left", padx=10, pady=10)
    
    # Botones de acción rápida
      buttons_frame = ctk.CTkFrame(search_frame)
      buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
     
      btn_limpiar = ctk.CTkButton(
         buttons_frame,
         text="🗑️ Limpiar",
         command=self.limpiar_busqueda,
         height=30,
         width=100,
         fg_color=("gray70", "gray30")
         )
      btn_limpiar.pack(side="left", padx=20, pady=10)
    
      btn_buscar_avanzado = ctk.CTkButton(
         buttons_frame,
         text="🔍 Búsqueda Avanzada",
         command=self.busqueda_avanzada,
         height=30,
         width=150
         )
      btn_buscar_avanzado.pack(side="right", padx=20, pady=10)
    
    # Frame para resultados
      results_label = ctk.CTkLabel(
            main_frame,
        text="Resultados de la búsqueda:",
        font=ctk.CTkFont(size=16, weight="bold")
        )
      results_label.pack(pady=(20, 10))
    
    # Frame scrollable para resultados
      self.resultados_frame = ctk.CTkScrollableFrame(main_frame, height=250)
      self.resultados_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Frame para botones inferiores
      bottom_buttons = ctk.CTkFrame(main_frame)
      bottom_buttons.pack(fill="x", padx=20, pady=10)
    
      btn_cerrar = ctk.CTkButton(
         bottom_buttons,
         text="❌ Cerrar",
         command=self.modal_busqueda.destroy,
         height=35,
         fg_color=("gray70", "gray30")
         )
      btn_cerrar.pack(side="right", padx=20, pady=10)
    
    # Mostrar todos los clientes inicialmente
      self.filtrar_clientes_tiempo_real()

    def filtrar_clientes_tiempo_real(self):
     """Filtrar clientes en tiempo real mientras se escribe"""
     try:
        # Limpiar resultados anteriores
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        # Obtener término de búsqueda
        termino = self.busqueda_var.get().lower().strip()
        tipo = self.tipo_busqueda.get()
        
        # Filtrar clientes
        clientes_filtrados = []
        for cliente in self.gestion_clientes.clientes:
            # Aplicar filtros
            if self.filtro_activo.get():
                
                pass
            
            # Aplicar búsqueda por término
            if not termino:  # Si no hay término, mostrar todos
                clientes_filtrados.append(cliente)
                continue
            
            # Determinar en qué campos buscar según el tipo seleccionado
            campos_busqueda = []
            if tipo == "Todos los campos":
                campos_busqueda = [
                    cliente.nombre.lower(),
                    cliente.apellido.lower(),
                    cliente.id_cliente.lower(),
                    cliente.correo.lower(),
                    cliente.telefono.lower() if hasattr(cliente, 'telefono') else ""
                ]
            elif tipo == "Solo nombre":
                campos_busqueda = [cliente.nombre.lower(), cliente.apellido.lower()]
            elif tipo == "Solo ID":
                campos_busqueda = [cliente.id_cliente.lower()]
            elif tipo == "Solo correo":
                campos_busqueda = [cliente.correo.lower()]
            
            # Verificar si el término está en algún campo
            if any(termino in campo for campo in campos_busqueda):
                clientes_filtrados.append(cliente)
        
        # Mostrar resultados
        if not clientes_filtrados:
            no_results = ctk.CTkLabel(
                self.resultados_frame,
                text="No se encontraron clientes que coincidan con la búsqueda.",
                font=ctk.CTkFont(size=14),
                text_color=("gray60", "gray40")
            )
            no_results.pack(pady=30)
        else:
            # Mostrar header
            header_frame = ctk.CTkFrame(self.resultados_frame)
            header_frame.pack(fill="x", padx=10, pady=(5, 10))
            
            headers = ["ID", "Nombre Completo", "Correo", "Teléfono", "Acciones"]
            for i, header in enumerate(headers):
                header_label = ctk.CTkLabel(
                    header_frame,
                    text=header,
                    font=ctk.CTkFont(size=12, weight="bold")
                )
                header_label.grid(row=0, column=i, padx=10, pady=8, sticky="w")
            
            # Mostrar cada cliente encontrado
            for cliente in clientes_filtrados:
                self.mostrar_cliente_resultado(cliente)
        
        # Actualizar contador
        count_label = ctk.CTkLabel(
            self.resultados_frame,
            text=f"Se encontraron {len(clientes_filtrados)} cliente(s)",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        count_label.pack(pady=5)
        
     except Exception as e:
        print(f"Error en filtro: {e}")

    def mostrar_cliente_resultado(self, cliente):
      """Mostrar un cliente en los resultados de búsqueda"""
      resultado_frame = ctk.CTkFrame(self.resultados_frame)
      resultado_frame.pack(fill="x", padx=10, pady=2)
    
    # Datos del cliente
      id_label = ctk.CTkLabel(
        resultado_frame,
        text=cliente.id_cliente,
        font=ctk.CTkFont(size=11),
        width=80
       )
      id_label.grid(row=0, column=0, padx=10, pady=8, sticky="w")
    
      nombre_completo = f"{cliente.nombre} {cliente.apellido}"
      nombre_label = ctk.CTkLabel(
        resultado_frame,
        text=nombre_completo,
        font=ctk.CTkFont(size=11),
        width=150
       )
      nombre_label.grid(row=0, column=1, padx=10, pady=8, sticky="w")
    
      correo_label = ctk.CTkLabel(
        resultado_frame,
        text=cliente.correo,
        font=ctk.CTkFont(size=11),
        width=180
       )
      correo_label.grid(row=0, column=2, padx=10, pady=8, sticky="w")
    
      telefono_text = getattr(cliente, 'telefono', 'N/A')
      telefono_label = ctk.CTkLabel(
        resultado_frame,
        text=telefono_text,
        font=ctk.CTkFont(size=11),
        width=100
        )
      telefono_label.grid(row=0, column=3, padx=10, pady=8, sticky="w")
    
    # Botones de acción
      acciones_frame = ctk.CTkFrame(resultado_frame)
      acciones_frame.grid(row=0, column=4, padx=10, pady=5)
     
      btn_ver = ctk.CTkButton(
        acciones_frame,
        text="👁️ Ver",
        width=60,
        height=25,
        command=lambda: self.ver_cliente_desde_busqueda(cliente),
        font=ctk.CTkFont(size=10)
        )
      btn_ver.pack(side="left", padx=2)
    
      btn_seleccionar = ctk.CTkButton(
        acciones_frame,
        text="✅ Seleccionar",
        width=80,
        height=25,
        command=lambda: self.seleccionar_cliente(cliente),
        font=ctk.CTkFont(size=10)
       )
      btn_seleccionar.pack(side="left", padx=2)

    def ver_cliente_desde_busqueda(self, cliente):
     """Ver detalles del cliente desde la búsqueda"""
     self.ver_cliente(cliente)  # Usar la función ya existente

    def seleccionar_cliente(self, cliente):
     """Seleccionar un cliente y cerrar la búsqueda"""
     from tkinter import messagebox
    
     respuesta = messagebox.showinfo(
        "Cliente Seleccionado",
        f"Has seleccionado:\n\n"
        f"ID: {cliente.id_cliente}\n"
        f"Nombre: {cliente.nombre} {cliente.apellido}\n"
        f"Correo: {cliente.correo}\n\n"
        f"¿Qué deseas hacer con este cliente?"
        )
    
    # Cerrar la ventana de búsqueda
     self.modal_busqueda.destroy()
     
    def limpiar_busqueda(self):
      """Limpiar el campo de búsqueda"""
      self.busqueda_var.set("")
      self.tipo_busqueda.set("Todos los campos")
      self.filtro_activo.set(True)
     
    def salir_aplicacion(self):
     """Confirmar y salir de la aplicación"""
     if messagebox.askyesno("Confirmar Salida", "¿Estás seguro de que deseas salir?"):
        self.root.quit()
        self.root.destroy()
    
    def ejecutar(self):
     """Ejecutar la aplicación"""
     self.root.mainloop()

def main():
  """Función principal"""
  try:
      app = SistemaCompraModerno()
      app.ejecutar()
  except Exception as e:
      print(f"Error al iniciar la aplicación: {e}")
      messagebox.showerror("Error", f"Error al iniciar: {e}")

if __name__ == "__main__":
 main()
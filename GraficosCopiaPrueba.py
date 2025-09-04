import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
clases_base_path = os.path.join(current_dir, "Clases_Base")
sys.path.append(clases_base_path)
estructuras_path = os.path.join(current_dir, "Estructuras")
sys.path.append(estructuras_path)
Proyecto_Estructuras_Python_path= os.path.join(current_dir,"Proyecto_Estructuras_Python")
sys.path.append(Proyecto_Estructuras_Python_path)
import uuid
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
from Estructuras.GestionRegistros import Registros
from Archivos.PersistenciaDatos import Archivo as file
from tkinter import simpledialog
from Clases_Base.Registro import Registro
class SistemaCompraModerno:
    def __init__(self):
        gestion_clientes, gestion_tarjetas, articulos, registros_lista = file.cargar_datos()
        self.clientes = gestion_clientes
        self.tarjetas = gestion_tarjetas
        self.articulos = articulos
        self.registros = Registros()
        self.registros = registros_lista
        ctk.set_appearance_mode("light")  
        ctk.set_default_color_theme("blue")  
        self.root = ctk.CTk()
        self.root.title("🛒 Sistema de Compra Profesional")
        self.root.geometry("1200x800")
        self.centrar_ventana()
        self.root.minsize(1000,700)
        self.usuario_actual = None
        self.carrito = None
        self.inventario = ListaInventario()
        self.gestion_clientes = GestionClientes("Clientes.csv")
        self.gestion_tarjetas = GestionTarjetas("Tarjetas.csv",self.gestion_clientes)
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
        self.main_container.pack(fill="both", expand=True, padx=5, pady=10)
        
        
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
        self.logo_label.grid(row=0, column=0, padx=20, pady=(15, 20))
        botones_menu = [
            ("🏠 Inicio", self.mostrar_bienvenida),
            ("👤 Gestión Clientes", self.mostrar_gestion_clientes),
            ("📦 Inventario", self.mostrar_inventario),
            ("🛍️ Nueva Compra", self.mostrar_nueva_compra),
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
        
        total_productos=self.inventario.contar_productos()
        total_clientes = len(self.gestion_clientes.clientes)
        total_ventas=self.calcular_ventas_hoy()
        stats_frame = ctk.CTkFrame(welcome_frame)
        stats_frame.pack(pady=40, padx=40, fill="x")
        stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.crear_stat_card(stats_frame, "👥", "Clientes", str(total_clientes), 0, 0)
        self.crear_stat_card(stats_frame, "📦", "Productos", str(total_productos), 0, 1)
        self.crear_stat_card(stats_frame, "💰", "Ventas Hoy", f"${total_ventas}", 0, 2)
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
     articulos_csv = file.cargar_articulos()
     for articulo in articulos_csv:
         self.inventario.agregar_articulo(articulo)
     print(f"Inventario inicializado con {len(articulos_csv)}")  

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
      self.modal_producto = ctk.CTkToplevel(self.root)
      self.modal_producto.title("➕ Nuevo Producto")
      self.modal_producto.geometry("500x600")
      self.modal_producto.transient(self.root)
      self.modal_producto.grab_set()

    # Centrar la ventana modal
      self.modal_producto.update_idletasks()
      x = (self.modal_producto.winfo_screenwidth() // 2) - (250)
      y = (self.modal_producto.winfo_screenheight() // 2) - (300)
      self.modal_producto.geometry(f"500x600+{x}+{y}")

    # Frame principal
      main_frame = ctk.CTkFrame(self.modal_producto)
      main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
      title_label = ctk.CTkLabel(
         main_frame,
         text="Registrar Nuevo Producto",
         font=ctk.CTkFont(size=20, weight="bold")
         )
      title_label.pack(pady=(10, 30))

    # Frame para el formulario
      form_frame = ctk.CTkFrame(main_frame)
      form_frame.pack(fill="x", padx=22, pady=17)

    # Variables para los campos
      self.nombre_producto_var = ctk.StringVar()
      self.tipo_producto_var = ctk.StringVar(value="Electrónica")  # Valor por defecto
      self.precio_producto_var = ctk.StringVar()
      self.cantidad_producto_var = ctk.StringVar()
  
    # Campo Nombre
      nombre_label = ctk.CTkLabel(form_frame, text="Nombre del Producto:", font=ctk.CTkFont(size=14))
      nombre_label.pack(anchor="w", padx=20, pady=(15, 5))
    
      nombre_entry = ctk.CTkEntry(
         form_frame, 
         textvariable=self.nombre_producto_var,
         height=35,
         font=ctk.CTkFont(size=12),
         placeholder_text="Ej: Laptop Gaming"
         )
      nombre_entry.pack(fill="x", padx=20, pady=(0, 10))
      nombre_entry.focus()  # Dar foco al primer campo

    # Campo Tipo/Categoría
      tipo_label = ctk.CTkLabel(form_frame, text="Categoría:", font=ctk.CTkFont(size=14))
      tipo_label.pack(anchor="w", padx=20, pady=(15, 5))
    
      tipo_menu = ctk.CTkOptionMenu(
         form_frame,
         values=["Electrónica", "Muebles", "Educación", "Fotografía", "Ropa", "Deportes", "Hogar", "Otros"],
         variable=self.tipo_producto_var,
         height=35,
         font=ctk.CTkFont(size=12)
         )
      tipo_menu.pack(fill="x", padx=20, pady=(0, 10))

    # Campo Precio
      precio_label = ctk.CTkLabel(form_frame, text="Precio (USD):", font=ctk.CTkFont(size=14))
      precio_label.pack(anchor="w", padx=20, pady=(15, 5))
    
      precio_entry = ctk.CTkEntry(
         form_frame, 
         textvariable=self.precio_producto_var,
         height=35,
         font=ctk.CTkFont(size=12),
         placeholder_text="Ej: 1299.99"
         ) 
      precio_entry.pack(fill="x", padx=20, pady=(0, 10))

    # Campo Cantidad
      cantidad_label = ctk.CTkLabel(form_frame, text="Cantidad Inicial:", font=ctk.CTkFont(size=14))
      cantidad_label.pack(anchor="w", padx=20, pady=(15, 5))
    
      cantidad_entry = ctk.CTkEntry(
         form_frame, 
         textvariable=self.cantidad_producto_var,
         height=35,
         font=ctk.CTkFont(size=12),
         placeholder_text="Ej: 10"
         )
      cantidad_entry.pack(fill="x", padx=20, pady=(0, 10))

    # Información adicional
      info_frame = ctk.CTkFrame(form_frame)
      info_frame.pack(fill="x", padx=20, pady=15)
    
      info_label = ctk.CTkLabel(
         info_frame,
         text="💡 Información: El producto se agregará al inventario con la cantidad especificada",
         font=ctk.CTkFont(size=11),
         text_color=("gray60", "gray40"),
         wraplength=400
         )
      info_label.pack(pady=10)

    # Frame para botones
      buttons_frame = ctk.CTkFrame(main_frame)
      buttons_frame.pack(fill="x", padx=20, pady=20)

    # Botón Cancelar
      btn_cancelar = ctk.CTkButton(
         buttons_frame,
         text="❌ Cancelar",
         command=self.modal_producto.destroy,
         height=40,
         fg_color=("gray70", "gray30"),
         hover_color=("gray60", "gray40")
         )
      btn_cancelar.pack(side="right", padx=(10, 20), pady=15)

    # Botón Guardar
      btn_guardar = ctk.CTkButton(
         buttons_frame,
         text="💾 Guardar Producto",
         command=self.guardar_producto,
         height=40,
         font=ctk.CTkFont(size=14, weight="bold")
         )
      btn_guardar.pack(side="right", padx=20, pady=15)
    def guardar_producto(self):
      """Validar y guardar el nuevo producto"""
      from tkinter import messagebox
    
    # Obtener valores
      nombre = self.nombre_producto_var.get().strip()
      tipo = self.tipo_producto_var.get().strip()
      precio_str = self.precio_producto_var.get().strip()
      cantidad_str = self.cantidad_producto_var.get().strip()
    
    # Validaciones básicas
      errores = []
    
      if not nombre:
         errores.append("• El nombre del producto es obligatorio")
      elif len(nombre) < 2:
         errores.append("• El nombre debe tener al menos 2 caracteres")
    
      if not tipo:
         errores.append("• Debe seleccionar una categoría")
    
    # Validar precio
      precio = None
      if not precio_str:
         errores.append("• El precio es obligatorio")
      else:
          try:
              precio = float(precio_str)
              if precio <= 0:
                 errores.append("• El precio debe ser mayor a 0")
              elif precio > 999999:
                 errores.append("• El precio no puede ser mayor a $999,999")
          except ValueError:
             errores.append("• El precio debe ser un número válido (ej: 99.99)")
    
    # Validar cantidad
      cantidad = None
      if not cantidad_str:
         errores.append("• La cantidad es obligatoria")
      else:
          try:
              cantidad = int(cantidad_str)
              if cantidad < 0:
                 errores.append("• La cantidad no puede ser negativa")
              elif cantidad > 10000:
                 errores.append("• La cantidad no puede ser mayor a 10,000")
          except ValueError:
            errores.append("• La cantidad debe ser un número entero")
    
    # Verificar si el producto ya existe usando el nuevo método
      if nombre and hasattr(self, 'inventario'):
          if self.inventario.existe_articulo(nombre):
             errores.append(f"• Ya existe un producto con ese nombre: '{nombre}'")
    
    # Si hay errores, mostrarlos
      if errores:
         mensaje_error = "Por favor corrige los siguientes errores:\n\n" + "\n".join(errores)
         messagebox.showerror("Errores de validación", mensaje_error)
         return
    
    # Intentar agregar el producto
      try:
        
        # Crear el nuevo artículo
          nuevo_articulo = Articulo(nombre, tipo, precio, cantidad)
        
        # Agregar al inventario
          print(f"DEBUG: Intentando agregar producto '{nombre}' al inventario")
          resultado = self.inventario.agregar_articulo(nuevo_articulo)
          print(f"DEBUG: Resultado de agregar_articulo: {resultado}")
        
          if resultado == True:
              articulos_para_guardar=[]
              actual = self.inventario.primero
              while actual:
                 art = actual.dato
                 articulos_para_guardar.append(art)
                 actual = actual.siguiente
              file.guardar_articulos(articulos_para_guardar)
              messagebox.showinfo(
                  "Producto Agregado", 
                  f"Producto '{nombre}' agregado exitosamente!\n\n"
                  f"Categoría: {tipo}\n"
                  f"Precio: ${precio:.2f}\n"
                  f"Cantidad: {cantidad} unidades"
                  )
            
            # Cerrar modal
              self.modal_producto.destroy()
            
            # Actualizar la vista del inventario si está activa
              self.actualizar_vista_inventario()
            
          elif resultado == False:
             messagebox.showerror(
                 "Error: Producto Duplicado", 
                 f"El producto '{nombre}' ya existe en el inventario.\n\n"
                 f"No se pueden tener productos con el mismo nombre."
                )
          else:
             messagebox.showerror(
                 "Error Desconocido", 
                 f"Ocurrió un error inesperado al agregar el producto.\n"
                 f"Valor devuelto: {resultado}"
                )
            
      except Exception as e:
         messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
         print(f"Error detallado: {e}")
    def actualizar_vista_inventario(self):
      """Actualizar la vista del inventario después de agregar un producto"""
      try:
        # Si estamos en la vista de inventario, recargar los productos
          if hasattr(self, 'productos_frame') and self.productos_frame.winfo_exists():
             self.cargar_productos_en_interfaz()
             print("Vista de inventario actualizada correctamente")
          else:
             print("No hay vista de inventario activa para actualizar")
      except Exception as e:
         print(f"Error al actualizar vista de inventario: {e}")     
 
    def editar_producto(self, articulo):
      """Editar un producto existente"""
      messagebox.showinfo("Editar Producto", f"Editando: {articulo.nombre}")

    def confirmar_eliminar_producto(self, nombre_producto):
       
      respuesta = messagebox.askyesno(
         "Confirmar Eliminación",
         f"¿Estás seguro de que deseas eliminar el producto?\n\n"
         f"Producto: {nombre_producto}\n\n"
         f"Esta acción eliminará todas las unidades del inventario\n"
         f"y no se puede deshacer."
         )
    
      if respuesta:
          try:
            # Eliminar del inventario
              resultado = self.inventario.eliminar_articulo(nombre_producto)
            
              if resultado:
                 messagebox.showinfo("Producto Eliminado", f"Producto '{nombre_producto}' eliminado exitosamente")
                 self.actualizar_vista_inventario()  # Refrescar la vista
              else:
                 messagebox.showerror("Error", f"No se pudo eliminar el producto '{nombre_producto}'")
                
          except Exception as e:
             messagebox.showerror("Error", f"Error al eliminar producto: {str(e)}")
             print(f"Error detallado: {e}")
    
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

        # Selección de cliente
        cliente_label = ctk.CTkLabel(compra_frame, text="Selecciona un cliente:", font=ctk.CTkFont(size=16))
        cliente_label.pack(pady=10)
        clientes_nombres = [f"{c.nombre} {c.apellido} ({c.id_cliente})" for c in self.gestion_clientes.clientes]
        self.cliente_compra_var = ctk.StringVar(value=clientes_nombres[0] if clientes_nombres else "")
        cliente_menu = ctk.CTkOptionMenu(compra_frame, values=clientes_nombres, variable=self.cliente_compra_var)
        cliente_menu.pack(pady=5)

        # Lista de productos con cantidad
        productos_label = ctk.CTkLabel(compra_frame, text="Selecciona productos y cantidad:", font=ctk.CTkFont(size=16))
        productos_label.pack(pady=10)
        productos_nodos = self.inventario.pasar_a_lista_nodos(self.inventario)
        self.productos_vars = []
        productos_frame = ctk.CTkFrame(compra_frame)
        productos_frame.pack(pady=10)
        for nodo in productos_nodos:
            var = ctk.IntVar(value=0)
            cantidad_var = ctk.StringVar(value="1")
            articulo = nodo.dato
            fila = ctk.CTkFrame(productos_frame)
            fila.pack(fill="x", pady=2)
            ctk.CTkCheckBox(fila, text=f"{articulo.nombre} (${articulo.precio:.2f})", variable=var).pack(side="left", padx=5)
            ctk.CTkLabel(fila, text="Cantidad:").pack(side="left", padx=5)
            ctk.CTkEntry(fila, textvariable=cantidad_var, width=50).pack(side="left", padx=5)
            self.productos_vars.append((var, cantidad_var, articulo, nodo))

        # Botón para agregar al carrito
        btn_agregar = ctk.CTkButton(
            compra_frame,
            text="Agregar al carrito",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.agregar_seleccion_a_carrito
        )
        btn_agregar.pack(pady=20)

        # Frame para mostrar el carrito
        self.carrito_frame = ctk.CTkFrame(compra_frame)
        self.carrito_frame.pack(fill="x", pady=10)
        self.carrito_label = ctk.CTkLabel(self.carrito_frame, text="Carrito vacío", font=ctk.CTkFont(size=14))
        self.carrito_label.pack(pady=10)

        # Botón para procesar pago
        btn_pagar = ctk.CTkButton(
            compra_frame,
            text="Procesar Pago",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.procesar_pago
        )
        btn_pagar.pack(pady=10)

    def agregar_seleccion_a_carrito(self):
        """Agregar productos seleccionados al carrito"""
        # Obtener cliente
        cliente_id = self.cliente_compra_var.get().split("(")[-1].replace(")", "").strip()
        cliente = next((c for c in self.gestion_clientes.clientes if c.id_cliente == cliente_id), None)
        if not cliente:
            self.carrito_label.configure(text="Selecciona un cliente válido.")
            return

        # Crear carrito si no existe o si cambió el cliente
        if self.carrito is None or self.carrito.cliente.id_cliente != cliente.id_cliente:
            self.carrito = CarroDeCompra(cliente)
        else:
            self.carrito.vaciar_carrito()

        # Agregar productos seleccionados
        for var, cantidad_var, articulo, nodo in self.productos_vars:
            if var.get() == 1:
                try:
                    cantidad = int(cantidad_var.get())
                    if cantidad < 1:
                        continue
                    stock = len(nodo.pila.items)
                    if cantidad > stock:
                        continue
                    self.carrito.agregar_item(
                        id_producto=articulo.nombre,
                        nombre=articulo.nombre,
                        cantidad=cantidad,
                        precio_unitario=articulo.precio
                    )
                except Exception:
                    continue

        self.actualizar_carrito_vista()

    def actualizar_carrito_vista(self):
        """Actualizar la vista del carrito"""
        for widget in self.carrito_frame.winfo_children():
            widget.destroy()
        if self.carrito and self.carrito.items:
            texto = "Carrito:\n"
            for item in self.carrito.items:
                texto += f"- {item['nombre']} x{item['cantidad']} = ${item['subtotal']:.2f}\n"
            texto += f"\nTotal: ${self.carrito.calcular_total():.2f}"
            self.carrito_label = ctk.CTkLabel(self.carrito_frame, text=texto, font=ctk.CTkFont(size=14))
            self.carrito_label.pack(pady=10)
        else:
            self.carrito_label = ctk.CTkLabel(self.carrito_frame, text="Carrito vacío", font=ctk.CTkFont(size=14))
            self.carrito_label.pack(pady=10)

    def procesar_pago(self):
        """Procesar el pago del carrito actual"""
        if not self.carrito or not self.carrito.items:
            messagebox.showinfo("Pago", "El carrito está vacío.")
            return
        ProcesarPago(self.carrito).procesar_pago()
        # Eliminar productos del inventario
        for item in self.carrito.items:
            nodo = next((n for n in self.inventario.pasar_a_lista_nodos(self.inventario) if n.dato.nombre == item["nombre"]), None)
            if nodo:
                for _ in range(item["cantidad"]):
                    if nodo.pila.items:
                        nodo.pila.items.pop()
        messagebox.showinfo("Pago", "Pago procesado con éxito")
        self.carrito = None
        self.actualizar_carrito_vista()
        self.cargar_productos_en_interfaz()  # Actualiza inventario en la interfaz
       
        
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
            
            if not self.registros.lista_registros:
               placeholder = ctk.CTkLabel(
                  reportes_frame,
                  text="No hay registros...",
                  font=ctk.CTkFont(size=16)
               )
               placeholder.pack(pady=100)
               return
            
            for registro in self.registros.lista_registros:
               frame = ctk.CTkFrame(reportes_frame)
               frame.pack(fill="x",padx=10,pady=5)

               texto = (
                  f"ID Registro: {registro.id_registro}\n"
                  f"Cliente: {registro.cliente.nombre} {registro.cliente.apellido}\n"
                  f"Total: ${registro.total:.2f}\n"
                  f"Método de Pago: {registro.metodoDePago}\n"
                  f"Estado: {registro.estado}\n"
                  f"Fecha: {registro.fecha}"
              )
               label = ctk.CTkLabel(frame, text=texto, justify = "left")
               label.pack(padx=10,pady=10)

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
      self.modal_cliente.geometry("500x700")  # Aumentar altura para más campos
      self.modal_cliente.transient(self.root)
      self.modal_cliente.grab_set()

    # Centrar la ventana modal
      self.modal_cliente.update_idletasks()
      x = (self.modal_cliente.winfo_screenwidth() // 2) - (250)
      y = (self.modal_cliente.winfo_screenheight() // 2) - (350)
      self.modal_cliente.geometry(f"500x700+{x}+{y}")

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

    # Frame para el formulario scrollable
      form_frame = ctk.CTkScrollableFrame(main_frame, height=400)
      form_frame.pack(fill="both", expand=True, padx=22, pady=17)

    # Variables para los campos
      self.nombre_var = ctk.StringVar()
      self.apellido_var = ctk.StringVar()
      self.telefono_var = ctk.StringVar()
      self.correo_var = ctk.StringVar()
      self.direccion_var = ctk.StringVar()
      self.password_var = ctk.StringVar()
    
    # GENERAR ID ÚNICO AUTOMÁTICAMENTE
   
      id_unico = str(uuid.uuid4())
      self.id_cliente_var = ctk.StringVar(value=id_unico)

    # Campos editables
      campos_editables = [
         ("Nombre:", self.nombre_var, "Ej: Juan"),
         ("Apellido:", self.apellido_var, "Ej: Pérez"),
         ("Teléfono:", self.telefono_var, "Ej: +506 8888-8888"),
         ("Correo:", self.correo_var, "Ej: juan@email.com"),
         ("Dirección:", self.direccion_var, "Ej: San José, Costa Rica"),
         ("Contraseña:", self.password_var, "Mínimo 4 caracteres")
         ]

    # Mostrar ID generado (solo lectura)
      id_label = ctk.CTkLabel(
         form_frame, 
         text="ID del Cliente (generado automáticamente):",
         font=ctk.CTkFont(size=14, weight="bold"),
         text_color=("blue", "lightblue")
         )
      id_label.pack(anchor="w", padx=20, pady=(15, 5))
    
    # Entry para ID (solo lectura)
      id_entry = ctk.CTkEntry(
         form_frame, 
         textvariable=self.id_cliente_var,
         height=35,
         font=ctk.CTkFont(size=10),
         state="readonly",
         text_color=("gray60", "gray40")
         )
      id_entry.pack(fill="x", padx=20, pady=(0, 10))

    # Crear campos editables
      for i, (label_text, var, placeholder) in enumerate(campos_editables):
        # Label
          label = ctk.CTkLabel(form_frame, text=label_text, font=ctk.CTkFont(size=14))
          label.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Entry
          show = "*" if "Contraseña" in label_text else None
          entry = ctk.CTkEntry(
             form_frame, 
             textvariable=var,
             height=35,
             font=ctk.CTkFont(size=12),
             placeholder_text=placeholder,
             show=show
          )
          entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Si es el primer campo, darle foco
          if i == 0:
             entry.focus()

    # Información sobre el ID
      info_frame = ctk.CTkFrame(form_frame)
      info_frame.pack(fill="x", padx=20, pady=15)
    
      info_label = ctk.CTkLabel(
         info_frame,
         text="💡 El ID único se genera automáticamente y garantiza que no haya duplicados.\nPodrás gestionar las tarjetas del cliente después de crearlo.",
         font=ctk.CTkFont(size=11),
         text_color=("gray60", "gray40"),
         wraplength=400
         )
      info_label.pack(pady=10)

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
      password = self.password_var.get().strip()
      id_cliente = self.id_cliente_var.get()  # Ya viene generado con UUID

    # Validaciones básicas
      errores = []

      if not nombre or len(nombre) < 2:
         errores.append("• El nombre debe tener al menos 2 caracteres")
    
      if not apellido or len(apellido) < 2:
         errores.append("• El apellido debe tener al menos 2 caracteres")
        
      if not telefono:
         errores.append("• El teléfono es obligatorio")
      elif len(telefono.replace(" ", "").replace("-", "")) < 8:
         errores.append("• El teléfono debe tener al menos 8 dígitos")

      if not correo:
         errores.append("• El correo es obligatorio")
      elif "@" not in correo or "." not in correo.split("@")[-1]:
         errores.append("• El formato del correo no es válido")

      if not direccion:
         errores.append("• La dirección es obligatoria")
        
      if not password or len(password) < 4:
         errores.append("• La contraseña debe tener al menos 4 caracteres")

    # Verificar correo duplicado (más importante que ID duplicado con UUID)
      for cliente in self.gestion_clientes.clientes:
          if cliente.correo.lower() == correo.lower():
             errores.append("• Ya existe un cliente con ese correo electrónico")
             break

    # Si hay errores, mostrarlos
      if errores:
         mensaje_error = "Por favor corrige los siguientes errores:\n\n" + "\n".join(errores)
         messagebox.showerror("Errores de validación", mensaje_error)
         return

    # Intentar registrar el cliente
      try:
         # Generar fecha de registro automáticamente
          from datetime import datetime
          fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Intentar registrar en el sistema
          if self.gestion_clientes.registrar_cliente(
              nombre=nombre,
              id=id_cliente,  # UUID generado automáticamente
              password=password,
              apellido=apellido, 
              telefono=telefono, 
              correo=correo,
              direccion_envio=direccion,
              fecha_registro=fecha_registro
              ):
             messagebox.showinfo(
                 "Cliente Registrado", 
                 f"Cliente {nombre} {apellido} registrado exitosamente!\n\n"
                 f"ID único: {id_cliente[:8]}...\n"
                 f"Correo: {correo}\n\n"
                 f"Ahora puedes gestionar sus tarjetas desde la lista de clientes."
                 )
             file.guardar_clientes(self.gestion_clientes.clientes)
            # Cerrar modal
             self.modal_cliente.destroy()
            
            # Actualizar la vista de clientes si está activa
             self.actualizar_lista_clientes()
            
          else:
            # Con UUID esto es muy improbable, pero por si acaso
               messagebox.showerror(
                 "Error de Registro", 
                 f"No se pudo registrar el cliente.\n"
                 f"Posible causa: Error en el sistema de almacenamiento."
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

    # Headers de la tabla - CORREGIDOS
        headers_frame = ctk.CTkFrame(self.lista_frame)
        headers_frame.pack(fill="x", padx=10, pady=(5, 15))

        headers = ["ID", "Nombre", "Apellido", "Teléfono", "Correo", "Fecha", "Acciones"]  # IDs más cortos
        header_widths = [80, 120, 120, 100, 180, 100, 120]  # ID más pequeño

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
        # Datos del cliente - ID FORMATEADo
            datos = [
              self.gestion_clientes.formatear_id(getattr(cliente, 'id_cliente', 'N/A')),  # ID ACORTADO
              getattr(cliente, 'nombre', 'N/A'),
              getattr(cliente, 'apellido', 'N/A'),
              getattr(cliente, 'telefono', 'N/A'),
              getattr(cliente, 'correo', 'N/A'),
              str(getattr(cliente, 'fecha_registro', 'N/A'))[:10],  # Solo la fecha
            ]
        
        # Mostrar datos en columnas
            for j, (dato, width) in enumerate(zip(datos, header_widths[:-1])):
            # Configuración especial para el ID
                 if j == 0:  # Columna ID
                   dato_label = ctk.CTkLabel(
                       cliente_frame,
                       text=str(dato),
                       font=ctk.CTkFont(size=10, family="monospace"),  # Fuente monospace más pequeña
                       width=width,
                       anchor="w",
                       text_color=("gray50", "gray60")  # Color más suave
                  )
                 else:
                     dato_label = ctk.CTkLabel(
                    cliente_frame,
                    text=str(dato),
                    font=ctk.CTkFont(size=11),
                    width=width,
                    anchor="w"
                  )
                 dato_label.grid(row=0, column=j, padx=5, pady=8, sticky="w")
        
        # Botones de acción - ORGANIZADOS CORRECTAMENTE
            acciones_frame = ctk.CTkFrame(cliente_frame)
            acciones_frame.grid(row=0, column=len(datos), padx=5, pady=5, sticky="e")
        
        # Configurar grid del frame de acciones
            acciones_frame.grid_columnconfigure(0, weight=1)
            acciones_frame.grid_columnconfigure(1, weight=1)
            acciones_frame.grid_columnconfigure(2, weight=1)
        
        # Botón Ver/Editar
            btn_ver = ctk.CTkButton(
                  acciones_frame, 
                  text="👁️",
                  width=30,
                  height=25,
                  command=lambda c=cliente: self.ver_cliente(c),
                  font=ctk.CTkFont(size=12),
                  fg_color=("blue", "darkblue"),
                  hover_color=("darkblue", "blue")
                 )
            btn_ver.grid(row=0, column=0, padx=2, pady=5)    
    
        # Botón Gestionar Tarjetas
            btn_tarjetas = ctk.CTkButton(
                acciones_frame,
                text="💳",
                width=30,
                height=25,
                command=lambda c=cliente: self.gestionar_tarjetas_cliente(c),
                font=ctk.CTkFont(size=12),
                fg_color=("green", "darkgreen"),
                hover_color=("darkgreen", "green")
                  )
            btn_tarjetas.grid(row=0, column=1, padx=2, pady=5)    
            
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
            btn_eliminar.grid(row=0, column=2, padx=2, pady=5)   

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
                if hasattr(self, 'gestion_tarjetas') and self.gestion_tarjetas.tarjetas is not None:
                   self.gestion_tarjetas.tarjetas = [
                      t for t in self.gestion_tarjetas.tarjetas
                      if t.id_usuario != cliente.id_cliente
                   ]
                   self.gestion_tarjetas.guardar_tarjetas()
                self.gestion_clientes.clientes.remove(cliente)
                self.gestion_clientes.guardar_clientes()
                messagebox.showinfo("Cliente Eliminado", f"Cliente {cliente.nombre} eliminado exitosamente")
                self.actualizar_lista_clientes()  # Refrescar la lista
                
    def buscar_cliente(self):
        """Abrir diálogo para buscar cliente"""
        # Verificar si ya hay una ventana de búsqueda abierta
        if hasattr(self, 'modal_busqueda') and self.modal_busqueda.winfo_exists():
            self.modal_busqueda.lift()  # Traer al frente
            self.modal_busqueda.focus()
            return

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

        # Limpiar variables previas de búsqueda
        self.limpiar_variables_busqueda()

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

        # Inicializar variables ANTES de crear la interfaz
        self.busqueda_var = ctk.StringVar()
        self.filtro_activo = ctk.BooleanVar(value=True)
        self.tipo_busqueda = ctk.StringVar(value="Todos los campos")

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
            placeholder_text="Escribe para buscar... (ej: Jose)"
            )
        self.entry_busqueda.pack(fill="x", padx=20, pady=(0, 15))

        # Frame para opciones de búsqueda
        options_frame = ctk.CTkFrame(search_frame)
        options_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Checkbox para mostrar solo activos
        checkbox_activos = ctk.CTkCheckBox(
            options_frame,
            text="Solo clientes activos",
            variable=self.filtro_activo
            )
        checkbox_activos.pack(side="left", padx=20, pady=10)

        # Selector de tipo de búsqueda
        tipo_label = ctk.CTkLabel(options_frame, text="Buscar en:")
        tipo_label.pack(side="left", padx=(40, 10), pady=10)

    
        tipo_menu = ctk.CTkOptionMenu(
            options_frame,
            values=["Todos los campos", "Solo nombre", "Solo ID", "Solo correo"],
            variable=self.tipo_busqueda
            )
        tipo_menu.pack(side="left", padx=10, pady=10)

        # Botones de acción 
        buttons_frame = ctk.CTkFrame(search_frame)
        buttons_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        btn_buscar_manual = ctk.CTkButton(
            buttons_frame,
            text="🔍 Buscar",
            command=self.ejecutar_busqueda,
            height=35,
            font=ctk.CTkFont(size=12, weight="bold")
            )
        btn_buscar_manual.pack(side="left", padx=20, pady=10)

        btn_limpiar = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar",
            command=self.limpiar_busqueda,
            height=35,
            width=100,
            fg_color=("gray70", "gray30")
            )
        btn_limpiar.pack(side="left", padx=10, pady=10)

        btn_mostrar_todos = ctk.CTkButton(
            buttons_frame,
            text="👥 Mostrar Todos",
            command=self.mostrar_todos_en_busqueda,
            height=35,
            width=120,
            fg_color=("green", "darkgreen")
            )
        btn_mostrar_todos.pack(side="left", padx=10, pady=10)

        # Frame para resultados
        results_label = ctk.CTkLabel(
            main_frame,
            text="Resultados de la búsqueda:",
            font=ctk.CTkFont(size=16, weight="bold")
            )
        results_label.pack(pady=(20, 10))

        # Frame scrollable para resultados - CREAR SIEMPRE
        self.resultados_frame = ctk.CTkScrollableFrame(main_frame, height=250)
        self.resultados_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Frame para botones inferiores
        bottom_buttons = ctk.CTkFrame(main_frame)
        bottom_buttons.pack(fill="x", padx=20, pady=10)

        btn_cerrar = ctk.CTkButton(
            bottom_buttons,
            text="❌ Cerrar",
            command=self.cerrar_busqueda,
            height=35,
            fg_color=("gray70", "gray30")
            )
        btn_cerrar.pack(side="right", padx=20, pady=10)

        # Inicializar con pantalla vacía - NO mostrar todos automáticamente
        self.mostrar_mensaje_inicial()

        # Configurar el evento de entrada DESPUÉS de crear todo
        self.entry_busqueda.bind('<KeyRelease>', self.on_busqueda_keyrelease)
        self.entry_busqueda.focus()
    def limpiar_variables_busqueda(self):
        """Limpiar variables de búsqueda previas"""
        if hasattr(self, 'busqueda_var'):
            del self.busqueda_var
        if hasattr(self, 'filtro_activo'):
            del self.filtro_activo
        if hasattr(self, 'tipo_busqueda'):
            del self.tipo_busqueda
        if hasattr(self, 'resultados_frame'):
            del self.resultados_frame
    def mostrar_mensaje_inicial(self):
        """Mostrar mensaje inicial en lugar de todos los clientes"""
        # Limpiar resultados
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        # Mostrar mensaje inicial
        mensaje_inicial = ctk.CTkLabel(
            self.resultados_frame,
            text="Escribe en el campo de búsqueda para encontrar clientes.\n\nO haz clic en 'Mostrar Todos' para ver todos los clientes registrados.",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
            )
        mensaje_inicial.pack(pady=50)     
    def on_busqueda_keyrelease(self, event):
        """Manejar evento cuando se escribe en el campo de búsqueda"""
        # Solo buscar si hay texto
        if self.busqueda_var.get().strip():
            self.ejecutar_busqueda()  
    def ejecutar_busqueda(self):
        """Ejecutar la búsqueda de clientes"""
        try:
            # Verificar que resultados_frame existe
            if not hasattr(self, 'resultados_frame') or not self.resultados_frame.winfo_exists():
                print("Error: resultados_frame no existe")
                return

            # Limpiar resultados anteriores
            for widget in self.resultados_frame.winfo_children():
                widget.destroy()
            
            # Verificar que hay clientes para buscar
            if not hasattr(self, 'gestion_clientes') or not self.gestion_clientes.clientes:
                no_results = ctk.CTkLabel(
                    self.resultados_frame,
                    text="No hay clientes registrados para buscar.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray60", "gray40")
                )
                no_results.pack(pady=30)
                return

            # Obtener término de búsqueda
            termino = self.busqueda_var.get().lower().strip()
            
            if not termino:
                self.mostrar_mensaje_inicial()
                return
                
            tipo = self.tipo_busqueda.get()
            
            # Filtrar clientes
            clientes_filtrados = []
            for cliente in self.gestion_clientes.clientes:
                # Determinar en qué campos buscar
                campos_busqueda = []
                if tipo == "Todos los campos":
                    campos_busqueda = [
                        getattr(cliente, 'nombre', '').lower(),
                        getattr(cliente, 'apellido', '').lower(),
                        getattr(cliente, 'id_cliente', '').lower(),
                        getattr(cliente, 'correo', '').lower(),
                        getattr(cliente, 'telefono', '').lower()
                    ]
                elif tipo == "Solo nombre":
                    campos_busqueda = [
                        getattr(cliente, 'nombre', '').lower(), 
                        getattr(cliente, 'apellido', '').lower()
                    ]
                elif tipo == "Solo ID":
                    campos_busqueda = [getattr(cliente, 'id_cliente', '').lower()]
                elif tipo == "Solo correo":
                    campos_busqueda = [getattr(cliente, 'correo', '').lower()]
                
                # Verificar si el término está en algún campo
                if any(termino in campo for campo in campos_busqueda if campo):
                    clientes_filtrados.append(cliente)
            
            # Mostrar resultados
            if not clientes_filtrados:
                no_results = ctk.CTkLabel(
                    self.resultados_frame,
                    text=f"No se encontraron clientes con '{termino}'.\nVerifica que el nombre esté escrito correctamente.",
                    font=ctk.CTkFont(size=14),
                    text_color=("orange", "orange")
                )
                no_results.pack(pady=30)
            else:
                self.mostrar_resultados_busqueda(clientes_filtrados)
            
        except Exception as e:
            print(f"Error en búsqueda: {e}") 
    def mostrar_todos_en_busqueda(self):
        """Mostrar todos los clientes en la búsqueda"""
        try:
            if not hasattr(self, 'gestion_clientes') or not self.gestion_clientes.clientes:
                self.mostrar_mensaje_inicial()
                return
                
            # Limpiar campo de búsqueda
            self.busqueda_var.set("")
            
            # Mostrar todos los clientes
            self.mostrar_resultados_busqueda(self.gestion_clientes.clientes)
            
        except Exception as e:
            print(f"Error mostrando todos los clientes: {e}")    
    def mostrar_resultados_busqueda(self, clientes_filtrados):
        """Mostrar la lista de clientes filtrados"""
        # Limpiar resultados
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
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
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("blue", "lightblue")
            )
        count_label.pack(pady=5)     
    def mostrar_cliente_resultado(self, cliente):
        """Mostrar un cliente en los resultados de búsqueda"""
        resultado_frame = ctk.CTkFrame(self.resultados_frame)
        resultado_frame.pack(fill="x", padx=10, pady=2)

        # Datos del cliente
        id_cliente = getattr(cliente, 'id_cliente', 'N/A')
        nombre = getattr(cliente, 'nombre', 'N/A')
        apellido = getattr(cliente, 'apellido', '')
        correo = getattr(cliente, 'correo', 'N/A')
        telefono = getattr(cliente, 'telefono', 'N/A')

        # Columnas de datos
        ctk.CTkLabel(resultado_frame, text=id_cliente, font=ctk.CTkFont(size=11), width=80).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(resultado_frame, text=f"{nombre} {apellido}".strip(), font=ctk.CTkFont(size=11, weight="bold"), width=150, text_color=("blue", "lightblue")).grid(row=0, column=1, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(resultado_frame, text=correo, font=ctk.CTkFont(size=11), width=180).grid(row=0, column=2, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(resultado_frame, text=telefono, font=ctk.CTkFont(size=11), width=100).grid(row=0, column=3, padx=10, pady=8, sticky="w")

        # Botones de acción
        acciones_frame = ctk.CTkFrame(resultado_frame)
        acciones_frame.grid(row=0, column=4, padx=10, pady=5)
        
        ctk.CTkButton(acciones_frame, text="👁️ Ver", width=60, height=25, command=lambda: self.ver_cliente(cliente), font=ctk.CTkFont(size=10)).pack(side="left", padx=2)
        ctk.CTkButton(acciones_frame, text="✅ Usar", width=60, height=25, command=lambda: self.seleccionar_cliente(cliente), font=ctk.CTkFont(size=10), fg_color=("green", "darkgreen")).pack(side="left", padx=2) 
    def seleccionar_cliente(self, cliente):
        """Seleccionar un cliente y cerrar la búsqueda"""
        from tkinter import messagebox
        
        messagebox.showinfo(
            "Cliente Seleccionado",
            f"Has seleccionado:\n\n"
            f"ID: {getattr(cliente, 'id_cliente', 'N/A')}\n"
            f"Nombre: {getattr(cliente, 'nombre', 'N/A')} {getattr(cliente, 'apellido', '')}\n"
            f"Correo: {getattr(cliente, 'correo', 'N/A')}\n"
            f"Teléfono: {getattr(cliente, 'telefono', 'N/A')}"
        )
        
        self.cerrar_busqueda() 
    def limpiar_busqueda(self):
        """Limpiar el campo de búsqueda"""
        self.busqueda_var.set("")
        self.tipo_busqueda.set("Todos los campos")
        self.filtro_activo.set(True)
        self.mostrar_mensaje_inicial()

    def cerrar_busqueda(self):
        """Cerrar la ventana de búsqueda correctamente"""
        if hasattr(self, 'modal_busqueda') and self.modal_busqueda.winfo_exists():
            self.modal_busqueda.destroy()
        
        # Limpiar variables
        self.limpiar_variables_busqueda()        

    def ver_cliente_desde_busqueda(self, cliente):
     """Ver detalles del cliente desde la búsqueda"""
     self.ver_cliente(cliente)  

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
     
    def gestionar_tarjetas_cliente(self, cliente):
      """Abrir interfaz para gestionar las tarjetas de un cliente"""
    # Crear ventana modal para gestión de tarjetas
      self.modal_tarjetas = ctk.CTkToplevel(self.root)
      self.modal_tarjetas.title(f"💳 Tarjetas de {cliente.nombre} {cliente.apellido}")
      self.modal_tarjetas.geometry("800x600")
      self.modal_tarjetas.transient(self.root)
      self.modal_tarjetas.grab_set()

    # Centrar ventana
      self.modal_tarjetas.update_idletasks()
      x = (self.modal_tarjetas.winfo_screenwidth() // 2) - 400
      y = (self.modal_tarjetas.winfo_screenheight() // 2) - 300
      self.modal_tarjetas.geometry(f"800x600+{x}+{y}")

    # Frame principal
      main_frame = ctk.CTkFrame(self.modal_tarjetas)
      main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
      title_label = ctk.CTkLabel(
          main_frame,
          text=f"Gestión de Tarjetas - {cliente.nombre} {cliente.apellido}",
          font=ctk.CTkFont(size=18, weight="bold")
         )
      title_label.pack(pady=(10, 20))

    # Info del cliente
      info_frame = ctk.CTkFrame(main_frame)
      info_frame.pack(fill="x", padx=10, pady=10)
    
      cliente_info = ctk.CTkLabel(
          info_frame,
          text=f"👤 {cliente.nombre} {cliente.apellido} | 🆔 {cliente.id_cliente[:8]}... | 📧 {cliente.correo}",
          font=ctk.CTkFont(size=12)
         )
      cliente_info.pack(pady=10)

    # Botón agregar tarjeta
      btn_agregar_tarjeta = ctk.CTkButton(
         main_frame,
         text="➕ Agregar Nueva Tarjeta",
        command=lambda: self.abrir_modal_nueva_tarjeta(cliente),
         height=40,
         font=ctk.CTkFont(size=14, weight="bold")
         )
      btn_agregar_tarjeta.pack(pady=10)

    # Frame para lista de tarjetas
      self.tarjetas_list_frame = ctk.CTkScrollableFrame(
         main_frame,
         label_text="Tarjetas Registradas"
         )
      self.tarjetas_list_frame.pack(fill="both", expand=True, padx=10, pady=20)

    # Cargar tarjetas del cliente
      self.cargar_tarjetas_cliente(cliente)

    # Botón cerrar
      btn_cerrar = ctk.CTkButton(
         main_frame,
         text="❌ Cerrar",
         command=self.modal_tarjetas.destroy,
         height=35,
         fg_color=("gray70", "gray30")
         )
      btn_cerrar.pack(pady=10)
    def cargar_tarjetas_cliente(self, cliente):
      """Cargar y mostrar las tarjetas del cliente"""
    # Limpiar frame
      for widget in self.tarjetas_list_frame.winfo_children():
         widget.destroy()

    # Buscar tarjetas del cliente usando el gestor de tarjetas
      tarjetas_cliente = []
      if hasattr(self, 'gestion_tarjetas'):
         tarjetas_cliente = [
             t for t in self.gestion_tarjetas.tarjetas 
             if t.id_usuario == cliente.id_cliente
             ]    

      if not tarjetas_cliente:
         no_cards_label = ctk.CTkLabel(
             self.tarjetas_list_frame,
             text="💳 Este cliente no tiene tarjetas registradas.\nHaz clic en 'Agregar Nueva Tarjeta' para comenzar.",
              font=ctk.CTkFont(size=14),
             text_color=("gray60", "gray40")
            )
         no_cards_label.pack(pady=50)
         return

    # Mostrar cada tarjeta
      for i, tarjeta in enumerate(tarjetas_cliente):
         self.crear_tarjeta_visual(tarjeta, i + 1) 
    def crear_tarjeta_visual(self, tarjeta, numero_tarjeta):
      """Crear representación visual de una tarjeta"""
    # Frame de la tarjeta
      card_frame = ctk.CTkFrame(self.tarjetas_list_frame)
      card_frame.pack(fill="x", padx=10, pady=10)

    # Frame de información
      info_frame = ctk.CTkFrame(card_frame)
      info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

    # Número de tarjeta (solo últimos 4 dígitos)
      numero_label = ctk.CTkLabel(
         info_frame,
         text=f"💳 Tarjeta #{numero_tarjeta} - **** **** **** {tarjeta.numero_tarjeta[-4:]}",
         font=ctk.CTkFont(size=16, weight="bold"),
         text_color=("blue", "lightblue")
         )
      numero_label.pack(anchor="w", padx=10, pady=(10, 5))

    # Banco
      banco_label = ctk.CTkLabel(
         info_frame,
         text=f"🏛️ Banco: {tarjeta.banco}",
         font=ctk.CTkFont(size=14)
         )
      banco_label.pack(anchor="w", padx=10, pady=2)

    # CVV (oculto)
      cvv_label = ctk.CTkLabel(
         info_frame,
         text="🔒 CVV: ***",
         font=ctk.CTkFont(size=12),
         text_color=("gray60", "gray40")
         )
      cvv_label.pack(anchor="w", padx=10, pady=(2, 10))

    # Botones
      buttons_frame = ctk.CTkFrame(card_frame)
      buttons_frame.pack(side="right", fill="y", padx=15, pady=15)

    #Boton recargar tarjeta
      btn_recargar = ctk.CTkButton(
         buttons_frame,
         text="💳 Recargar",
         command=lambda t=tarjeta: self.abrir_modal_recarga(t),
         height=35,
         fg_color=("blue", "lightblue")
      )
      btn_recargar.pack(pady=5)

      btn_ver_tarjeta = ctk.CTkButton(
          buttons_frame,
          text="Ver Tarjeta",
          command=lambda: self.ver_detalles_de_tarjeta(tarjeta),
          fg_color=("orange")
        )
      btn_ver_tarjeta.pack(pady=15)

    # Botón eliminar tarjeta
      btn_eliminar = ctk.CTkButton(
        buttons_frame,
        text="🗑️ Eliminar",
        command=lambda t=tarjeta: self.confirmar_eliminar_tarjeta(t),
        width=100,
        height=35,
        fg_color=("red", "darkred")
        )
      btn_eliminar.pack(pady=5)  


    def abrir_modal_recarga(self, tarjeta):
    # Crear ventana modal
      modal = ctk.CTkToplevel(self.root)
      modal.title("Recargar Tarjeta")
      modal.geometry("400x400")
      modal.resizable(False, False)
    
      modal.grab_set()
    # Título
      titulo = ctk.CTkLabel(modal, text="💳 Recargar Tarjeta", 
                         font=ctk.CTkFont(size=20, weight="bold"))
      titulo.pack(pady=20)
    
    # Mostrar info de la tarjeta
      info_tarjeta = ctk.CTkLabel(modal, text=f"Tarjeta: **** {tarjeta.numero_tarjeta[-4:]}")
      info_tarjeta.pack(pady=5)
    
      saldo_actual = ctk.CTkLabel(modal, text=f"Saldo actual: ${tarjeta.saldo}", 
                               font=ctk.CTkFont(size=16))
      saldo_actual.pack(pady=10)
    
    # Frame para los botones de recarga
      botones_frame = ctk.CTkFrame(modal)
      botones_frame.pack(pady=20, padx=30, fill="x")
    
    # Los 4 botones de recarga
      montos = [200, 400, 800, 1000]
      colores = [("green", "lightgreen"), ("blue", "lightblue"), 
               ("orange", "lightyellow"), ("purple", "lightpink")]
    
      for i, monto in enumerate(montos):
          btn = ctk.CTkButton(
              botones_frame,
              text=f"Recargar ${monto}",
              command=lambda m=monto: self.realizar_recarga(tarjeta, m, modal, saldo_actual),
              height=40,
              fg_color=colores[i],
              font=ctk.CTkFont(size=14)
            )
          btn.pack(pady=8, padx=20, fill="x")
    
    # Botón cerrar
      btn_cerrar = ctk.CTkButton(modal, text="Cerrar", 
                              command=modal.destroy,
                              fg_color=("gray", "darkgray"))
      btn_cerrar.pack(pady=20) 
    

    def abrir_modal_nueva_tarjeta(self, cliente):
      """Abrir modal para agregar nueva tarjeta"""
      modal_nueva_tarjeta = ctk.CTkToplevel(self.modal_tarjetas)
      modal_nueva_tarjeta.title("➕ Nueva Tarjeta")
      modal_nueva_tarjeta.geometry("500x450")
      modal_nueva_tarjeta.transient(self.modal_tarjetas)
      modal_nueva_tarjeta.grab_set()

    # Centrar ventana
      modal_nueva_tarjeta.update_idletasks()
      x = (modal_nueva_tarjeta.winfo_screenwidth() // 2) - 250
      y = (modal_nueva_tarjeta.winfo_screenheight() // 2) - 225
      modal_nueva_tarjeta.geometry(f"500x450+{x}+{y}")

    # Frame principal
      main_frame = ctk.CTkFrame(modal_nueva_tarjeta)
      main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
      title_label = ctk.CTkLabel(
         main_frame,
         text=f"Agregar Tarjeta para {cliente.nombre}",
         font=ctk.CTkFont(size=18, weight="bold")
         )
      title_label.pack(pady=(10, 30))

    # Variables
      numero_var = ctk.StringVar()
      cvv_var = ctk.StringVar()
      banco_var = ctk.StringVar(value="Banco Nacional")

    # Campos del formulario
    # Número de tarjeta
      numero_label = ctk.CTkLabel(main_frame, text="Número de Tarjeta:", font=ctk.CTkFont(size=14))
      numero_label.pack(anchor="w", padx=20, pady=(15, 5))

      numero_entry = ctk.CTkEntry(
         main_frame,
         textvariable=numero_var,
         height=35,
         font=ctk.CTkFont(size=12),
         placeholder_text="1234567812345678 (15 o 16 dígitos)"
         )
      numero_entry.pack(fill="x", padx=20, pady=(0, 10))
      numero_entry.focus()

    # CVV
      cvv_label = ctk.CTkLabel(main_frame, text="Código de Seguridad (CVV):", font=ctk.CTkFont(size=14))
      cvv_label.pack(anchor="w", padx=20, pady=(15, 5))

      cvv_entry = ctk.CTkEntry(
         main_frame,
         textvariable=cvv_var,
         height=35,
         font=ctk.CTkFont(size=12),
         placeholder_text="123 (3 dígitos)",
         show="*"
         )
      cvv_entry.pack(fill="x", padx=20, pady=(0, 10))

    # Banco
      banco_label = ctk.CTkLabel(main_frame, text="Banco Emisor:", font=ctk.CTkFont(size=14))
      banco_label.pack(anchor="w", padx=20, pady=(15, 5))

      banco_menu = ctk.CTkOptionMenu(
         main_frame,
         values=["Banco Nacional", "Banco de Costa Rica", "BAC San José", "Scotiabank", "Banco Popular", "Davivienda", "Otro"],
         variable=banco_var,
         height=35
         )
      banco_menu.pack(fill="x", padx=20, pady=(0, 15))

    # Información de seguridad
      info_frame = ctk.CTkFrame(main_frame)
      info_frame.pack(fill="x", padx=20, pady=10)

      info_label = ctk.CTkLabel(
         info_frame,
         text="🔒 La información de la tarjeta se almacena de forma segura.\nSolo se mostrarán los últimos 4 dígitos para identificación.",
         font=ctk.CTkFont(size=11),
         text_color=("gray60", "gray40"),
         wraplength=400
         )
      info_label.pack(pady=10)

    # Botones
      buttons_frame = ctk.CTkFrame(main_frame)
      buttons_frame.pack(fill="x", padx=20, pady=20)

      btn_cancelar = ctk.CTkButton(
         buttons_frame,
         text="❌ Cancelar",
         command=modal_nueva_tarjeta.destroy,
         height=40,
         fg_color=("gray70", "gray30")
         )
      btn_cancelar.pack(side="right", padx=(10, 20), pady=15)

      btn_guardar = ctk.CTkButton(
         buttons_frame,
         text="💾 Guardar Tarjeta",
         command=lambda: self.guardar_nueva_tarjeta(
             modal_nueva_tarjeta, cliente, numero_var.get(), cvv_var.get(), banco_var.get()
            ),
          height=40,
          font=ctk.CTkFont(size=14, weight="bold")
            )
      btn_guardar.pack(side="right", padx=20, pady=15)

    def ver_detalles_de_tarjeta(self, tarjeta):
        modal = ctk.CTkToplevel()
        modal.title("Detalles de Tarjeta")
        modal.geometry("300x200")
        modal.resizable(False, False)

        modal.grab_set()
        modal.focus_force()
        modal.lift()
        modal.attributes("-topmost", True)
        modal.after(100, lambda: modal.attributes("-topmost", False))

    # Título
        ctk.CTkLabel(
            modal, 
            text="Detalles de la Tarjeta", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=15)

    # Banco
        ctk.CTkLabel(modal, text=f"Banco: {tarjeta.banco}").pack(pady=5)

    # 🔥 Label del saldo (lo guardamos en una variable)
        saldo_label = ctk.CTkLabel(modal, text=f"Saldo: ${tarjeta.saldo}")
        saldo_label.pack(pady=5)

    # Botón actualizar saldo (opcional)
        ctk.CTkButton(
            modal, 
            text="Actualizar Saldo", 
            command=lambda: saldo_label.configure(text=f"Saldo: ${tarjeta.saldo}")
        ).pack(pady=10)

    # Botón cerrar
        ctk.CTkButton(modal, text="Cerrar", command=modal.destroy).pack(pady=10)

    def guardar_nueva_tarjeta(self, modal, cliente, numero, cvv, banco):
      """Guardar nueva tarjeta para el cliente"""
   
      numero = numero.strip().replace(" ", "").replace("-", "")
      cvv = cvv.strip()
      banco = banco.strip()

    # Validaciones
      errores = []
      
      if not numero or not numero.isdigit():
         errores.append("• El número de tarjeta debe contener solo dígitos")
      elif len(numero) not in [15, 16]:
         errores.append("• El número de tarjeta debe tener 15 o 16 dígitos")

      if not cvv or not cvv.isdigit() or len(cvv) != 3:
         errores.append("• El CVV debe ser un número de 3 dígitos")

      if not banco:
         errores.append("• Debe seleccionar un banco")   

    # Verificar si la tarjeta ya existe
      if hasattr(self, 'gestion_tarjetas'):
          for tarjeta in self.gestion_tarjetas.tarjetas:
              if tarjeta.numero_tarjeta == numero:
                  errores.append("• Esta tarjeta ya está registrada en el sistema")
                  break

      if errores:
         mensaje_error = "Por favor corrige los siguientes errores:\n\n" + "\n".join(errores)
         messagebox.showerror("Errores de validación", mensaje_error)
         return

      try:
        # Registrar la tarjeta usando el gestor
          if hasattr(self, 'gestion_tarjetas'):
             resultado = self.gestion_tarjetas.registrar_tarjeta(
                 id_usuario=cliente.id_cliente,
                 numero=numero,
                 codigo=cvv,
                 banco=banco
                 )

             if resultado:
                 messagebox.showinfo(
                     "Tarjeta Agregada",
                     f"Tarjeta terminada en {numero[-4:]} agregada exitosamente!\n\n"
                     f"Banco: {banco}\n"
                     f"Cliente: {cliente.nombre} {cliente.apellido}"
                 )
                 
                 modal.destroy()
                 self.cargar_tarjetas_cliente(cliente)  # Refrescar lista
                 file.guardar_tarjetas(self.gestion_tarjetas.tarjetas)
             else:
                 messagebox.showerror("Error", "No se pudo agregar la tarjeta")
          else:
             messagebox.showerror("Error", "Sistema de tarjetas no disponible")

      except Exception as e:
        messagebox.showerror("Error", f"Error al agregar tarjeta: {str(e)}")

    def realizar_recarga(self, tarjeta, monto, modal, label_saldo):
        exito, mensaje = self.gestion_tarjetas.recargar_tarjeta(tarjeta, monto)
        if exito:
            messagebox.showinfo("Recarga Exitosa", mensaje)
            label_saldo.configure(text=f"Saldo: ${tarjeta.saldo}")
        else:
            messagebox.showerror("Error", mensaje)
          

    def confirmar_eliminar_tarjeta(self, tarjeta):
      """Confirmar eliminación de tarjeta"""
      respuesta = messagebox.askyesno(
         "Confirmar Eliminación",
         f"¿Estás seguro de que deseas eliminar esta tarjeta?\n\n"
         f"Tarjeta: **** **** **** {tarjeta.numero_tarjeta[-4:]}\n"
         f"Banco: {tarjeta.banco}\n\n"
         f"Esta acción no se puede deshacer."
         )

      if respuesta:
          try:
              if hasattr(self, 'gestion_tarjetas'):
                  resultado = self.gestion_tarjetas.eliminar_tarjeta(
                     tarjeta.id_usuario,
                     tarjeta.numero_tarjeta,
                     tarjeta.codigo,
                     tarjeta.saldo
                     )

                  if resultado:
                     messagebox.showinfo("Tarjeta Eliminada", "Tarjeta eliminada exitosamente")
                     # Buscar el cliente para refrescar la lista
                     cliente = next(
                         (c for c in self.gestion_clientes.clientes if c.id_cliente == tarjeta.id_usuario),
                         None
                         )
                     if cliente:
                        self.cargar_tarjetas_cliente(cliente)
                  else:
                     messagebox.showerror("Error", "No se pudo eliminar la tarjeta")
              else:
                 messagebox.showerror("Error", "Sistema de tarjetas no disponible")

          except Exception as e:
             messagebox.showerror("Error", f"Error al eliminar tarjeta: {str(e)}")
    def procesar_pago(self):
          """Procesar el pago del carrito actual"""

          # Obtener cliente seleccionado del dropdown
          cliente_seleccionado_texto = self.cliente_compra_var.get()
          print(f"DEBUG - Texto seleccionado: {cliente_seleccionado_texto}")

          # Buscar el objeto cliente completo
          self.usuario_actual = next(
            (c for c in self.gestion_clientes.clientes
            if f"{c.nombre} {c.apellido} ({c.id_cliente})" == cliente_seleccionado_texto),
            None
          )

                
          print(f"DEBUG - Usuario encontrado: {self.usuario_actual}")

          # Verificar que hay un cliente seleccionado
          if not self.usuario_actual:
              messagebox.showerror("Error", "Debe seleccionar un cliente válido")
              return

          # Verificar que el carrito no está vacío
          if not self.carrito or not self.carrito.items:
              messagebox.showinfo("Pago", "El carrito está vacío.")
              return
          
          # Pedir datos al usuario
          numero = simpledialog.askstring("Pago", "Ingrese número de tarjeta:")
          if not numero:
              return

          cvv = simpledialog.askstring("Pago", "Ingrese CVV:")
          if not cvv:
              return

          password = simpledialog.askstring("Pago", "Ingrese su contraseña:")
          if not password:
              return

          if self.usuario_actual.password != password:
            return "Contraseña incorrecta. Pago cancelado."
          
          try:
              # Crear procesador de pago
              procesador = ProcesarPago(self.carrito, self.gestion_tarjetas, self.registros)

              # Procesar pago
              resultado = procesador.procesar_pago(
                  self.usuario_actual,  # cliente obtenido del dropdown
                  numero,
                  cvv,
                  password
              )

              print(f"DEBUG - Resultado del pago: {resultado}")

              # Si el pago fue exitoso (verificar si contiene símbolo de éxito)
              if "✅" in resultado or "exitoso" in resultado.lower():
                  # Eliminar productos del inventario solo si el pago fue exitoso
                  for item in self.carrito.items:
                      nodo = next(
                          (n for n in self.inventario.pasar_a_lista_nodos(self.inventario)
                           if n.dato.nombre == item["nombre"]),
                          None
                      )
                      if nodo:
                          for _ in range(item["cantidad"]):
                              if nodo.pila.items:
                                  nodo.pila.items.pop()
                  registro = Registro(
                     cliente = self.usuario_actual,
                     total = self.carrito.calcular_total(),
                     metodoDePago="Tarjeta",
                     estado = "Exitoso"
                  )
                  self.registros.lista_registros.append(registro)
                  file.guardar_registros(self.registros)
                  
                  # Resetear carrito
                  self.carrito = None
                  self.actualizar_carrito_vista()
                  self.cargar_productos_en_interfaz()
                  
              # Mostrar resultado del pago
              if "❌" in resultado or "error" in resultado.lower():
                  messagebox.showerror("Error de pago", resultado)
              else:
                  messagebox.showinfo("Pago", resultado)

          except Exception as e:
              print(f"DEBUG - Excepción: {str(e)}")
              messagebox.showerror("Error de pago", f"Error inesperado: {str(e)}")
    def calcular_ventas_hoy(self):
      """Calcular las ventas del día actual basándose en los registros"""
      from datetime import datetime
    
      fecha_hoy = datetime.now().strftime("%Y-%m-%d")
      total_ventas_hoy = 0.0
    
    # Verificar que existen registros
      if hasattr(self.registros, 'lista_registros') and self.registros.lista_registros:
         for registro in self.registros.lista_registros:
             # Verificar que el registro tiene los atributos necesarios
             if hasattr(registro, 'fecha') and hasattr(registro, 'total') and hasattr(registro, 'estado'):
                 # Comprobar si es del día de hoy y si fue exitoso
                 registro_fecha = str(registro.fecha)
                 if fecha_hoy in registro_fecha and registro.estado.lower() == "exitoso":
                    total_ventas_hoy += registro.total
    
      return total_ventas_hoy 

    def salir_aplicacion(self):
        """Confirmar y salir de la aplicación"""
        if messagebox.askyesno("Confirmar Salida", "¿Estás seguro de que deseas salir?"):
            self.gestion_tarjetas.reiniciar_limites_recarga()
            inventario = ListaInventario()
            articulos_para_guardar = []
            actual = inventario.primero
            while actual:
               art = actual.dato
               art.cantidad = len(actual.pila.items)
               articulos_para_guardar.append(art)
               actual = actual.siguiente

            self.clientes = self.gestion_clientes.clientes
            self.tarjetas = self.gestion_tarjetas.tarjetas
            file.guardar_datos(
               self.clientes,
               self.tarjetas,
               articulos_para_guardar,
               self.registros.lista_registros,
            )

            self.root.quit()
            self.root.destroy()
        
    def ejecutar(self):
      """Ejecutar la aplicación"""
      (self.clientes,
      self.tarjetas,
      self.articulos,
      self.registros) = file.cargar_datos()

      inventario = ListaInventario()
      for articulo in self.articulos:
          inventario.agregar_articulo(articulo)

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


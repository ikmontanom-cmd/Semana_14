import tkinter as tk
from tkinter import messagebox, ttk

from ui.iconos import iconos


class MainView(tk.Frame):
    def __init__(self, master, restaurante_servicio, usuario_actual, al_cerrar_sesion):
        super().__init__(master, bg="#f7fafc")
        self.restaurante_servicio = restaurante_servicio
        self.usuario_actual = usuario_actual
        self.al_cerrar_sesion = al_cerrar_sesion

        # Contenedores y componentes que se reutilizan en la vista.
        self.contenido = None
        self.etiqueta_estado = None
        self.etiqueta_mensaje = None
        self.tabla_productos = None
        self.variables_formulario = {}

        self.definir_estilos()
        self.construir_interfaz()

    # ------------------------------------------------------------------ estilos
    def definir_estilos(self):
        # Define colores y estilos reutilizables de esta vista.
        self.color_fondo = "#f7fafc"
        self.color_encabezado = "#7c2d12"
        self.color_texto = "#243447"
        self.color_secundario = "#ffedd5"
        self.color_resaltado = "#ea580c"

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "MenuApp.TButton",
            background=self.color_secundario,
            foreground=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("MenuApp.TButton", background=[("active", "#fed7aa")])

        estilo.configure(
            "CerrarSesion.TButton",
            background="#e11d48",
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(12, 8),
            borderwidth=0,
        )
        estilo.map("CerrarSesion.TButton", background=[("active", "#be123c")])

        # Estilos de los botones de accion del formulario de productos.
        acciones = {
            "Registrar.TButton": ("#16a34a", "#15803d"),
            "Consultar.TButton": ("#0284c7", "#0369a1"),
            "Actualizar.TButton": ("#ea580c", "#c2410c"),
            "Eliminar.TButton": ("#e11d48", "#be123c"),
            "Limpiar.TButton": ("#64748b", "#475569"),
        }

        for nombre, (color, color_activo) in acciones.items():
            estilo.configure(
                nombre,
                background=color,
                foreground="#ffffff",
                font=("Arial", 10, "bold"),
                padding=(10, 7),
                borderwidth=0,
            )
            estilo.map(nombre, background=[("active", color_activo)])

        estilo.configure(
            "Tabla.Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground=self.color_texto,
            rowheight=26,
            font=("Arial", 10),
            borderwidth=0,
        )
        estilo.configure(
            "Tabla.Treeview.Heading",
            background=self.color_encabezado,
            foreground="#ffffff",
            font=("Arial", 10, "bold"),
            padding=(6, 6),
        )
        estilo.map(
            "Tabla.Treeview",
            background=[("selected", self.color_resaltado)],
            foreground=[("selected", "#ffffff")],
        )

    # -------------------------------------------------------------- estructura
    def construir_interfaz(self):
        # Construye los contenedores principales de la pantalla.
        self.crear_encabezado()
        self.crear_barra_navegacion()
        self.crear_barra_estado()

        self.contenido = tk.Frame(self, bg=self.color_fondo, padx=24, pady=20)
        self.contenido.pack(fill="both", expand=True)

        self.mostrar_inicio()

    def crear_encabezado(self):
        # Contenedor superior con el logotipo y el usuario conectado.
        encabezado = tk.Frame(self, bg=self.color_encabezado, padx=28, pady=16)
        encabezado.pack(fill="x")

        logo = iconos.obtener("logo")
        if logo is not None:
            tk.Label(encabezado, image=logo, bg=self.color_encabezado).pack(
                side="left", padx=(0, 16)
            )

        textos = tk.Frame(encabezado, bg=self.color_encabezado)
        textos.pack(side="left", fill="x", expand=True)

        tk.Label(
            textos,
            text="RESTAURANTE",
            bg=self.color_encabezado,
            fg="#ffffff",
            font=("Arial", 19, "bold"),
        ).pack(anchor="w")

        tk.Label(
            textos,
            text=f"Bienvenido, {self.usuario_actual.nombre}",
            bg=self.color_encabezado,
            fg="#ffedd5",
            font=("Arial", 11),
        ).pack(anchor="w", pady=(4, 0))

    def crear_barra_navegacion(self):
        # Contenedor de navegacion entre las secciones del sistema.
        barra = tk.Frame(self, bg=self.color_secundario, padx=18, pady=10)
        barra.pack(fill="x")

        self.crear_boton_menu(barra, "Inicio", self.mostrar_inicio, "inicio")
        self.crear_boton_menu(barra, "Productos", self.mostrar_productos, "productos")
        self.crear_boton_menu(barra, "Usuarios", self.mostrar_usuarios, "usuarios")

        ttk.Button(
            barra,
            text=" Cerrar sesion",
            image=iconos.obtener("salir"),
            compound="left",
            command=self.cerrar_sesion,
            style="CerrarSesion.TButton",
        ).pack(side="right")

    def crear_boton_menu(self, contenedor, texto, comando, nombre_icono=None):
        # Agrega una opcion visual con icono en la barra superior.
        ttk.Button(
            contenedor,
            text=f" {texto}",
            image=iconos.obtener(nombre_icono) if nombre_icono else "",
            compound="left",
            command=comando,
            style="MenuApp.TButton",
        ).pack(side="left", padx=(0, 6))

    def crear_barra_estado(self):
        # Contenedor inferior con el resumen general del sistema.
        barra_estado = tk.Frame(self, bg=self.color_secundario, padx=18, pady=8)
        barra_estado.pack(fill="x", side="bottom")

        self.etiqueta_estado = tk.Label(
            barra_estado,
            text="",
            bg=self.color_secundario,
            fg=self.color_texto,
            font=("Arial", 10),
        )
        self.etiqueta_estado.pack(side="left")

        self.actualizar_barra_estado()

    def actualizar_barra_estado(self):
        # Refresca los contadores despues de cada operacion.
        if self.etiqueta_estado is None:
            return

        self.etiqueta_estado.config(
            text=(
                f"Productos: {self.restaurante_servicio.cantidad_productos()} | "
                f"Usuarios: {self.restaurante_servicio.cantidad_usuarios()} | "
                "Datos JSON locales"
            )
        )

    def limpiar_contenido(self):
        # Limpia el area central antes de mostrar una nueva seccion.
        assert self.contenido is not None

        for widget in self.contenido.winfo_children():
            widget.destroy()

        self.tabla_productos = None
        self.etiqueta_mensaje = None
        self.variables_formulario = {}

    def crear_titulo_seccion(self, texto, nombre_icono=None):
        # Presenta el titulo de la seccion seleccionada con su icono.
        assert self.contenido is not None

        tk.Label(
            self.contenido,
            text=f"  {texto}",
            image=iconos.obtener(nombre_icono) if nombre_icono else "",
            compound="left",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 17, "bold"),
        ).pack(anchor="w", pady=(0, 14))

    # ------------------------------------------------------------------ inicio
    def mostrar_inicio(self):
        # Muestra el estado inicial de la interfaz principal.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Panel principal", "inicio")

        tarjetas = tk.Frame(self.contenido, bg=self.color_fondo)
        tarjetas.pack(fill="x")

        self.crear_tarjeta(
            tarjetas,
            "Productos",
            self.restaurante_servicio.cantidad_productos(),
            "productos",
        )
        self.crear_tarjeta(
            tarjetas,
            "Usuarios",
            self.restaurante_servicio.cantidad_usuarios(),
            "usuarios",
        )

        tk.Label(
            self.contenido,
            text=(
                "Seleccione una opcion de la barra superior. En la seccion Productos "
                "puede registrar, consultar, actualizar y eliminar registros."
            ),
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 11),
            wraplength=640,
            justify="left",
        ).pack(anchor="w", pady=(18, 0))

    def crear_tarjeta(self, contenedor, titulo, valor, nombre_icono):
        # Tarjeta informativa construida con un contenedor propio.
        tarjeta = tk.Frame(contenedor, bg="#ffffff", padx=18, pady=14)
        tarjeta.pack(side="left", padx=(0, 14))

        icono = iconos.obtener(nombre_icono)
        if icono is not None:
            tk.Label(tarjeta, image=icono, bg="#ffffff").pack(side="left", padx=(0, 12))

        textos = tk.Frame(tarjeta, bg="#ffffff")
        textos.pack(side="left")

        tk.Label(
            textos,
            text=str(valor),
            bg="#ffffff",
            fg=self.color_resaltado,
            font=("Arial", 20, "bold"),
        ).pack(anchor="w")

        tk.Label(
            textos,
            text=titulo,
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10),
        ).pack(anchor="w")

    # --------------------------------------------------------------- productos
    def mostrar_productos(self):
        # Construye el formulario, las acciones y la tabla de productos.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Gestion de productos", "productos")

        self.crear_formulario_productos(self.contenido)
        self.crear_acciones_productos(self.contenido)
        self.crear_mensaje_productos(self.contenido)
        self.crear_tabla_productos(self.contenido)

        self.refrescar_tabla_productos()

    def crear_formulario_productos(self, contenedor):
        # Contenedor de captura de datos organizado con grid.
        formulario = tk.LabelFrame(
            contenedor,
            text=" Datos del producto ",
            bg="#ffffff",
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=16,
            pady=14,
            bd=1,
            relief="solid",
        )
        formulario.pack(fill="x")

        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        self.variables_formulario = {
            "codigo": tk.StringVar(),
            "nombre": tk.StringVar(),
            "precio": tk.StringVar(),
            "categoria": tk.StringVar(),
        }

        self.crear_campo(formulario, "Codigo", "codigo", 0, 0)
        self.crear_campo(formulario, "Nombre", "nombre", 0, 2)
        self.crear_campo(formulario, "Precio", "precio", 1, 0)

        tk.Label(
            formulario,
            text="Categoria",
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=2, sticky="w", padx=(0, 10), pady=6)

        combo = ttk.Combobox(
            formulario,
            textvariable=self.variables_formulario["categoria"],
            values=self.restaurante_servicio.categorias_disponibles(),
            state="readonly",
            font=("Arial", 10),
        )
        combo.grid(row=1, column=3, sticky="ew", pady=6)

    def crear_campo(self, contenedor, etiqueta, clave, fila, columna):
        # Crea una etiqueta y su entrada dentro del formulario.
        tk.Label(
            contenedor,
            text=etiqueta,
            bg="#ffffff",
            fg=self.color_texto,
            font=("Arial", 10, "bold"),
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 10), pady=6)

        entrada = tk.Entry(
            contenedor,
            textvariable=self.variables_formulario[clave],
            font=("Arial", 10),
            relief="solid",
            bd=1,
        )
        entrada.grid(row=fila, column=columna + 1, sticky="ew", pady=6, ipady=3)

    def crear_acciones_productos(self, contenedor):
        # Contenedor con los botones de accion mediante command=.
        acciones = tk.Frame(contenedor, bg=self.color_fondo, pady=12)
        acciones.pack(fill="x")

        botones = [
            ("Registrar", self.registrar_producto, "Registrar.TButton", "agregar"),
            ("Consultar", self.consultar_producto, "Consultar.TButton", "buscar"),
            ("Actualizar", self.actualizar_producto, "Actualizar.TButton", "actualizar"),
            ("Eliminar", self.eliminar_producto, "Eliminar.TButton", "eliminar"),
            ("Limpiar", self.limpiar_formulario, "Limpiar.TButton", "limpiar"),
        ]

        for texto, comando, estilo, nombre_icono in botones:
            ttk.Button(
                acciones,
                text=f" {texto}",
                image=iconos.obtener(nombre_icono),
                compound="left",
                command=comando,
                style=estilo,
            ).pack(side="left", padx=(0, 8))

    def crear_mensaje_productos(self, contenedor):
        # Area donde se informa el resultado de cada operacion.
        self.etiqueta_mensaje = tk.Label(
            contenedor,
            text="Complete el formulario y utilice los botones de accion.",
            bg=self.color_fondo,
            fg=self.color_texto,
            font=("Arial", 10),
            anchor="w",
        )
        self.etiqueta_mensaje.pack(fill="x", pady=(0, 10))

    def crear_tabla_productos(self, contenedor):
        # Contenedor de visualizacion con tabla y barra de desplazamiento.
        marco_tabla = tk.LabelFrame(
            contenedor,
            text=" Productos registrados ",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bd=1,
            relief="solid",
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "precio", "categoria")
        self.tabla_productos = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Tabla.Treeview",
            height=6,
        )

        titulos = {
            "codigo": ("Codigo", 90, "w"),
            "nombre": ("Nombre", 230, "w"),
            "precio": ("Precio", 90, "e"),
            "categoria": ("Categoria", 150, "w"),
        }

        for columna in columnas:
            titulo, ancho, alineacion = titulos[columna]
            self.tabla_productos.heading(columna, text=titulo)
            self.tabla_productos.column(columna, width=ancho, anchor=alineacion)

        barra_scroll = ttk.Scrollbar(
            marco_tabla, orient="vertical", command=self.tabla_productos.yview
        )
        self.tabla_productos.configure(yscrollcommand=barra_scroll.set)

        self.tabla_productos.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

    def refrescar_tabla_productos(self):
        # Vuelve a cargar la tabla con la informacion entregada por el servicio.
        if self.tabla_productos is None:
            return

        for fila in self.tabla_productos.get_children():
            self.tabla_productos.delete(fila)

        for producto in self.restaurante_servicio.listar_productos():
            self.tabla_productos.insert(
                "",
                "end",
                values=(
                    producto.codigo,
                    producto.nombre,
                    f"${producto.precio:.2f}",
                    producto.categoria,
                ),
            )

        self.actualizar_barra_estado()

    # ---------------------------------------------------- acciones de productos
    def leer_formulario(self):
        # Obtiene los valores escritos por el usuario en el formulario.
        return {
            clave: variable.get().strip()
            for clave, variable in self.variables_formulario.items()
        }

    def escribir_formulario(self, producto):
        # Carga en el formulario los datos de un producto consultado.
        self.variables_formulario["codigo"].set(producto.codigo)
        self.variables_formulario["nombre"].set(producto.nombre)
        self.variables_formulario["precio"].set(f"{producto.precio:.2f}")
        self.variables_formulario["categoria"].set(producto.categoria)

    def limpiar_formulario(self):
        # Deja el formulario en blanco para un nuevo registro.
        for variable in self.variables_formulario.values():
            variable.set("")

        self.mostrar_mensaje("Formulario limpio.")

    def mostrar_mensaje(self, texto, es_error=False):
        # Informa el resultado de la operacion dentro de la misma pantalla.
        if self.etiqueta_mensaje is None:
            return

        self.etiqueta_mensaje.config(
            text=texto,
            fg="#b42318" if es_error else "#15803d",
        )

    def registrar_producto(self):
        # Solicita el registro al servicio y actualiza la interfaz.
        datos = self.leer_formulario()

        try:
            producto = self.restaurante_servicio.registrar_producto(
                datos["codigo"], datos["nombre"], datos["precio"], datos["categoria"]
            )
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.mostrar_mensaje(f"Producto {producto.codigo} registrado correctamente.")

    def consultar_producto(self):
        # Carga en el formulario el producto solicitado por su codigo.
        datos = self.leer_formulario()

        try:
            producto = self.restaurante_servicio.obtener_producto(datos["codigo"])
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.escribir_formulario(producto)
        self.mostrar_mensaje(f"Producto {producto.codigo} cargado en el formulario.")

    def actualizar_producto(self):
        # Solicita la actualizacion al servicio y refresca la tabla.
        datos = self.leer_formulario()

        try:
            producto = self.restaurante_servicio.actualizar_producto(
                datos["codigo"], datos["nombre"], datos["precio"], datos["categoria"]
            )
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.refrescar_tabla_productos()
        self.mostrar_mensaje(f"Producto {producto.codigo} actualizado correctamente.")

    def eliminar_producto(self):
        # Confirma la accion y delega la eliminacion al servicio.
        datos = self.leer_formulario()

        if not datos["codigo"]:
            self.mostrar_mensaje("Ingrese el codigo del producto.", es_error=True)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            f"Desea eliminar el producto {datos['codigo']}?",
        )

        if not confirmar:
            return

        try:
            producto = self.restaurante_servicio.eliminar_producto(datos["codigo"])
        except ValueError as error:
            self.mostrar_mensaje(str(error), es_error=True)
            return

        self.refrescar_tabla_productos()
        self.limpiar_formulario()
        self.mostrar_mensaje(f"Producto {producto.codigo} eliminado.")

    # ---------------------------------------------------------------- usuarios
    def mostrar_usuarios(self):
        # Consulta los usuarios registrados y los muestra en una tabla.
        self.limpiar_contenido()

        assert self.contenido is not None

        self.crear_titulo_seccion("Usuarios registrados", "usuarios")

        marco_tabla = tk.LabelFrame(
            self.contenido,
            text=" Consulta de usuarios ",
            bg=self.color_fondo,
            fg=self.color_encabezado,
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10,
            bd=1,
            relief="solid",
        )
        marco_tabla.pack(fill="both", expand=True)

        columnas = ("identificador", "nombre", "usuario")
        tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Tabla.Treeview",
            height=8,
        )

        titulos = {
            "identificador": ("Identificador", 130),
            "nombre": ("Nombre", 240),
            "usuario": ("Usuario", 180),
        }

        for columna in columnas:
            titulo, ancho = titulos[columna]
            tabla.heading(columna, text=titulo)
            tabla.column(columna, width=ancho, anchor="w")

        barra_scroll = ttk.Scrollbar(
            marco_tabla, orient="vertical", command=tabla.yview
        )
        tabla.configure(yscrollcommand=barra_scroll.set)

        tabla.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")

        for usuario in self.restaurante_servicio.listar_usuarios():
            tabla.insert(
                "",
                "end",
                values=(usuario.identificador, usuario.nombre, usuario.usuario),
            )

    # ------------------------------------------------------------------- otros
    def cerrar_sesion(self):
        # Regresa al login sin crear otra ventana ni otro mainloop.
        self.al_cerrar_sesion()

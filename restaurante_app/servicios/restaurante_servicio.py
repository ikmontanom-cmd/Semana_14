from modelos.producto import Producto
from modelos.usuario import Usuario


class RestauranteServicio:
    ARCHIVO_PRODUCTOS = "productos.json"
    CATEGORIAS = ["Entradas", "Platos fuertes", "Bebidas", "Postres"]

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.cargar_datos()

    def cargar_datos(self):
        # Carga los datos persistidos y los convierte en objetos.
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", datos.get("contrasena", "")),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", ""),
                datos.get("nombre", ""),
                datos.get("precio", 0),
                datos.get("categoria", ""),
            )
            for datos in productos_json
        ]

    def validar_acceso(self, usuario, contrasena):
        # Verifica si las credenciales coinciden con un usuario cargado.
        for usuario_registrado in self.usuarios:
            if (
                usuario_registrado.usuario == usuario
                and usuario_registrado.contrasena == contrasena
            ):
                return usuario_registrado

        return None

    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def listar_usuarios(self):
        # Entrega los usuarios cargados para mostrarlos en la interfaz.
        return self.usuarios

    def listar_productos(self):
        # Entrega los productos cargados para mostrarlos en la interfaz.
        return self.productos

    def categorias_disponibles(self):
        # Entrega las categorias permitidas para el formulario de productos.
        categorias = list(self.CATEGORIAS)

        for producto in self.productos:
            if producto.categoria not in categorias:
                categorias.append(producto.categoria)

        return categorias

    def buscar_producto(self, codigo):
        # Busca un producto por su codigo y devuelve None si no existe.
        codigo = str(codigo).strip().upper()

        for producto in self.productos:
            if producto.codigo.upper() == codigo:
                return producto

        return None

    def obtener_producto(self, codigo):
        # Devuelve el producto solicitado o informa que no existe.
        if not str(codigo).strip():
            raise ValueError("Ingrese el codigo del producto.")

        producto = self.buscar_producto(codigo)

        if producto is None:
            raise ValueError(f"No existe un producto con el codigo {codigo}.")

        return producto

    def registrar_producto(self, codigo, nombre, precio, categoria):
        # Valida los datos, crea el producto y guarda los cambios.
        producto = Producto(codigo, nombre, precio, categoria)

        if self.buscar_producto(producto.codigo) is not None:
            raise ValueError(f"El codigo {producto.codigo} ya esta registrado.")

        self.productos.append(producto)
        self.guardar_productos()

        return producto

    def actualizar_producto(self, codigo, nombre, precio, categoria):
        # Modifica los datos de un producto existente y persiste el cambio.
        producto = self.obtener_producto(codigo)

        producto.nombre = nombre
        producto.precio = precio
        producto.categoria = categoria

        self.guardar_productos()

        return producto

    def eliminar_producto(self, codigo):
        # Quita un producto de la lista y actualiza el archivo JSON.
        producto = self.obtener_producto(codigo)

        self.productos.remove(producto)
        self.guardar_productos()

        return producto

    def guardar_productos(self):
        # Delega la escritura del archivo JSON al servicio de archivos.
        datos = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio,
                "categoria": producto.categoria,
            }
            for producto in self.productos
        ]

        self.archivo_servicio.escribir_json(self.ARCHIVO_PRODUCTOS, datos)

# restaurante_app

## Propósito (Semana 14 — Componentes y contenedores)

`restaurante_app` es la aplicación de escritorio en **Tkinter** del proyecto de
la asignatura. Sobre la base gráfica construida en la Semana 13 (arquitectura
modular con modelos, servicios, vistas y `main.py`), esta versión de la
**Semana 14** evoluciona la capa de interfaz aplicando **componentes,
contenedores y gestores de geometría**.

La pantalla principal se reorganiza en contenedores claramente diferenciados
(encabezado, barra de navegación, formulario, acciones, tabla y barra de
estado) y la sección de Productos permite ahora **registrar, consultar,
actualizar y eliminar** registros desde la interfaz, mediante botones con
`command=`. Las validaciones y reglas de negocio se mantienen dentro de
`RestauranteServicio`, y la persistencia sigue realizándose en
`datos/productos.json` a través de `ArchivoServicio`.

## Estructura de carpetas y archivos

```
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── iconos.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── actualizar.png
│   ├── agregar.png
│   ├── app_icon.png
│   ├── buscar.png
│   ├── campo_clave.png
│   ├── campo_usuario.png
│   ├── ingresar.png
│   ├── eliminar.png
│   ├── inicio.png
│   ├── limpiar.png
│   ├── logo.png
│   ├── productos.png
│   ├── salir.png
│   └── usuarios.png
├── main.py
└── README.md
```

- **modelos/**: representan las entidades del dominio.
  - `Producto`: código, nombre, precio y categoría, con validaciones básicas
    (campos obligatorios y precio numérico no negativo).
  - `Usuario`: identificador, nombre, usuario y contraseña, usado para la
    simulación de acceso.
- **servicios/**:
  - `ArchivoServicio`: única responsabilidad de leer y escribir los archivos
    JSON en `datos/`.
  - `RestauranteServicio`: carga los datos vía `ArchivoServicio`, los convierte
    en objetos `Producto`/`Usuario` y expone las operaciones que necesitan las
    vistas: `validar_acceso`, `listar_usuarios`, `listar_productos`,
    `cantidad_usuarios`, `cantidad_productos`, `categorias_disponibles`,
    `buscar_producto`, `obtener_producto`, `registrar_producto`,
    `actualizar_producto`, `eliminar_producto` y `guardar_productos`. Las
    vistas nunca leen ni escriben los JSON directamente.
- **ui/**:
  - `LoginView`: pantalla de acceso simulada (usuario, contraseña, mensaje de
    error, botón de ingreso).
  - `MainView`: panel principal con navegación entre "Inicio", "Productos"
    (formulario, acciones y tabla) y "Usuarios" (consulta en tabla).
- **main.py**: crea la única ventana de Tkinter, prepara `ArchivoServicio` y
  `RestauranteServicio`, y controla el cambio entre `LoginView` y `MainView`
  dentro de la misma ventana (sin abrir ventanas ni `mainloop()` adicionales).

## Flujo de la aplicación

```
Inicio de la aplicación
        ↓
main.py prepara Tkinter y los servicios
        ↓
LoginView
        ↓
Ingreso de usuario y contraseña
        ↓
RestauranteServicio valida el acceso
        ↓
MainView
        ↓
Navegación: Inicio | Productos | Usuarios
        ↓
Usuarios → consulta en tabla (Treeview)
        ↓
Productos → formulario + acciones + tabla
        ↓
Registrar | Consultar | Actualizar | Eliminar | Limpiar
        ↓
RestauranteServicio valida y procesa la operación
        ↓
Persistencia en datos/productos.json (ArchivoServicio)
        ↓
Actualización de la tabla y de la barra de estado
        ↓
Cerrar sesión
        ↓
LoginView
```

## Nota sobre las contraseñas

Como en el proyecto docente, esta es una simulación con fines didácticos: las
contraseñas se guardan en texto plano en `usuarios.json` únicamente para poder
practicar la arquitectura de la aplicación. En un sistema real, la contraseña
jamás se transmite ni se almacena tal cual: se guarda un *hash* (una huella
digital irreversible) generado a partir de ella, y la validación se hace
comparando hashes, nunca contraseñas en claro.

## Usuarios de prueba

| Usuario  | Contraseña |
|----------|------------|
| admin    | 1234       |
| mesero   | abcd       |

## Cómo ejecutar

1. Ubicarse en la carpeta raíz del proyecto (`restaurante_app/`).
2. Ejecutar:

   ```bash
   python main.py
   ```

3. Se abrirá la pantalla de acceso. Ingresar un usuario y contraseña válidos
   (ver tabla anterior).
4. Tras un acceso correcto se mostrará el panel principal, donde se puede:
   - Ver el resumen en **Inicio** (tarjetas con la cantidad de productos y
     usuarios registrados).
   - Gestionar **Productos**: completar el formulario y usar los botones
     *Registrar*, *Consultar*, *Actualizar*, *Eliminar* y *Limpiar*; los
     cambios se guardan en `datos/productos.json` y se reflejan en la tabla.
   - Consultar los **Usuarios** cargados desde `datos/usuarios.json`.
5. El botón **Cerrar sesión** regresa a la pantalla de login dentro de la
   misma ventana.

## Iconos (carpeta `assets/`)

La carpeta `assets/` contiene los recursos visuales del proyecto en formato PNG
con fondo transparente. Se cargan mediante `ui/iconos.py`, que expone la clase
`GestorIconos` y la instancia compartida `iconos`:

- `iconos.obtener("productos")` devuelve un `tk.PhotoImage` ya cargado.
- Las imágenes se guardan en un diccionario interno para conservar la
  referencia y evitar que Tkinter las elimine de memoria.
- Si un archivo no existe, el método devuelve `None` y la interfaz se muestra
  igualmente solo con texto.

Uso dentro de la interfaz:

| Icono | Uso |
|-------|-----|
| `logo.png` | Logotipo en el login y en el encabezado principal |
| `app_icon.png` | Icono de la ventana (`iconphoto`) |
| `campo_usuario.png`, `campo_clave.png` | Etiquetas de los campos del login |
| `ingresar.png` | Botón "Iniciar sesión" |
| `productos.png`, `usuarios.png` | Botones del menú, títulos de sección y filas de información |
| `inicio.png` | Botón "Inicio" del menú y título del panel principal |
| `agregar.png`, `buscar.png`, `actualizar.png`, `eliminar.png`, `limpiar.png` | Botones de acción del formulario de productos |
| `salir.png` | Botón "Cerrar sesión" |

Los iconos se combinan con el texto mediante `compound="left"`, por lo que no
alteran la lógica del proyecto ni la separación de responsabilidades.

## Componentes y contenedores utilizados

**Contenedores**

| Contenedor | Uso |
|------------|-----|
| `tk.Frame` | Encabezado, barra de navegación, área de contenido, barra de estado, fila de botones y tarjetas del panel principal |
| `tk.LabelFrame` | Agrupa el formulario "Datos del producto" y las tablas de productos y usuarios |
| `tk.Frame` como vista | `LoginView` y `MainView` heredan de `Frame` y se intercambian dentro de la misma ventana |

**Componentes**

| Componente | Uso |
|------------|-----|
| `tk.Label` | Títulos de sección, etiquetas del formulario, mensajes de resultado y contadores |
| `tk.Entry` | Captura de código, nombre y precio (asociados a `StringVar`) |
| `ttk.Combobox` | Selección de la categoría del producto (`state="readonly"`) |
| `ttk.Button` | Navegación y acciones sobre productos mediante `command=` |
| `ttk.Treeview` | Tabla de productos y tabla de usuarios |
| `ttk.Scrollbar` | Desplazamiento vertical de las tablas |
| `ttk.Style` | Estilos de botones y tablas (colores, tipografía, `padding`) |
| `messagebox` | Confirmación de eliminación y aviso de sección pendiente |

**Gestores de geometría**

- `pack()`: organiza los contenedores principales de arriba hacia abajo
  (encabezado, navegación, contenido, barra de estado) y la fila de botones
  (`side="left"`).
- `grid()`: organiza el formulario de productos en filas y columnas, con
  `columnconfigure(..., weight=1)` para que los campos se expandan.
- `place()`: centra la tarjeta de acceso en `LoginView`.

## Operaciones implementadas sobre productos

Todas se ejecutan desde la interfaz con `command=` y se delegan al servicio:

| Botón | Método de la vista | Método del servicio |
|-------|--------------------|---------------------|
| Registrar | `registrar_producto()` | `RestauranteServicio.registrar_producto()` |
| Consultar | `consultar_producto()` | `RestauranteServicio.obtener_producto()` |
| Actualizar | `actualizar_producto()` | `RestauranteServicio.actualizar_producto()` |
| Eliminar | `eliminar_producto()` | `RestauranteServicio.eliminar_producto()` |
| Limpiar | `limpiar_formulario()` | (solo interfaz) |

Validaciones que permanecen en el dominio y en el servicio:

- Campos obligatorios y precio numérico no negativo (`Producto`).
- Código no duplicado al registrar y código existente al consultar, actualizar
  o eliminar (`RestauranteServicio`).
- Los errores se devuelven como `ValueError` y la vista solo los muestra en la
  etiqueta de mensajes; la interfaz nunca accede a los archivos JSON.

## Persistencia

Cada operación que modifica la lista de productos llama a
`RestauranteServicio.guardar_productos()`, que convierte los objetos `Producto`
en diccionarios y solicita la escritura a `ArchivoServicio.escribir_json()`
sobre `datos/productos.json`. Por eso los cambios se conservan al cerrar y
volver a ejecutar `main.py`.

## Mejoras de interfaz de esta semana

- Encabezado con logotipo, barra de navegación con iconos y barra de estado con
  contadores que se actualizan tras cada operación.
- Panel principal con tarjetas de resumen de productos y usuarios.
- Formulario de productos organizado con `grid()` dentro de un `LabelFrame`.
- Botones de acción diferenciados por color e icono.
- Tablas `Treeview` con encabezados y barra de desplazamiento en lugar de filas
  de texto.
- Mensajes de resultado en pantalla (verde para éxito, rojo para error).

## Alcance de esta etapa

No se implementan: manejo avanzado de eventos con `bind()`, doble clic, eventos
de teclado o mouse, edición directa sobre la tabla, módulo de ventas, bases
de datos ni autenticación real. Estas funcionalidades se incorporarán en las
siguientes semanas sobre esta misma base estructural, de acuerdo con el
alcance definido para la Semana 14 (Componentes y contenedores).

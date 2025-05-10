import flet as ft


def main(page: ft.Page):
    # Configuración básica de la página
    page.title = "ola"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#e9f7fa"  # Fondo azul claro

    # Formulario para agregar productos
    def add_producto(e):
        # Aquí es donde agregarías el código para agregar el producto a la base de datos
        print(
            f"Agregar Producto: {id_producto.value}, {nombre_producto.value}, {descripcion.value}, {precio.value}, {unidad.value}, {stock.value}")

        # Limpiar los campos después de agregar
        id_producto.value = ""
        nombre_producto.value = ""
        descripcion.value = ""
        precio.value = ""
        unidad.value = ""
        stock.value = ""
        page.update()

    # Campos de entrada para los productos con un estilo moderno
    id_producto = ft.TextField(
        label="ID Producto",
        width=320,
        border_color="#00bcd4",  # Color de borde personalizado
        color="#00796b",  # Color del texto
        border_radius=12,  # Bordes redondeados
    )
    nombre_producto = ft.TextField(
        label="Nombre del Producto",
        width=320,
        border_color="#00bcd4",
        color="#00796b",
        border_radius=12,
    )
    descripcion = ft.TextField(
        label="Descripción",
        multiline=True,
        width=320,
        border_color="#00bcd4",
        color="#00796b",
        border_radius=12,
    )
    precio = ft.TextField(
        label="Precio",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=320,
        border_color="#00bcd4",
        color="#00796b",
        border_radius=12,
    )
    unidad = ft.Dropdown(
        label="Unidad",
        options=[ft.dropdown.Option("Pieza"), ft.dropdown.Option("Paquete"), ft.dropdown.Option("Caja")],
        width=320,
        border_color="#00bcd4",
        color="#00796b",
        border_radius=12,
    )
    stock = ft.TextField(
        label="Stock",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=320,
        border_color="#00bcd4",
        color="#00796b",
        border_radius=12,
    )

    # Botón para agregar producto sin border_radius
    btn_add_producto = ft.ElevatedButton(
        "Agregar Producto",
        on_click=add_producto,
        width=320,
        bgcolor="#00796b",  # Fondo del botón
        color="white",  # Color del texto del botón
    )

    # Estructura del formulario de productos con espaciado y más márgenes
    producto_form = ft.Column(
        [
            ft.Text("Agregar Producto", size=24, weight=ft.FontWeight.BOLD, color="#00796b"),
            id_producto,
            nombre_producto,
            descripcion,
            precio,
            unidad,
            stock,
            btn_add_producto
        ],
        spacing=15,  # Más espaciado entre los elementos
        horizontal_alignment=ft.CrossAxisAlignment.CENTER  # Centramos los elementos
    )

    # Envuelve el formulario en un Container con márgenes
    container = ft.Container(
        content=producto_form,
        margin=ft.Margin(top=20, bottom=20, left=20, right=20)  # Márgenes completos alrededor del formulario
    )

    # Añadir el formulario de productos a la página
    page.add(container)
    page.update()


ft.app(target=main)

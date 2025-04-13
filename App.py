import flet as ft
from db.Database import DBConnection as DB


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "K'lux Papelería"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.bgcolor = "#f2f2f2"

        self.boton_activo = None
        self.main_content_column = None

        # Categoría
        self.txt_id_categoria = None
        self.txt_nombre_categoria = None
        self.txt_descripcion_categoria = None
        self.btn_guardar_categoria = None
        self.categoria_editando = None  # Variable para almacenar el ID de la categoría que se está editando

        # Proveedor
        self.txt_id_proveedor = None
        self.txt_nombre_proveedor = None
        self.txt_telefono_proveedor = None
        self.txt_direccion_proveedor = None
        self.btn_guardar_proveedor = None
        self.proveedor_editando = None  # Variable para almacenar el ID del proveedor que se está editando

        self.build_ui()

    def seleccionar_opcion(self, boton, seccion):
        if self.boton_activo:
            self.boton_activo.style = ft.ButtonStyle(color=ft.colors.BLACK)
            self.boton_activo.update()

        boton.style = ft.ButtonStyle(color=ft.colors.BLUE)
        boton.update()
        self.boton_activo = boton

        self.main_content_column.controls.clear()

        secciones = {
            "inicio": self.render_inicio,
            "productos": self.render_productos,
            "categoria": self.render_categoria,
            "proveedor": self.render_proveedor,
        }

        if seccion in secciones:
            self.main_content_column.controls.extend(secciones[seccion]())

        self.page.update()

    def build_ui(self):
        btn_inicio = ft.TextButton("🏠 Inicio", on_click=lambda e: self.seleccionar_opcion(btn_inicio, "inicio"))
        btn_productos = ft.TextButton("📦 Productos", on_click=lambda e: self.seleccionar_opcion(btn_productos, "productos"))
        btn_categoria = ft.TextButton("📂 Categoría", on_click=lambda e: self.seleccionar_opcion(btn_categoria, "categoria"))
        btn_proveedor = ft.TextButton("🚚 Proveedor", on_click=lambda e: self.seleccionar_opcion(btn_proveedor, "proveedor"))

        sidebar = ft.Container(
            width=200,
            bgcolor='#ffffff',
            padding=10,
            content=ft.Column(
                controls=[ft.Text("🧾 K'lux Papelería", size=18, weight="bold"),
                          ft.Divider(),
                          btn_inicio,
                          btn_productos,
                          btn_categoria,
                          btn_proveedor],
                spacing=10,
                alignment="start"
            )
        )

        self.main_content_column = ft.Column()

        main_content = ft.Container(
            expand=True,
            bgcolor="#ffffff",
            padding=20,
            content=self.main_content_column
        )

        layout = ft.Row(
            controls=[sidebar, main_content],
            expand=True
        )

        self.page.add(layout)
        self.seleccionar_opcion(btn_inicio, "inicio")

    def render_inicio(self):
        return [
            ft.Text("Inicio", size=22, weight="bold"),
            ft.Text("Bienvenido al sistema POS.")
        ]

    def render_productos(self):
        productos = self.obtener_productos()

        # Campos de entrada para los productos
        self.txt_id_producto = ft.TextField(label="ID de Producto", bgcolor="#ffffff", width=400, filled=True)
        self.txt_nombre_producto = ft.TextField(label="Nombre", width=400, bgcolor="#ffffff", filled=True)
        self.txt_descripcion_producto = ft.TextField(label="Descripción", bgcolor="#ffffff", width=400, multiline=True,
                                                     min_lines=2, max_lines=4, filled=True)
        self.txt_precio_producto = ft.TextField(label="Precio", width=400, bgcolor="#ffffff", filled=True)
        self.txt_stock_producto = ft.TextField(label="Stock", width=400, bgcolor="#ffffff", filled=True)
        self.txt_unidad_producto = ft.TextField(label="Unidad (pieza, paquete, etc.)", width=400, bgcolor="#ffffff",
                                                filled=True)
        self.txt_categoria_producto = ft.TextField(label="ID de Categoría", width=400, bgcolor="#ffffff", filled=True)
        self.txt_proveedor_producto = ft.TextField(label="ID de Proveedor", width=400, bgcolor="#ffffff", filled=True)

        self.btn_guardar_producto = ft.ElevatedButton(
            "Guardar",
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            on_click=self.guardar_producto,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        if not productos:
            lista_productos = ft.Text("Aún no hay productos añadidos.", italic=True, color=ft.colors.GREY)
        else:
            lista_productos = ft.DataTable(
                columns=[
                    ft.DataColumn(label=ft.Text("ID")),
                    ft.DataColumn(label=ft.Text("Nombre")),
                    ft.DataColumn(label=ft.Text("Descripción")),
                    ft.DataColumn(label=ft.Text("Precio")),
                    ft.DataColumn(label=ft.Text("Stock")),
                    ft.DataColumn(label=ft.Text("Unidad")),
                    ft.DataColumn(label=ft.Text("Acciones")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(prod[0]))),
                            ft.DataCell(ft.Text(prod[1])),
                            ft.DataCell(ft.Text(prod[2])),
                            ft.DataCell(ft.Text(str(prod[3]))),
                            ft.DataCell(ft.Text(str(prod[4]))),
                            ft.DataCell(ft.Text(prod[5])),
                            ft.DataCell(
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            tooltip="Editar",
                                            icon_color=ft.colors.BLUE,
                                            on_click=lambda e, prod_id=prod[0]: self.editar_producto(prod_id)
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="Eliminar",
                                            icon_color=ft.colors.RED,
                                            on_click=lambda e, prod_id=prod[0]: self.eliminar_producto(prod_id)
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                    for prod in productos
                ]
            )

        return [
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        padding=20,
                        bgcolor="#fafafa",
                        border_radius=10,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                ft.Text("Agregar nuevo producto", size=18, weight="bold"),
                                self.txt_id_producto,
                                self.txt_nombre_producto,
                                self.txt_descripcion_producto,
                                self.txt_precio_producto,
                                self.txt_stock_producto,
                                self.txt_unidad_producto,
                                self.txt_categoria_producto,
                                self.txt_proveedor_producto,
                                ft.Row(
                                    controls=[self.btn_guardar_producto],
                                    alignment="end"
                                )
                            ]
                        )
                    )
                ),
                margin=10
            ),
            ft.Text("Productos existentes", size=18, weight="bold"),
            lista_productos
        ]

    def guardar_producto(self, e):
        id_text = self.txt_id_producto.value
        nombre = self.txt_nombre_producto.value
        descripcion = self.txt_descripcion_producto.value
        precio_text = self.txt_precio_producto.value
        stock_text = self.txt_stock_producto.value
        unidad = self.txt_unidad_producto.value
        id_categoria_text = self.txt_categoria_producto.value
        id_proveedor_text = self.txt_proveedor_producto.value

        if not id_text or not nombre or not descripcion or not precio_text or not stock_text or not unidad or not id_categoria_text or not id_proveedor_text:
            self.page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            id_producto = int(id_text)
            precio = float(precio_text)
            stock = int(stock_text)
            id_categoria = int(id_categoria_text)
            id_proveedor = int(id_proveedor_text)
        except ValueError:
            self.page.snack_bar = ft.SnackBar(
                ft.Text("El ID debe ser un número entero, y el precio, stock, categoría y proveedor números válidos"),
                bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()

        try:
            if self.producto_editando is not None:
                cursor.execute(
                    "UPDATE producto SET nombre = %s, descripcion = %s, precio = %s, stock = %s, unidad = %s, idCategoria = %s, idProveedor = %s WHERE idProducto = %s",
                    (nombre, descripcion, precio, stock, unidad, id_categoria, id_proveedor, self.producto_editando)
                )
                self.page.snack_bar = ft.SnackBar(ft.Text("Producto actualizado correctamente"),
                                                  bgcolor=ft.colors.GREEN)
                self.btn_guardar_producto.text = "Guardar"
                self.btn_guardar_producto.icon = ft.icons.SAVE
                self.producto_editando = None
            else:
                cursor.execute(
                    "INSERT INTO producto (idProducto, nombre, descripcion, precio, stock, unidad, idCategoria, idProveedor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (id_producto, nombre, descripcion, precio, stock, unidad, id_categoria, id_proveedor)
                )
                self.page.snack_bar = ft.SnackBar(ft.Text("Producto guardado correctamente"), bgcolor=ft.colors.GREEN)

            conexion.commit()
            self.txt_id_producto.value = ""
            self.txt_nombre_producto.value = ""
            self.txt_descripcion_producto.value = ""
            self.txt_precio_producto.value = ""
            self.txt_stock_producto.value = ""
            self.txt_unidad_producto.value = ""
            self.txt_categoria_producto.value = ""
            self.txt_proveedor_producto.value = ""

        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"), bgcolor=ft.colors.RED)

        finally:
            self.page.snack_bar.open = True
            self.page.update()
            self.seleccionar_opcion(self.boton_activo, "productos")

    def obtener_productos(self):
        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT idProducto, nombre, descripcion, precio, stock, unidad FROM producto")
        productos = cursor.fetchall()
        cursor.close()
        conexion.close()
        return productos

    def editar_producto(self, producto_id):
        productos = self.obtener_productos()
        producto = next((prod for prod in productos if prod[0] == producto_id), None)

        if producto:
            self.txt_id_producto.value = str(producto[0])
            self.txt_nombre_producto.value = producto[1]
            self.txt_descripcion_producto.value = producto[2]
            self.txt_precio_producto.value = str(producto[3])
            self.txt_stock_producto.value = str(producto[4])
            self.txt_unidad_producto.value = producto[5]
            self.btn_guardar_producto.text = "Editar"
            self.btn_guardar_producto.icon = ft.icons.EDIT
            self.producto_editando = producto_id
            self.page.update()

    def eliminar_producto(self, producto_id):
        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM producto WHERE idProducto = %s", (producto_id,))
        conexion.commit()
        conexion.close()

        self.page.snack_bar = ft.SnackBar(ft.Text("Producto eliminado correctamente"), bgcolor=ft.colors.GREEN)
        self.page.snack_bar.open = True
        self.page.update()
        self.seleccionar_opcion(self.boton_activo, "productos")

    def render_categoria(self):
        categorias = self.obtener_categorias()

        self.txt_id_categoria = ft.TextField(label="ID de Categoría", bgcolor="#ffffff", width=400, filled=True)
        self.txt_nombre_categoria = ft.TextField(label="Nombre", width=400, bgcolor="#ffffff", filled=True)
        self.txt_descripcion_categoria = ft.TextField(label="Descripción", bgcolor="#ffffff", width=400, multiline=True,
                                                      min_lines=2, max_lines=4, filled=True)

        self.btn_guardar_categoria = ft.ElevatedButton(
            "Guardar",
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            on_click=self.guardar_categoria,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        if not categorias:
            lista_categorias = ft.Text("Aún no hay categorías añadidas.", italic=True, color=ft.colors.GREY)
        else:
            lista_categorias = ft.DataTable(
                columns=[
                    ft.DataColumn(label=ft.Text("ID")),
                    ft.DataColumn(label=ft.Text("Nombre")),
                    ft.DataColumn(label=ft.Text("Descripción")),
                    ft.DataColumn(label=ft.Text("Acciones")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cat[0]))),
                            ft.DataCell(ft.Text(cat[1])),
                            ft.DataCell(ft.Text(cat[2])),
                            ft.DataCell(
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            tooltip="Editar",
                                            icon_color=ft.colors.BLUE,
                                            on_click=lambda e, cat_id=cat[0]: self.editar_categoria(cat_id)
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="Eliminar",
                                            icon_color=ft.colors.RED,
                                            on_click=lambda e, cat_id=cat[0]: self.eliminar_categoria(cat_id)
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                    for cat in categorias
                ]
            )

        return [
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        padding=20,
                        bgcolor="#fafafa",
                        border_radius=10,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                ft.Text("Agregar nueva categoría", size=18, weight="bold"),
                                self.txt_id_categoria,
                                self.txt_nombre_categoria,
                                self.txt_descripcion_categoria,
                                ft.Row(
                                    controls=[self.btn_guardar_categoria],
                                    alignment="end"
                                )
                            ]
                        )
                    )
                ),
                margin=10
            ),
            ft.Text("Categorías existentes", size=18, weight="bold"),
            lista_categorias
        ]

    def guardar_categoria(self, e):
        id_text = self.txt_id_categoria.value
        nombre = self.txt_nombre_categoria.value
        descripcion = self.txt_descripcion_categoria.value

        if not id_text or not nombre or not descripcion:
            self.page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            id_categoria = int(id_text)
        except ValueError:
            self.page.snack_bar = ft.SnackBar(ft.Text("El ID debe ser un número entero"), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()

        try:
            if self.categoria_editando is not None:
                cursor.execute(
                    "UPDATE categoria SET nombre = %s, descripcion = %s WHERE idCategoria = %s",
                    (nombre, descripcion, self.categoria_editando)
                )
                self.page.snack_bar = ft.SnackBar(ft.Text("Categoría actualizada correctamente"), bgcolor=ft.colors.GREEN)
                self.btn_guardar_categoria.text = "Guardar"
                self.btn_guardar_categoria.icon = ft.icons.SAVE
                self.categoria_editando = None
            else:
                cursor.execute(
                    "INSERT INTO categoria (idCategoria, nombre, descripcion) VALUES (%s, %s, %s)",
                    (id_categoria, nombre, descripcion)
                )
                self.page.snack_bar = ft.SnackBar(ft.Text("Categoría guardada correctamente"), bgcolor=ft.colors.GREEN)

            conexion.commit()
            self.txt_id_categoria.value = ""
            self.txt_nombre_categoria.value = ""
            self.txt_descripcion_categoria.value = ""

        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"), bgcolor=ft.colors.RED)

        finally:
            self.page.snack_bar.open = True
            self.page.update()
            self.seleccionar_opcion(self.boton_activo, "categoria")

    def obtener_categorias(self):
        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT idCategoria, nombre, descripcion FROM categoria")
        categorias = cursor.fetchall()
        cursor.close()
        conexion.close()
        return categorias

    def editar_categoria(self, categoria_id):
        categorias = self.obtener_categorias()
        categoria = next((cat for cat in categorias if cat[0] == categoria_id), None)

        if categoria:
            self.txt_id_categoria.value = str(categoria[0])
            self.txt_nombre_categoria.value = categoria[1]
            self.txt_descripcion_categoria.value = categoria[2]
            self.btn_guardar_categoria.text = "Editar"
            self.btn_guardar_categoria.icon = ft.icons.EDIT
            self.categoria_editando = categoria_id
            self.page.update()

    def eliminar_categoria(self, categoria_id):
        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM categoria WHERE idCategoria = %s", (categoria_id,))
        conexion.commit()
        conexion.close()

        self.page.snack_bar = ft.SnackBar(ft.Text("Categoría eliminada correctamente"), bgcolor=ft.colors.GREEN)
        self.page.snack_bar.open = True
        self.page.update()
        self.seleccionar_opcion(self.boton_activo, "categoria")

    # Proveedor

    def render_proveedor(self):
        proveedores = self.obtener_proveedores()

        self.txt_id_proveedor = ft.TextField(label="ID de Proveedor", bgcolor="#ffffff", width=400, filled=True)
        self.txt_nombre_proveedor = ft.TextField(label="Nombre", width=400, bgcolor="#ffffff", filled=True)
        self.txt_telefono_proveedor = ft.TextField(label="Teléfono", width=400, bgcolor="#ffffff", filled=True)
        self.txt_direccion_proveedor = ft.TextField(label="Dirección", bgcolor="#ffffff", width=400, multiline=True,
                                                    min_lines=2, max_lines=4, filled=True)

        self.btn_guardar_proveedor = ft.ElevatedButton(
            "Guardar",
            icon=ft.icons.SAVE,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            on_click=self.guardar_proveedor,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )

        if not proveedores:
            lista_proveedores = ft.Text("Aún no hay proveedores añadidos.", italic=True, color=ft.colors.GREY)
        else:
            lista_proveedores = ft.DataTable(
                columns=[
                    ft.DataColumn(label=ft.Text("ID")),
                    ft.DataColumn(label=ft.Text("Nombre")),
                    ft.DataColumn(label=ft.Text("Teléfono")),
                    ft.DataColumn(label=ft.Text("Dirección")),
                    ft.DataColumn(label=ft.Text("Acciones")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(prov[0]))),
                            ft.DataCell(ft.Text(prov[1])),
                            ft.DataCell(ft.Text(prov[2])),
                            ft.DataCell(ft.Text(prov[3])),
                            ft.DataCell(
                                ft.Row(
                                    spacing=10,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.icons.EDIT,
                                            tooltip="Editar",
                                            icon_color=ft.colors.BLUE,
                                            on_click=lambda e, prov_id=prov[0]: self.editar_proveedor(prov_id)
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.DELETE,
                                            tooltip="Eliminar",
                                            icon_color=ft.colors.RED,
                                            on_click=lambda e, prov_id=prov[0]: self.eliminar_proveedor(prov_id)
                                        ),
                                    ]
                                )
                            ),
                        ]
                    )
                    for prov in proveedores
                ]
            )

        return [
            ft.Container(
                content=ft.Card(
                    content=ft.Container(
                        padding=20,
                        bgcolor="#fafafa",
                        border_radius=10,
                        content=ft.Column(
                            spacing=15,
                            controls=[
                                ft.Text("Agregar nuevo proveedor", size=18, weight="bold"),
                                self.txt_id_proveedor,
                                self.txt_nombre_proveedor,
                                self.txt_telefono_proveedor,
                                self.txt_direccion_proveedor,
                                ft.Row(
                                    controls=[self.btn_guardar_proveedor],
                                    alignment="end"
                                )
                            ]
                        )
                    )
                ),
                margin=10
            ),
            ft.Text("Proveedores existentes", size=18, weight="bold"),
            lista_proveedores
        ]

    def obtener_proveedores(self):
        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT idProveedor, nombre, telefono, direccion FROM proveedor")
        proveedores = cursor.fetchall()
        cursor.close()
        conexion.close()
        return proveedores

    def guardar_proveedor(self, e):
        id_text = self.txt_id_proveedor.value
        nombre = self.txt_nombre_proveedor.value
        telefono = self.txt_telefono_proveedor.value
        direccion = self.txt_direccion_proveedor.value

        if not id_text or not nombre or not telefono or not direccion:
            self.page.snack_bar = ft.SnackBar(ft.Text("Todos los campos son obligatorios"), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        try:
            id_proveedor = int(id_text)
        except ValueError:
            self.page.snack_bar = ft.SnackBar(ft.Text("El ID debe ser un número entero"), bgcolor=ft.colors.RED)
            self.page.snack_bar.open = True
            self.page.update()
            return

        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()

        try:
            if self.proveedor_editando is not None:
                cursor.execute(
                    "UPDATE proveedor SET nombre = %s, telefono = %s, direccion = %s WHERE idProveedor = %s",
                    (nombre, telefono, direccion, self.proveedor_editando)
                )
                self.page.snack_bar = ft.SnackBar(ft.Text("Proveedor actualizado correctamente"), bgcolor=ft.colors.GREEN)
                self.btn_guardar_proveedor.text = "Guardar"
                self.btn_guardar_proveedor.icon = ft.icons.SAVE
                self.proveedor_editando = None
            else:
                cursor.execute(
                    "INSERT INTO proveedor (idProveedor, nombre, telefono, direccion) VALUES (%s, %s, %s, %s)",
                    (id_proveedor, nombre, telefono, direccion)
                )
                self.page.snack_bar = ft.SnackBar(ft.Text("Proveedor guardado correctamente"), bgcolor=ft.colors.GREEN)

            conexion.commit()
            self.txt_id_proveedor.value = ""
            self.txt_nombre_proveedor.value = ""
            self.txt_telefono_proveedor.value = ""
            self.txt_direccion_proveedor.value = ""

        except Exception as e:
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(e)}"), bgcolor=ft.colors.RED)

        finally:
            self.page.snack_bar.open = True
            self.page.update()
            self.seleccionar_opcion(self.boton_activo, "proveedor")

    def editar_proveedor(self, proveedor_id):
        proveedores = self.obtener_proveedores()
        proveedor = next((prov for prov in proveedores if prov[0] == proveedor_id), None)

        if proveedor:
            self.txt_id_proveedor.value = str(proveedor[0])
            self.txt_nombre_proveedor.value = proveedor[1]
            self.txt_telefono_proveedor.value = proveedor[2]
            self.txt_direccion_proveedor.value = proveedor[3]
            self.btn_guardar_proveedor.text = "Editar"
            self.btn_guardar_proveedor.icon = ft.icons.EDIT
            self.proveedor_editando = proveedor_id
            self.page.update()

    def eliminar_proveedor(self, proveedor_id):
        db = DB()
        conexion = db.connect()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM proveedor WHERE idProveedor = %s", (proveedor_id,))
        conexion.commit()
        conexion.close()

        self.page.snack_bar = ft.SnackBar(ft.Text("Proveedor eliminado correctamente"), bgcolor=ft.colors.GREEN)
        self.page.snack_bar.open = True
        self.page.update()
        self.seleccionar_opcion(self.boton_activo, "proveedor")

if __name__ == '__main__':
    ft.app(target=App)


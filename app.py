from tkinter import ttk
from tkinter import *
import sqlite3

from sqlalchemy import values
from sqlalchemy.orm import Session
from database import Producto, get_db, Base, engine, SessionLocal

class VentanaPrincipal():

    def __init__(self, root):
        self.ventana = root
        self.ventana.title("App Gestor de Productos")
        self.ventana.resizable(1,1) #Activa la redimencion de la ventana
        self.ventana.wm_iconbitmap("recursos/icono.ico")
        self.ventana.geometry("650x730")

        self.ventana.columnconfigure(0, weight=1)
        self.ventana.columnconfigure(1, weight=1)

        self.ventana.rowconfigure(0, weight=1)
        self.ventana.rowconfigure(6, weight=0)
        self.ventana.rowconfigure(7, weight=10)
        self.ventana.rowconfigure(8, weight=1)


        # Configuracion de estilos para una interfaz más moderna
        s = ttk.Style()
        # Estilo para LabelFrame
        s.configure('TFrame', background='#e0e0e0', relief='flat')  # Un color de fondo suave y sin relieve
        s.configure('TLabelframe', background='#e0e0e0', relief='flat')
        s.configure('TLabelframe.Label', font=('Calibri', 18, 'bold'),foreground='purple')  # Color de texto oscuro para el título del frame

        # Estilo para Label
        s.configure('TLabel',
                    font=('Calibri', 14),
                    background='#e0e0e0',
                    foreground='#444444')  # Color de fondo y de texto para etiquetas

        # Estilo para Botones
        s.configure('my.TButton',
                    font=('Calibri', 16, 'bold'),
                    background='#4CAF50',
                    foreground='magenta',
                    relief='raised',
                    padding=10)
        s.map('my.TButton',
              background=[('active', '#45a049')],
              foreground=[('active', 'white')])  # Cambio de color al pasar el ratón

        # Mensaje informativo
        s.configure('Error.TLabel', font=('Calibri', 13, 'bold'), foreground='red', background='#e0e0e0')
        s.configure('TCombobox', font=('Calibri', 13)) # Estilo para el Combobox

        # Creacion del contenedor principal (frame)
        frame = ttk.LabelFrame(self.ventana, text="Registrar Un Nuevo Producto", style='TLabelframe')
        frame.grid(row=0, column=0, pady=20, columnspan=3, sticky=W+E+N+S)
        frame.columnconfigure(1, weight=1)

        # Label de Nombre
        self.etiqueta_nombre = ttk.Label(frame, text="Nombre: ", style='TLabel')
        self.etiqueta_nombre.grid(row=1, column=0, pady=5, sticky=W)

        #Entry de Nombre
        self.nombre = Entry(frame, font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1)
        self.nombre.grid(row=1, column=1, pady=5, padx=5, sticky=W +E )
        self.nombre.focus()

        # Label de Precio
        self.etiqueta_precio = ttk.Label(frame, text="Precio: ", style='TLabel')
        self.etiqueta_precio.grid(row=2, column=0, pady=5, sticky=W)

        # Entry de Precio
        self.precio = Entry(frame, font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1)
        self.precio.grid(row=2, column=1, pady=5, padx=5, sticky=W+E)

        # Label Categoria
        self.etiqueta_categoria = ttk.Label(frame, text="Categoría: ", style='TLabel')
        self.etiqueta_categoria.grid(row=3, column=0, pady=5, sticky=W)

        #Combobox de Categoria
        self.categorias_posibles = ['Electrónica', 'Alimentos', 'Ropa', 'Hogar', 'Juguetes', 'Libros', 'Automoviles', 'Sin categoría']
        self.categoria = ttk.Combobox(frame, font=('Calibri', 13),
                                      values=self.categorias_posibles, state="readonly", style='TCombobox')
        self.categoria.grid(row=3, column=1, pady=5, sticky=W + E)
        self.categoria.set('Sin Categoria')

        # Label de Stock
        self.etiqueta_stock = ttk.Label(frame, text="Stock: ", style='TLabel')
        self.etiqueta_stock.grid(row=4, column=0, pady=5, sticky=W)

        # Spibox stock
        self.stock = ttk.Spinbox(frame, from_=0, to=9999, increment=1,
                                 font=('Calibri', 13))
        self.stock.grid(row=4, column=1, pady=5, sticky=W + E)
        self.stock.set(0)

        # Boton añadir producto
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto", command=self.add_producto,
                                        style='my.TButton')
        self.boton_aniadir.grid(row=5, columnspan=2, sticky=W + E, pady=10, padx=5)

        # Mensaje informativo para el usuario
        self.mensaje = ttk.Label(self.ventana, text='', style='Error.TLabel')
        self.mensaje.grid(row=6, column=0, columnspan=2, sticky=W + E, pady=5)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness= 0, bd=0,
                        font=('Calibri', 13)) # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri' , 13, 'bold'), background='#007bff', foreground='blue') # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.trearea' , {'sticky': 'nswe'})]) #Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=(1, 2, 3,4), style="mystyle.Treeview")
        self.tabla.grid(row=7, column=0, columnspan=2, pady=10, padx=20, sticky=W+E+N+S)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER) # Encabezado 0
        self.tabla.heading('#1', text='ID', anchor=CENTER) # Encabezado 1
        self.tabla.heading('#2', text='Precio', anchor=CENTER) # Encabezado 2
        self.tabla.heading('#3', text='Categoria', anchor=CENTER) # Encabezado 3
        self.tabla.heading('#4', text='Stock', anchor=CENTER) # Encabezado 4

        self.tabla.column('#0', width=150, anchor=CENTER)
        self.tabla.column('#1', width=50, anchor=CENTER)
        self.tabla.column('#2', width=100, anchor=CENTER)
        self.tabla.column('#3', width=150, anchor=CENTER)
        self.tabla.column('#4', width=80, anchor=CENTER)

        # Botones de Eliminar y Editar
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command = self.del_producto,
                                         style='my.TButton')
        self.boton_eliminar.grid(row=8, column=0, sticky=W + E, pady=3, padx=20)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto,
                                       style='my.TButton')
        self.boton_editar.grid(row=8, column=1, sticky=W + E, pady=3, padx=20)

        self.get_productos()

    def get_productos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla.get_children() # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        db = next(get_db())
        productos = db.query(Producto).order_by(Producto.nombre.desc()).all()
        db.close()

        for prod in productos:
            self.tabla.insert("", 0, text=prod.nombre, values=(prod.id, prod.precio, prod.categoria, prod.stock))

    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def validacion_Stock(self):
        try:
            stock_val = int(self.stock.get())
            return stock_val >= 0
        except ValueError:
            return False

    def validacion_precio_str(self, precio_str):
        try:
            precio = float(precio_str)
            return precio > 0
        except ValueError:
            return False

    def validacion_stock_str(self, stock_str):
        try:
            stock_val = int(stock_str)
            return stock_val >=0
        except ValueError:
            return False

    def add_producto(self):
        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacio'
            return
        if not self.validacion_precio():
            print("El precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un número valido mayor que 0'
            return
        if not self.validacion_Stock():
            self.mensaje['text'] = 'El stock es obligatorio y debe ser un número entero mayor o igual que 0.'
            return

        db = next(get_db())
        try:
            nuevo_producto = Producto(
                nombre = self.nombre.get(),
                precio = float(self.precio.get()),
                categoria = self.categoria.get(),
                stock = int(self.stock.get())
            )
            db.add(nuevo_producto)
            db.commit()
            db.refresh(nuevo_producto)
            self.mensaje['text'] = f'Producto {self.nombre.get()} añadido con éxito.'
        except Exception as e:
            db.rollback()
            self.mensaje['text'] = f'Error al añadir producto: {e}'
        finally:
            db.close()

        # print("Datos guardados")
        self.nombre.delete(0, END) # Borrar el campo nombre del formulario
        self.precio.delete(0, END) # Borrar el campo precio del formulario
        self.categoria.set('Sin Categoria')
        self.stock.delete(0, END)

        self.get_productos()

    def del_producto(self):
        self.mensaje['text'] = '' # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un producto para poder eliminarlo
        try:
            selected_items_ids = self.tabla.selection()

            if not selected_items_ids:
               self.mensaje['text'] = 'Por favor, seleccione un producto para eliminar.'
               return

            item_id_treeview = selected_items_ids[0]
            item_data = self.tabla.item(item_id_treeview)

            nombre_producto = item_data['text']
            id_producto = item_data['values'][0]

        except IndexError:
            self.mensaje['text'] = 'Error al obtener los datos del producto seleccionado (índice fuera de rango).'
            return
        except KeyError:
            self.mensaje['text'] = 'Error: No se pudieron obtener las claves de los valores del producto seleccionado.'
        except Exception as e:
            self.mensaje['text'] = f'Error inesperado al obtener selección: {e}'

        db = next(get_db())
        try:
            producto_a_eliminar = db.query(Producto).filter(Producto.id == id_producto).first()

            if producto_a_eliminar:
                db.delete(producto_a_eliminar)
                db.commit()
                self.mensaje['text'] = f'Producto {nombre_producto} eliminado con exito.'
                self.get_productos()
            else:
                self.mensaje['text'] = f'No se encontró el producto para eliminar en la bae de datos.'
        except Exception as e:
            db.rollback()
            self.mensaje['text'] = f'Error al eliminar producto: {e}'
        finally:
            db.close()

    def edit_producto(self):
        self.mensaje['text'] = ''
        try:
            item_seleccionado_treeview_id = self.tabla.focus()
            if not item_seleccionado_treeview_id:
                self.mensaje['text'] = 'Por favor seleccione un producto para editar.'
                return
            item_data = self.tabla.item(item_seleccionado_treeview_id)

            nombre_viejo = item_data['text']

            id_viejo = item_data['values'][0]
            precio_viejo = item_data['values'][1]
            categoria_vieja = item_data['values'][2]
            stock_viejo = item_data['values'][3]

            if stock_viejo is None:
                stock = 0

            self.editor_de_producto_actual = VentanaEditarProducto(self,
                                                                   id,
                                                                   nombre_viejo,
                                                                   precio_viejo,
                                                                   categoria_vieja,
                                                                   stock_viejo,
                                                                   self.mensaje)
            self.editor_de_producto_actual.ventana_editar.grab_set()
            self.editor_de_producto_actual.ventana_editar.wait_window()

        except IndexError:
            self.mensaje['text'] = 'Por favor seleccione un producto para editar.'
        except Exception as e:
            self.mensaje['text'] = f'Error al intentar editar el producto: {e}'

class VentanaEditarProducto():

    def __init__(self, ventana_principal, id, nombre, precio, categoria, stock, mensaje):
        self.ventana_principal = ventana_principal
        self.id_viejo = id
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.stock = stock
        self.mensaje = mensaje

        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto: {nombre}")

        # Asegurar que la ventana de edición sea modal (bloquea la ventana principal)
        self.ventana_editar.grab_set()
        self.ventana_editar.transient(self.ventana_principal.ventana)
        self.ventana_editar.resizable(False, False)

        # Creacion del contenedor Frame para la edición del producto
        frame_ep = ttk.LabelFrame(self.ventana_editar, text="Editar el siguiente Producto", style='TLabelframe')
        frame_ep.grid(row=0, column=0, columnspan=2, pady=20, padx=20)
        frame_ep.columnconfigure(1, weight=1)

        # Label y Entry para el Nombre antiguo (solo lectura)
        ttk.Label(frame_ep, text="Nombre antiguo: ", style=('TLabel')).grid(row=1, column=0, pady=5, sticky=W)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly',
              font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1).grid(row=1, column=1, pady=5, padx=5, sticky=W+E)

        # Label y Entry para el Nombre nuevo
        ttk.Label(frame_ep, text="Nombre nuevo: ", style='TLabel').grid(row=2, column=0, pady=5, sticky=W)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1)
        self.input_nombre_nuevo.grid(row=2, column=1, pady=5, padx=5, sticky=W + E)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        ttk.Label(frame_ep, text="Precio antiguo: ", style='TLabel').grid(row=3, column=0, pady=5, sticky=W)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly',
              font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1).grid(row=3, column=1, pady=5, padx=5, sticky=W+E)

        # Precio nuevo
        ttk.Label(frame_ep, text="Precio nuevo: ", style=('TLabel')).grid(row=4, column=0, pady=5, sticky=W)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1)
        self.input_precio_nuevo.grid(row=4, column=1, pady=5, padx=5, sticky= W +E)

        # Label y Combobox para Categoria antigua (solo lectura)
        ttk.Label(frame_ep, text="Categoría antigua: ", style='TLabel').grid(row=5, column=0, pady=5, sticky=W)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria), state='readonly',
             font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1).grid(row=5, column=1, pady=5, padx=5, sticky=W +E )

        # Categoria nueva (Combobox)
        ttk.Label(frame_ep, text="Categoría nueva: ", style='TLabel').grid(row=6, column=0, pady=5, sticky=W)
        self.input_categoria_nueva = ttk.Combobox(frame_ep, font=('Calibri', 13),
                                                  values=self.ventana_principal.categorias_posibles,
                                                  state="readonly", style='TCombobox')
        self.input_categoria_nueva.grid(row=6, column=1, pady=5, padx=5, sticky= W + E)
        self.input_categoria_nueva.set(categoria)

        # Stock antiguo (solo lectura)
        ttk.Label(frame_ep, text="Stock antiguo: ", style='TLabel').grid(row=7, column=0, pady=5, sticky=W)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=stock), state='readonly',
              font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1).grid(row=7, column=1, pady=5, padx=5, sticky=W + E)

        # Stock nuevo
        ttk.Label(frame_ep, text="Stock nuevo: ", style='TLabel').grid(row=8, column=0, pady=5, sticky=W)
        self.input_stock_nuevo = Entry(frame_ep, font=('Calibri', 13), relief='flat', bd=2, highlightbackground="#cccccc", highlightcolor="#007bff", highlightthickness=1)
        self.input_stock_nuevo.grid(row=8, column=1, pady=5, padx=5, sticky= W + E)
        self.input_stock_nuevo.insert(0, stock)

        ttk.Button(frame_ep, text="Actualizar Producto",
        style='my.TButton', command=self.actualizar).grid(row=9,columnspan=2,sticky=W + E, pady=10)

    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() .strip()
        # Si el nombre está vacío, usa el nombre original
        nombre_final = nuevo_nombre if nuevo_nombre else self.nombre

        nuevo_precio_str = self.input_precio_nuevo.get().strip()
        # Si el precio  nuevo está vacío, usa el nombre original
        precio_final_str = nuevo_precio_str if nuevo_precio_str else str(self.precio)

        nueva_categoria = self.input_categoria_nueva.get()
        # Si la categoría nueva está vacía, usa la categoría vieja
        categoria_final = nueva_categoria

        nuevo_stock_str = self.input_stock_nuevo.get().strip()
        stock_final_str = nuevo_stock_str if nuevo_stock_str else str(self.stock)

        if (nombre_final and
                self.ventana_principal.validacion_precio_str(precio_final_str) and
                self.ventana_principal.validacion_stock_str(stock_final_str)):

            db = next(get_db())
            try:
                producto_a_actualizar = db.query(Producto).filter(
                    Producto.nombre == self.nombre,
                    Producto.precio == self.precio,
                    Producto.categoria == self.categoria,
                    Producto.stock == self.stock
                ).first()

                if producto_a_actualizar:
                    producto_a_actualizar.nombre = nombre_final
                    producto_a_actualizar.precio = float(precio_final_str)
                    producto_a_actualizar.categoria = categoria_final
                    producto_a_actualizar.stock = int(stock_final_str)

                    db.commit()
                    self.ventana_principal.mensaje['text'] = f'El producto "{self.nombre}" ha sido actualizado con éxito.'
                    self.ventana_editar.destroy()
                    self.ventana_principal.get_productos()
                else:
                    self.ventana_principal.mensaje['text'] = f'No se encontró el producto original para actualizar.'

            except Exception as e:
                db.rollback()
                self.ventana_principal.mensaje['text'] = f'Error al actualizar el producto {self.nombre}. Verifique los datos.s '

        else:
                self.mensaje['text'] = f'No se puede actualizar el producto {self.nombre}. Verifique los datos.'

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    root = Tk() # Instancia de la ventana principal
    app = VentanaPrincipal(root) #Enviamos y cedemos el control a la clase
    root.mainloop()
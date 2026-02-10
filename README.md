# 📦 Gestor de Productos (Escritorio)

Aplicación de escritorio (Desktop App) desarrollada en Python para la gestión administrativa de inventarios. Este sistema permite a los usuarios mantener un control total sobre el stock de productos mediante una interfaz gráfica intuitiva y fácil de usar.

## 🚀 Características Principales

El sistema implementa un **CRUD completo** (Create, Read, Update, Delete) con las siguientes funcionalidades:

* **📝 Registro de Productos:** Formulario para ingresar nuevos artículos con validación de campos.
* **📊 Visualización de Inventario:** Tabla dinámica que muestra:
    * ID (Identificador único)
    * Nombre del producto
    * Precio
    * Categoría (Ej: Electrónica, Hogar, Alimentos, Ropa)
    * Stock disponible
* **✏️ Edición en Ventana Emergente:** Permite modificar los datos de un producto existente sin perder el foco de la tabla principal.
* **🗑️ Eliminación:** Opción para dar de baja productos del sistema con un solo clic.
* **📂 Categorización:** Organización de productos mediante categorías predefinidas.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Interfaz Gráfica (GUI):** Tkinter (Librería estándar de Python para interfaces de escritorio).
* **Base de Datos:** SQLite (Almacenamiento local y ligero).

El sistema cuenta con una interfaz amigable dividida en dos secciones principales: panel de registro y listado de productos.


## 🔧 Instalación y Uso

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/joce-ortiz/Gestor-de-productos.git](https://github.com/joce-ortiz/Gestor-de-productos.git)
    ```
2.  **Navegar a la carpeta:**
    ```bash
    cd Gestor-de-productos
    ```
3.  **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```
    *(Nota: Asegúrate de que tu archivo principal se llame 'main.py' o 'app.py', si tiene otro nombre, cámbialo en este comando).*

---
**Desarrollado por:** Jocelyn Ortiz

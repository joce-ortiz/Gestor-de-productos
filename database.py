from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Configuración de la base de datos
# Aquí defines la cadena de conexión. Para SQLite, es 'sqlite:///nombre_de_tu_base.db'
# Si quisieras cambiar a PostgreSQL, sería algo como 'postgresql://user:password@host:port/dbname'
DATABASE_URL = "sqlite:///database/productos.db"

# 2. Creación del "Engine"
# El engine es el punto de entrada principal para interactuar con la base de datos.
engine = create_engine(DATABASE_URL)

# 3. Declaración de la base (Base de clases para tus modelos)
# Todos tus modelos (clases que representan tablas) heredarán de esta Base.
Base = declarative_base()

# 4. Definición del Modelo (Producto)
# Esta clase representa tu tabla 'producto' en la base de datos.
class Producto(Base):
    __tablename__ = 'producto' # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String, default='Sin categoría')
    stock = Column(Integer, default=0)

    # Opcional: Representación en string del objeto, útil para depuración
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio}, categoria='{self.categoria}', stock={self.stock})>"

# 5. Creación de las tablas (si no existen)
# Esto revisa si la tabla 'producto' existe y, si no, la crea.
# Solo llama a esto una vez al inicio de tu aplicación o cuando se instala.
Base.metadata.create_all(engine)

# 6. Creación de una "SessionLocal"
# Esta es una fábrica de sesiones. Las sesiones son tu forma de interactuar con la DB.
# Cada vez que necesites realizar operaciones (leer, escribir), obtendrás una sesión.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 7. Función para obtener una sesión (dependencia)
# Esta es una buena práctica para manejar las sesiones, asegurando que se cierren correctamente.
def get_db():
    db = SessionLocal()
    try:
        yield db # 'yield' permite que la sesión se use y luego se cierre automáticamente
    finally:
        db.close()
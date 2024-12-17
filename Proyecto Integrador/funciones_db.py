import sqlite3

def db_inventario_launcher():   # Establece conección con la tabla "Productos". Si no existe la crea!
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS "Productos" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL UNIQUE,
	"descripcion"	TEXT,
	"cantidad"	INTEGER NOT NULL,
	"precio"	REAL NOT NULL,
	"categoria"	TEXT,
	"stockMin"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
) """
    )
    conexion.commit()
    conexion.close()
    return

def db_buscar_producto_one(columna, contenido): # Función de búsqueda a utiliar cuando se espera sólo un resgistro.
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    query = f"SELECT * FROM Productos WHERE {columna} = ?"
    placeholder = (contenido,)
    cursor.execute(query, placeholder)
    resultado = cursor.fetchone()
    conexion.close()
    return resultado

def db_buscar_productos_all(columna, contenido): # Función de búsueda a utilizar cuando se esperan multiples registros.
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    query = f"SELECT * FROM Productos WHERE {columna} LIKE '%{contenido}%'"
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def db_productos_bajo_stock(modalidad): # Devuelve los productos que cumplen con el criterio etablecido en "modalidad"
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    query = f"SELECT * FROM Productos WHERE cantidad <= {modalidad}"
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado
    
def db_registrar_producto(producto):    # Se ingrea registo NUEVO "producto" em la tabla "Productos".
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    query = "INSERT INTO Productos VALUES (NULL,?,?,?,?,?,?)"
    placeholder = (
        producto.get("nombre"),
        producto.get("descripcion"),
        producto.get("cantidad"),
        producto.get("precio"),
        producto.get("categoria"),
        producto.get("stockMin"),
    )
    try:
        cursor.execute(query, placeholder)
        conexion.commit()        
    except:
        print("-- No se ingresó...\n")
    else:
        print("-- Producto INGRESADO exitosamente!\n")
    conexion.close()
    return

def db_actualizar_producto(producto):   # Se ACTUALIZAN los dotos del regisro con la ID específica con los datos de "producto"
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    query = "UPDATE Productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ?, stockMin = ? WHERE id = ?"
    placeholder = (
        producto.get("nombre"),
        producto.get("descripcion"),
        producto.get("cantidad"),
        producto.get("precio"),
        producto.get("categoria"),
        producto.get("stockMin"),
        producto.get("id"),
    )
    try:
        cursor.execute(query, placeholder)
        conexion.commit()        
    except:
        print("-- No se actualizó...\n")
    else:
        print("-- Producto ACTUALIZADO exitosamente!\n")
    conexion.close()
    return

def db_eliminar_producto(prodID):   # Se ELIMINA el registro con ID especificado en "prodID".
    conexion = sqlite3.connect("Inventario.db")
    cursor = conexion.cursor()
    query = "DELETE FROM Productos WHERE id = ?"
    placeholder = (prodID,)
    try:
        cursor.execute(query, placeholder)
        conexion.commit()        
    except:
        print("-- No se eliminó...\n")
    else:
        print("-- Producto ELIMINADO exitosamente!\n")
    conexion.close()
    return


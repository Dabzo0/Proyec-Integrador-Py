import msvcrt
from funciones_db import *
from colorama import Fore, Style, Back, init  # requiere libreria #pip import colorama
init()

producto = {    # Diccionario Producto
    "id": int,
    "nombre": str,
    "descripcion": str,
    "cantidad": int,
    "precio": float,
    "categoria": str,
    "stockMin": int,
}

def menu_ppal(): # Muesta en pantalla el menú y pide al usuario ingresar una opción
    print("*" * 80)
    print(Back.BLUE +' '*32+ Fore.WHITE +"MENÚ DE OPCIONES"+' '*32+ Style.RESET_ALL + "\n")
    print(">>> Seleccione una opción presionando una tecla: ")
    nTxt=Fore.GREEN+"[N]"+Style.RESET_ALL
    print(f"\t{nTxt} Para registrar un NUEVO producto.")
    tTxt=Fore.GREEN+"[T]"+Style.RESET_ALL
    print(f"\t{tTxt} Para mostrar lista de TODOS los productos.")
    aTxt=Fore.GREEN+"[A]"+Style.RESET_ALL
    print(f"\t{aTxt} Para ACTUALIZAR la cantidad actual de un producto.")
    eTxt=Fore.GREEN+"[E]"+Style.RESET_ALL
    print(f"\t{eTxt} Para ELIMINAR productos.")
    bTxt=Fore.GREEN+"[B]"+Style.RESET_ALL
    print(f"\t{bTxt} Para BUSCAR productos.")
    sTxt=Fore.GREEN+"[S]"+Style.RESET_ALL
    print(f"\t{sTxt} Para mostrar productos con bajo STOCK.")
    escTxt=Fore.RED+"[Esc]"+Style.RESET_ALL
    print(f"\t{escTxt} Para SALIR.\n")
    return str(msvcrt.getch()).lower()

def ingresar_productos():
    print("[N] == Ingrese los detalles del producto " + "=" * 39)
    
    while True:
        prodNom=validar_nombre() # Se pide al usuario que ingrese un nombre y se carga en la variable "prodNom".
        
        if check_nombre_disponible(prodNom)==False: # Si el nombre se encuentra en tabla "Productos" no se hace nada.
            print("-- Ya existe producto ingresado con ese NOMBRE.\n")
        else:   # Si el nombre no se encuentra en tabla "Productos" se continúa con la carga de datos del producto en un diccionario producto.
            print("-- NOMBRE disponible!\n")
            producto["id"]="--" # Como es u producto nuevo no tiene ID todavía.
            producto["nombre"]=prodNom        
            producto["descripcion"] = validar_descripcion()
            producto["cantidad"] = validar_entero(" * Cantidad de unidades a ingresar: ", False, "cantidad")
            producto["precio"] = validar_precio()
            producto["categoria"] = elegir_categoria()
            producto["stockMin"] = validar_entero(" * Cantidad de unidades a considerar como mínimas: ", False, "cantidad")
            print("\n-- Se ingresará: \n")
            imprimir_producto(producto) # Se muestran al usuario todos los datos ingresados.
            
            while True: # Bucle confirmación. Se interrumpe sólo cuando el usuario ingresa una de las opciones ofrecidas.
                print(" * Presione [S] Para CONFIRMAR ingreso o [Esc] para CANCELAR")
                opt=str(msvcrt.getch()).lower() # Se captura tecla presionada por el usuario.
                if opt[2] == "s":   # Si se presionó la tecla "escape" se REALIZA el ingreso del producto.
                    print("-- Ingresando producto...")
                    db_registrar_producto(producto) # Se ingresa el diccionario producto en la tabla "Productos"
                    break
                elif opt[3:6] == "x1b": # Si se presionó la tecla "escape" se INTERRUMPE el ingreso del producto.
                    print("--  Cancelado...\n")
                    break
        
        print(" * Presiones cualquier tecla si desa INGRESAR otro producto o [Esc] para TERMINAR la operación.")
        if (str(msvcrt.getch()).lower())[3:6] == "x1b": # Finaliza el bucle principal el usuario presionó la tecla "escape".
            break
        else:   # Coninua el bucle principal si el usuario no presionó la tecla "escape".
            print("-- Continuar ingresando productos...\n")

    print("-- Operación terminada!\n")
    return

def mostrar_prductos_todos():
    print("[T] " + "=" * 22 + " Mostrando todos los productos " + "=" * 23)
    
    paqueteRegistros = db_buscar_productos_all("nombre","") # Se capturan de la tabla "Productos" todos los regitro con nombre.
    if not paqueteRegistros:    # Si no se ecuentran registros se informa al usuario.
        print("-- El inventario de productos se encuentra vacío...")
        return
    else:   # Si se encuentran registros se imprimen.
        imprimir_paqueteRegistros(paqueteRegistros)
    return

def actualizar_producto():
    print("[A] == Actualizar un producto buscado por ID " + 35 * "=")
    
    while True:     # Bucle principal.
        prodId = validar_entero(" * Ingrese ID del producto a actualizar: ", False, "ID")   # Se solicita al usuario ID.
        prodTupla = db_buscar_producto_one("id", prodId)    # Se busca reegisro con el ID ingresado por el usuario en la tabla "Productos".
        
        if not prodTupla:   # Si no se encuentra registro con el ID ingresado no se hace nada.
            print("-- No se encontró producto con el ID ingresado...\n")
        else:   # Si se encuentra registro con el ID ingresado se continúa.
            producto = convertir_a_producto(prodTupla)  # Se convierte la tupla devuelta por el fetchone en dieccionario producto.
            print("-- Se encontró:\n")
            imprimir_producto(producto) # Se muestra el producto encontrado.
            
            while True:  # Bucle gestón de modificación Actualiar o Agregar/Quitar.
                print(
                    " * Precione: [1] Modificar cantidad actual\t[2] Agregar/Quitar\t[Esc] Cancelar"
                )
                actModo = str(msvcrt.getch()).lower()   # Se captura la tecla presionada por el usuario en la variable "actModo".
                
                if actModo[2] == "1":   # Modo Actualizar: Canbia la cantidad alctual del producto por la nueva ingresada por el usuario.
                    nuevaCantidad = validar_entero(
                        " * [1] Ingrese la actidad actual del producto: ",
                        False,
                        "cantidad",
                    )   # Se pide al usuario que ingrese la nueva cantidad del producto y se valida que sea un estero positivo.
                    producto["cantidad"] = nuevaCantidad # Se cambia la cantidad en la variable diccionario producto.
                    print("-- Actualizando producto...")
                    db_actualizar_producto(producto)    # Se actualia el regitro en la base de datos con los nuevos datos del diccionario producto.
                    imprimir_producto(
                        convertir_a_producto(db_buscar_producto_one("id", prodId))
                    )   # Se muestra el resultado de la actualizacion.

                elif actModo[2] == "2": # Si se presionó la tecla "2": Modo Agregar/Quitar
                    nuevaCantidad = validar_entero(
                        " * [2] Ingrese la actidad de unidades a agregar o quitar: ",
                        True,
                        "cantidad",
                    ) # Se pide al isuario que ingrese una cantidad. Admite enteros negativos en caso de que se quiera disminuir la cantidad de unidades del producto.
                    producto["cantidad"] = producto.get("cantidad") + nuevaCantidad # Se adiciona la cantidad ingresada por el usuaruio a la existene en el diccionario producto.
                    print("-- Actualizando producto...")
                    db_actualizar_producto(producto)    # Se actualia el regitro en la base de datos con los nuevos datos del diccionario producto.
                    imprimir_producto(
                        convertir_a_producto(db_buscar_producto_one("id", prodId))
                    )   # Se muestra el resultado de la actualizacion.
                
                elif actModo[3:6] == "x1b": # Se interrumpe el bucle de gestión de modificación si el usuario presionó la tecla "escape".
                    print("-- [Esc] Actualización cancelada...\n")
                    break
        
        print(
            " * Precione cualquier tecla para ACTUALIZAR otro producto o [Esc] para TERMINAR la operación."
        )
        if str(msvcrt.getch()).lower()[3:6] == "x1b":   # Finaliza el bucle principal el usuario presionó la tecla "escape".            
            break
        else:   # Coninua el bucle principal si el usuario no presionó la tecla "escape".
            print("--- Actualizar otro poducto.\n")

    print("-- [Esc] Operación terminada!\n")
    return

def eliminar_producto():
    print("[E] == Elimnar un producto buscado por ID " + 38 * "=")
    
    while True: # Bucle principal.
        prodId = validar_entero(" * Ingrese ID: ", False, "ID") # Se solicita al usuario ID.
        prodTupla = db_buscar_producto_one("id", prodId)    # Se busca reegisro con el ID ingresado por el usuario en la tabla "Productos".
        
        if not prodTupla:   # Si no se encuentra registro con el ID ingresado no se hace nada.
            print("-- No se encontro el producto con el ID ingresado...\n")
        else:   # Si se encuentra registro con el ID ingresado se continúa.
            producto = convertir_a_producto(prodTupla) # Se convierte la tupla devuelta por el fetchone en dieccionario producto.
            print("-- Se encontro:\n")
            imprimir_producto(producto) # Se muestra al producto encontrado.
            
            while True: # Bucle caonfirmar o cancelar. Finaliza sólo cuando el usuario presiona una tecla correspondiente a las opciones ofrecidas.
                print(" * Presione:\t[C] Para CONFIRMAR\t\t[Esc] Para CANCELAR")
                opt=str(msvcrt.getch()).lower()
                if opt[2] == "c":   # Si se presionó la tecla "c".
                    print("-- [C] Eliminando producto...")
                    db_eliminar_producto(producto.get("id"))    # Se elimina registro de la tabla.
                    break
                elif opt[3:6] == "x1b": # Si se presionó la tecla "escape".
                    print("-- [Esc] Operación cancelada.\n")    # Se interrumpe la eliminación.
                    break
        
        print(
            " * Precione cualquier tecla para ELIMINAR otro producto o [Esc] Para FINALIZAR."
        )
        if str(msvcrt.getch()).lower()[3:6] == "x1b":   # Finaliza el bucle principal el usuario presionó la tecla "escape".
            break
        else:   # Coninua el bucle principal si el usuario no presionó la tecla "escape".
            print("-- Eliminar otro producto.\n")
               
    print("-- [Esc] Operación finalizada.\n")
    return

def buscar_productos():
    print("[B] ==  Buscar productos " + "=" * 55)
    
    while True: # Bucle principal.
        
        while True: # Bucle gestión de búsqueda.
            print(
                " * Presione: [1] Buscar por ID\t[2] Buscar por NOMBRE\t[3] Buscar por CATEGORÍA\t[Esc] FINALIZAR busqueda"
            )
            opt = str(msvcrt.getch()).lower()   # Se captrura la tecla presionada por el usuario en la variable "opt"
            
            if opt[2] == "1":   # Si el usuario presionó la tecla "1": Buscar por ID.
                print("-- [1] Búsqueda por ID.")
                prodId = validar_entero(" * Ingrese ID del producto a actualizar: ", False, "ID")   # Se solicita al usuario ID.
                prodTupla = db_buscar_producto_one("id", prodId)    # Se busca un reegisro con el ID ingresado por el usuario en la tabla "Productos".
                
                if not prodTupla:   # Si no se encuentró producto no se hace nada.
                    print("-- No se encuentra producto que el ID ingresado.\n")
                else:   # Si se encontró producto se imprime.
                    print("-- Se encontó:\n")
                    imprimir_producto(convertir_a_producto(prodTupla))
                break
            
            if opt[2] == "2":   # Si el usuario presionó la tecla "2": Buscar por NOMBRE.
                print("-- [2] Búsqueda por NOMBRE.")
                prodNomb = validar_nombre() # Se carga la variable "prodNomb" con el nombre ingresado por el usuario.
                paqueteRegistros = db_buscar_productos_all("nombre", prodNomb)  # Se buscan registros que contengan (todo o parte), del NOMBRE ingresado en la tabla "Productos".
                
                if not paqueteRegistros:    # Si no se encontraron productos no se hace nada.
                    print("-- No se encontraron productos...\n")
                else:   # Si se encontraron productos se imprimen.
                    print("-- Se encontró:\n")
                    imprimir_paqueteRegistros(paqueteRegistros)
                break
            
            if opt[2] == "3":   # Si el usuario presionó la tecla "1": Buscar por  CATEGORÍA.
                print("-- [3] Búsqueda por CATEGORIA.")
                catBuscar = elegir_categoria()  # Se pide al usuario elegir una categoría.
                paqueteRegistros = db_buscar_productos_all("categoria", catBuscar)  # Se buscan registros que contengan la CATEGORÍA elegida en la tabla "Productos".
                
                if not paqueteRegistros: # Si no se encontraron productos no se hace nada.
                    print("-- No se encontraron productos...\n")
                else:   # Si se encontraron productos se imprimen.
                    imprimir_paqueteRegistros(paqueteRegistros)
                break
            
            if opt[3:6] == "x1b":   # Si el usuario presionó la tecla "escape" se interrumpe el bucle gestión de búsqueda.
                print("-- [Esc] Operación cancelada...\n")
                break

        print(
            " * Presione cualquier tecla para realizar otra BÚSQUEDA o [Esc] Para FINALIZAR la operación."
        )
        if str(msvcrt.getch()).lower()[3:6] == "x1b":   # Finaliza el bucle principal el usuario presionó la tecla "escape".
            break
        else:   # Coninua el bucle principal si el usuario no presionó la tecla "escape".
            print("-- Buscar otro producto.\n")

    print("-- [Esc] Operación finalizada.\n")
    return

def mostrar_bajo_sotck():
    print("[B] " + "=" * 20 + " Mostrando productos con bajo stock " + "=" * 20)
    
    while True: # Bucle gestión modalidad de búsqueda. Se interrumpe sólo cuando el usuario seleciona alguna de las opciones ofrecidas. 
        print(""" * Seleccione modalidad presiponando: 
              \t[1] Mostrar indicando la cantidad MÍNIMA
              \t[2] Mostrar según stock mínimo ingresado en el producto"""
            )
        opt = str(msvcrt.getch()).lower() # Se captura la tecla presionada por el usuario.
        
        if opt[2]=="1": # Si presionó la tecla "1": Bucar por stock mínimo indicado por el usuario. 
            print("-- [1] Indiccando la cantidad mínima")
            stockMin=validar_entero(" * Ingrese el stock MÍNIMO deseado: ",False,"cantidad") # Se la carga variable "stockMin" con el VALOR ingresado.
            break
        
        if opt[2]=="2": # Si presionó la tecla "2": Bucar por stock mínimo indicado en la tabla "Productos". 
            print("-- [2] Según stock mínimo ingreasdo")
            stockMin="stockMin" # Se carga la variable "stockMin" con la COLUMNA a comparar en la tabla "Productos".
            break
    
    paqueteRegistros= db_productos_bajo_stock(stockMin)  # Se buscan registros con el parametro indicado en la variable "stockMin".
    
    if not paqueteRegistros:    # Si no se encuentran productos no se hace nada.
        print("-- No se encontraron productos con bajo stock!\n")
    else:   # Si se encuentran productos se imprimen.
        print("-- Poductos con bajo stock:\n")
        imprimir_paqueteRegistros(paqueteRegistros)
    return

def salir():    # Devuelve "True" o "False".
    
    if (
        input(' * [Esc] === Escriba "SALIR" para confirmar: ').strip().upper()
        == "SALIR"
    ):  # Se solicita al usuario escribir la palabra "salir" para confirmar ("verdadero"), o no ("falso"). la finalización del programa.
        return True # Retorna "verdadero"  si el usuario ecribe salir
    
    else:   
        return False    # Retorna "falso" usurio no escribe salir.

def validar_nombre():   # Devuelve cadena no nula en mayúcula.
    
    while True:
        nombre = input(" * Ingrese nombre de producto: ").strip().upper() # Se carga la variable "nombre" con una cadena en mayúsculas sin espacios al comienzo ni al final.
        
        if not nombre: # Se avisa al usuario que la cadena es nula.
            print("-- No se ha ingresado un nombre.\n")
        else:   # Si el usuario ingresa alguna cadena no nula se inerrumpe el biucle
            break

    return nombre   # Retorna el contenido de la variblae "nombre"

def validar_descripcion():  # Devuelve cadena no nula o "Sin categoría".
    descripcion = input(" * Descripción: ").strip().capitalize()    # Se carga la variable "descripcion" con una cadena con la primer letra en mayúscula sin espacios al comienzo ni al final.
    
    if not descripcion:
        descripcion = "Sin descripción."    # Se carga la variable "descripcion" es nulo se carga con "Sin descripción".
        print("-- Sin descripción.")    # Se informa al usuario del contenido de la variable descripción.        
   
    return descripcion  # Retorna el contenido de la variable de "descripcion"S

def validar_entero(rotulo=str, negativo=False, objeto=str): # Devuelve número entero >= 0 si "negaivo" es "False", sino número entero. 
            # ("texto a imprimir", Verdadero si se admite como restorn un entero negatvo o Falso en caso contrario, "id" "cantidad" "unidades")
    
    while True:
        
        try:
            numero = int(input(rotulo)) # Se intenta cargar la variable "numero" con un número entero.            
        except:
            print(f"-- {objeto.capitalize()} no válida.")   # Si no se pudo cargar la variable "numero" con un número entero no se interrumpe el bucle.
        else:  
            
            if negativo == False and numero < 0:    # Si se cargó la variable "numero" con un número entero < 0  y no se admite como retorno no se interrumpe el bucle.
                print(f"-- No se admite {objeto} negativa.")    # Se avisa al usuario.
            
            else:
                break   # Si se cargó la variable "numero" con un número entero que se admite como retorno se interrumpe el bucle.

    return numero   # Retorno el conenido de la variable "numero"

def validar_precio():   # Devuelve número flotante >= 0.
    
    while True:
        try:
            precio = float(input(f" * Ingrece precio del producto: "))  # Se intenta cargar la variable "precio" con un número flotante.            
        except:
            print("-- Precio no válido.")   # Si no se pudo cargar la variable "precio" con un número flotante no se interrumpe el bucle.
        else:
            
            if precio < 0:
                print("-- No se admite precio negativo.")   # Si se cargó la variable "precio" con un número flotante < 0 no se interrumpe el bucle.
            
            else:
                break   # Si se cargó la variable "precio" con un número flotante >= 0 interrumpe el bucle.
    
    return precio

def elegir_categoria(): # Devuelve una cadena.
   
    while True:
        print(
            """ * Presione:
        \t[1] Categoría A
        \t[2] Categoría B
        \t[3] Categoría C
        \t[4] Sin categoría"""
        )   # Se muestran las categorías disponible (se puede crear una variable lista al inicio de este archivo para tomar de alli las categorías... "To do" XD)
        opt = str(msvcrt.getch()) # Se captura la tecla presionada por el usuario. Se interrumple el blucle sólo si el usuaio elige una de las opciones disponible.
        
        if opt[2] == "1":
            categoria = "Categoría A"   # Se carga la variable "categoria" con la cadena "Categoría A".
            break
        
        elif opt[2] == "2":
            categoria = "Categoría B"   # Se carga la variable "categoria" con la cadena "Categoría B".
            break
        
        elif opt[2] == "3":
            categoria = "Categoría C"   # Se carga la variable "categoria" con la cadena "Categoría C".
            break
        
        elif opt[2] == "4":
            categoria = "Sin categoría" # Se carga la variable "categoria" con la cadena "Sin categoría".
            break

    print(f"-- [{opt[2]}] {categoria}\n")

    return categoria # Retorna el contenido de la variable "categoría"

def check_nombre_disponible(prodNomb):  # Devuelve "True" o "False" si la cadena "prodNomb" se encuentra, o no, en los regiotros de la columna nombre de la tabla "Productos".
    prodTupla = db_buscar_producto_one("nombre", prodNomb)  # Se realiza búsqueda de un registro que contenga la cadena "prodNomb" (coincidencia exacta), en la columna nombre de la tabla "Productos".
    
    if not prodTupla:
        return True     # Retorna "verdadero" si no se econtró un producto.
    
    else:
        return False    # Retorna "falso" si se encontró un producto

def imprimir_producto(producto):    # Iprime un diccionario producto.
    amarilloTxt= Fore.YELLOW +">>"+Style.RESET_ALL
    
    print(
        f""" {amarilloTxt}  Producto: {producto.get("nombre")}\t\t\t\tID: {str(producto.get("id"))}
    \tCantidad: {str(producto.get("cantidad"))} ({str(producto.get("stockMin"))} mín)\tPrecio: ${producto.get("precio")}
    \tDescripción: {producto.get("descripcion")}
    \tCategoría: {producto.get("categoria")}\n"""
    )
    
    return

def convertir_a_producto(prodTupla):    # Conviente una tupla en un diccionario producto.
    producto["id"] = prodTupla[0]
    producto["nombre"] = prodTupla[1]
    producto["descripcion"] = prodTupla[2]
    producto["cantidad"] = prodTupla[3]
    producto["precio"] = prodTupla[4]
    producto["categoria"] = prodTupla[5]
    producto["stockMin"] = prodTupla[6]
    return producto

def imprimir_paqueteRegistros(paqueteRegistros):    # Imprime un lista de productos.
    
    for prodTupla in paqueteRegistros:
        imprimir_producto(convertir_a_producto(prodTupla))
    print(f"-- Productos totales: {len(paqueteRegistros)} .\n")
    
    return

from funciones_menu import *
from funciones_db import db_inventario_launcher

def main_menu():
    
    while True:
        db_inventario_launcher()

        opt = menu_ppal() # menu_ppal() Muestra el menú y devuelve la opción ingreasda por el usuario
        
        if opt[2] == "n":  # Ingresar nuevo producto
            ingresar_productos()

        elif opt[2] == "t":  # Mostrar todos los productos
            mostrar_prductos_todos()

        elif opt[2] == "a":  # Actualuzar cantidad de un producto
            actualizar_producto()

        elif opt[2] == "e":  # Eliminar un producto
            eliminar_producto()

        elif opt[2] == "b":  # Buscar productos
            buscar_productos()

        elif opt[3:6] == "x1b":  # Salir
            if salir() == True:
                break
        
        elif opt[2] == "s": # Mostrar productos con bajo stock
            mostrar_bajo_sotck()

        else:  # Opción no válida
            print(f"-- [{opt[2].upper()}] No es una opción válida.")

    print("-- Tenga un buen día!!!")
    return 0

main_menu()
 ::: Funcionalidades de la aplicación :::

[R] Registrar un NUEVO producto: Permite al usuario agregar nuevos productos al inventario.
	Datos solicitados: 
- Nombre: Texto, no nulo. No puede coincidir con el nombre de algún producto existente en el inventario. Nombre del producto.
- Descripción: Texto. Breve descripción del producto.
- Cantidad: Número, no nulo, positivo. Cantidad disponible del producto.
- Precio: Real, no nulo, positivo. Precio del producto.
- Categoría: Texto. Se selecciona de una lisa de categorías disponibles. Categoría a la que pertenece el producto.
- Stock mínimo: Número, no nulo, positivo. Cantidad mínima que se desea tener en el inventario.

 [T] Mostrar lista de TODOS los productos: Muestra todos los productos registrados en el inventario, incluyendo su ID, nombre, descripción, cantidad, precio, categoría, stock mínimo.

 [A] ACTUALIZAR la cantidad actual de un producto: Permite al usuario actualizar la cantidad disponible de un producto específico utilizando su ID.

- [1] Modificar cantidad actual: Se solicita al usuario una cantidad de producto y se establece esa cantidad como la cantidad actual del producto en el inventario.
- [2] Agregar/Quitar: Se solicita al usuario una cantidad y se agrega esa cantidad a la cantidad del producto registrada en el inventario. Permite ingresar cantidad negativa para descontar unidades del producto.  

 [E] ELIMINAR productos: Permite al usuario eliminar un producto del inventario utilizando su ID.

 [B] Para BUSCAR productos: Permite al usuario buscar productos, mostrando los resultados que coincidan con los criterios de búsqueda.

- [1] Buscar por ID: Se muestran los productos con el ID especificado por el usuario (coincidencia exacta).
- [2] Buscar por NOMBRE: Se muestran los productos que contengan  (todo o parte), del nombre especificado por el usuario.
- [3] Buscar por CATEGORÍA: Se muestran todos los productos que contengan la categoría especificada por el usuario

 [S] Mostrar productos con bajo STOCK: Generar un reporte de productos que tengan una cantidad igual o inferior a un límite especificado.

- [1] Mostrar indicando la cantidad MÍNIMA: Reporta los productos que tengan una cantidad igual o inferior al límite especificado por el usuario.
- [2] Mostrar según stock mínimo ingresado en el producto: Reporta los productos que tengan una cantidad igual o inferior al límite especificado por el dato "Stock mínimo" ingresado en el producto.

 [Esc] SALIR: Finaliza la aplicación. Requiere escribir "Salir" para confirmar finalización.
 
:: Se ejecutan las funcionalidades con sólo presionar la tecla encerrada por los corchetes [*] ::
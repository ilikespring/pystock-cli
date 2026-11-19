class Producto:
    """
    Modelo central para la gestion de articulos en inventario.
    """

    def __init__(self, nombre: str, precio: float, stock: int):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del articulo no puede estar vacio.")
        if not isinstance(precio, (int, float)) or isinstance(precio, bool) or precio < 0:
            raise ValueError("El precio unitario debe ser un numero mayor o igual a 0.")
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("El inventario inicial debe ser un entero mayor o igual a 0.")

        self.nombre = nombre.strip()
        self.precio = float(precio)
        self.stock = stock

    def mostrar_info(self):
        estado = "EN STOCK" if self.stock > 0 else "AGOTADO"
        subtotal = self.precio * self.stock
        print(f"  - {self.nombre:<25} | PVP: ${self.precio:>7.2f} | Stock: {self.stock:>4} uds | [{estado}] (Valor: ${subtotal:.2f})")

    def aplicar_descuento(self, porcentaje: float):
        try:
            if not isinstance(porcentaje, (int, float)) or isinstance(porcentaje, bool):
                raise TypeError("El porcentaje debe ser numerico.")
            if not (0 <= porcentaje <= 100):
                raise ValueError("El descuento debe estar entre 0% y 100%.")
            
            precio_anterior = self.precio
            self.precio -= self.precio * (porcentaje / 100)
            print(f"[OK] Descuento del {porcentaje}% aplicado a '{self.nombre}': ${precio_anterior:.2f} -> ${self.precio:.2f}")
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e}")

    def vender(self, cantidad: int):
        try:
            if not isinstance(cantidad, int) or isinstance(cantidad, bool):
                raise TypeError("La cantidad debe ser un numero entero.")
            if cantidad <= 0:
                raise ValueError("La cantidad a vender debe ser mayor a 0.")
            if cantidad > self.stock:
                print(f"[STOCK INSUFICIENTE] Disponible: {self.stock} uds | Solicitado: {cantidad} uds.")
                return
            
            self.stock -= cantidad
            total = cantidad * self.precio
            print(f"[VENTA] {cantidad}x '{self.nombre}' procesada. Total a cobrar: ${total:.2f}")
            
            if self.stock <= 3:
                print(f"[ALERTA] Stock critico para '{self.nombre}' ({self.stock} uds restantes).")
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e}")

    def reabastecer(self, cantidad: int):
        try:
            if not isinstance(cantidad, int) or isinstance(cantidad, bool):
                raise TypeError("La cantidad debe ser un numero entero.")
            if cantidad <= 0:
                raise ValueError("La cantidad a ingresar debe ser mayor a 0.")
            
            self.stock += cantidad
            print(f"[INGRESO] +{cantidad} uds agregadas a '{self.nombre}'. Stock actual: {self.stock} uds.")
        except (TypeError, ValueError) as e:
            print(f"[ERROR] {e}")


# =====================================================================
# INTERFAZ INTERACTIVA DE TERMINAL (CLI)
# =====================================================================

def leer_float(mensaje: str) -> float:
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("[ERROR] No se permiten valores negativos.")
                continue
            return valor
        except ValueError:
            print("[ERROR] Entrada invalida. Ingrese un numero (ej. 19.99).")

def leer_int(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("[ERROR] No se permiten valores negativos.")
                continue
            return valor
        except ValueError:
            print("[ERROR] Entrada invalida. Ingrese un numero entero (ej. 5).")

def seleccionar_producto(catalogo: dict):
    if not catalogo:
        print("\n[AVISO] El inventario esta vacio. Use la opcion 2 para registrar un producto primero.")
        return None
    
    print("\n--- Catalogo Actual ---")
    for sku, prod in catalogo.items():
        print(f"[{sku}] ", end="")
        prod.mostrar_info()
        
    sku = input("\nIngrese el codigo (SKU) del producto: ").strip().upper()
    if sku not in catalogo:
        print(f"[ERROR] No existe ningun producto con el codigo '{sku}'.")
        return None
    return catalogo[sku]

def iniciar_sistema():
    catalogo = {}

    while True:
        print("\n" + "=" * 55)
        print("   PYSTOCK CLI - GESTION DE INVENTARIO Y VENTAS")
        print("=" * 55)
        print("1. Ver inventario completo")
        print("2. Registrar nuevo producto")
        print("3. Procesar venta")
        print("4. Reabastecer stock")
        print("5. Aplicar descuento promocional")
        print("6. Salir")
        print("=" * 55)

        opcion = input("Seleccione una accion (1-6): ").strip()

        if opcion == "1":
            if not catalogo:
                print("\n[AVISO] El inventario esta vacio. Registre un producto en la opcion 2.")
            else:
                print("\n--- ESTADO DEL INVENTARIO ---")
                valor_total = 0
                for sku, prod in catalogo.items():
                    print(f"[{sku}] ", end="")
                    prod.mostrar_info()
                    valor_total += prod.precio * prod.stock
                print("-" * 55)
                print(f"Valor total de mercaderia en bodega: ${valor_total:.2f}")

        elif opcion == "2":
            print("\n--- NUEVO ARTICULO ---")
            sku = input("Asigne un codigo unico (ej. P01): ").strip().upper()
            if not sku or sku in catalogo:
                print("[ERROR] El codigo esta vacio o ya existe en el inventario.")
                continue
            try:
                nombre = input("Nombre del producto: ")
                precio = leer_float("Precio unitario ($): ")
                stock = leer_int("Stock inicial: ")
                catalogo[sku] = Producto(nombre, precio, stock)
                print(f"[OK] Producto '{nombre}' registrado bajo el codigo [{sku}].")
            except ValueError as e:
                print(f"[ERROR] {e}")

        elif opcion == "3":
            prod = seleccionar_producto(catalogo)
            if prod:
                cant = leer_int(f"Cantidad de '{prod.nombre}' a vender: ")
                prod.vender(cant)

        elif opcion == "4":
            prod = seleccionar_producto(catalogo)
            if prod:
                cant = leer_int(f"Cantidad de '{prod.nombre}' que ingresa a bodega: ")
                prod.reabastecer(cant)

        elif opcion == "5":
            prod = seleccionar_producto(catalogo)
            if prod:
                porc = leer_float(f"Porcentaje de descuento para '{prod.nombre}' (0-100): ")
                prod.aplicar_descuento(porc)

        elif opcion == "6":
            print("Cerrando sesion de inventario...")
            break
        else:
            print("[ERROR] Opcion no valida. Elija del 1 al 6.")

if __name__ == "__main__":
    iniciar_sistema()

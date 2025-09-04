import uuid
import csv
from Fechas import Tiempo
class CarroDeCompra:
    def pila_articulos():
        print("Articulos")
    def __init__(self, cliente):
        self.id_carrito = str(uuid.uuid4())
        self.cliente = cliente  
        self.items = []  
        self.fecha_creacion = Tiempo.Ahora()
        self.estado = "abierto"  

    def agregar_item(self, id_producto, nombre, cantidad, precio_unitario):
        subtotal = cantidad * precio_unitario
        self.items.append({
            "id_producto": id_producto,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })

    def eliminar_item(self, id_producto):
        self.items = [item for item in self.items if item["id_producto"] != id_producto]

    def actualizar_cantidad(self, id_producto, cantidad):
        for item in self.items:
            if item["id_producto"] == id_producto:
                item["cantidad"] = cantidad
                item["subtotal"] = cantidad * item["precio_unitario"]

    def calcular_total(self):
        return sum(item["subtotal"] for item in self.items)

    def mostrar_carrito(self):
        print(f"Carrito {self.id_carrito} - Cliente: {self.cliente.nombre}")
        for item in self.items:
            print(f"- {item['nombre']} x{item['cantidad']} = {item['subtotal']}")
        print(f"Total: {self.calcular_total()}")

    def vaciar_carrito(self):
        self.items.clear()

    def Parametros(self):
        return {
            "id_carrito": self.id_carrito,
            "id_cliente": self.cliente,
            "fecha_creacion": self.fecha_creacion,
            "total": self.calcular_total()
        }

    def Parametros_csv(self):
        return [
            {
                "id_carrito": self.id_carrito,
                "id_producto": item["id_producto"],
                "nombre": item["nombre"],
                "cantidad": item["cantidad"],
                "precio_unitario": item["precio_unitario"],
                "subtotal": item["subtotal"]
            }
            for item in self.items
        ]
    def to_dict(self):
        return {
            "id_carrito": self.id_carrito,
            "id_cliente": self.cliente.id_cliente,
            "fecha_creacion": str(self.fecha_creacion),
            "items": self.items
        }

    @staticmethod
    def from_dict(data, clientes=None):
        cliente = None
        if clientes:
            cliente = next((c for c in clientes if str(c.id_cliente) == str(data.get("id_cliente"))), None)
        else:
            cliente = data.get("id_cliente")  
        carrito = CarroDeCompra(cliente)
        carrito.id_carrito = data.get("id_carrito")
        carrito.fecha_creacion = data.get("fecha_creacion")
        carrito.items = data.get("items", [])
        return carrito

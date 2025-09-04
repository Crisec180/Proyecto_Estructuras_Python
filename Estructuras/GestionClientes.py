import csv
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
clases_base_path = os.path.join(current_dir, "Clases_Base")
sys.path.append(clases_base_path)
from Clases_Base.Cliente import Cliente
from Archivos.PersistenciaDatos import Archivo as file

class GestionClientes:
    def __init__(self, archivo_clientes):
        self.archivo_clientes = archivo_clientes
        self.clientes = []
        self.cargar_clientes()
             
    def cargar_clientes(self):
        self.clientes = file.cargar_clientes()

    def guardar_clientes(self):
        file.guardar_clientes(self.clientes)

    @staticmethod
    def formatear_id(id_cliente):
        if id_cliente is None:
            return "N/A"
        
        id_str = str(id_cliente)
        if len(id_str) > 10:
            return id_str[:8] + "..."
        return id_str
    
    def registrar_cliente(self, nombre, id, password, apellido, telefono, correo, direccion_envio, fecha_registro):
        for c in self.clientes:
            if c.id_cliente == id:  
                return False
            
        nuevo_cliente = Cliente(
            nombre=nombre, 
            apellido=apellido, 
            telefono=telefono, 
            correo=correo, 
            direccion_envio=direccion_envio, 
            id_cliente=id, 
            fecha_registro=fecha_registro, 
            password=password
        )
        self.clientes.append(nuevo_cliente)
        self.guardar_clientes()
        return True
    
    def login(self, id, password):
        for c in self.clientes:
            if c.id_cliente == id and c.password == password:
                return c
        return None
         
    def eliminar_cliente(self, id, password):
        for c in self.clientes:
            if c.id_cliente == id and c.password == password:
                self.clientes.remove(c)
                self.guardar_clientes()
                return True
        return False





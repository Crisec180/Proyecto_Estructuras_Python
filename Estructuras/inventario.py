#La lista va a manejar pilas de articulos iguales

class PilaArticulos:
    def __init__(self):
        self.items = []

    def apilar(self, items):
       self.items.append(items)

    def desapilar(self):
        #si no hay items
        if not self.items:
            return None
        #si, si hay
        return self.items.pop()
    
    def __str__(self):
        return f" Articulos apilados: {len(self.items)}"
    
class Nodo:
    def __init__(self, articulo):
        self.dato = articulo
        self.pila = PilaArticulos()  # Cada nodo tiene su propia pila de artículos
        #copia los articulos en la pila por la cantidad ingresada
        for _ in range(articulo.cantidad):
            self.pila.apilar(articulo)

        self.siguiente = None #ve la pila siguiente
        self.anterior = None  #ve la pila anterior
       
#lista doblemente enlazada para mas practicidad
class ListaInventario:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.primero = None
            cls._instancia.ultimo = None
        return cls._instancia
    
    def __init__(self):
        if not hasattr(self, 'primero'):    
            self.primero = None
            self.ultimo = None
        
    def agregar_articulo(self, articulo):
        """
        Agrega un artículo al inventario.
        Retorna True si se agrega exitosamente, False si ya existe.
        """
        # Verificar si el artículo ya existe
        if self.existe_articulo(articulo.nombre):
            return False  # El artículo ya existe
        
        nuevo_nodo = Nodo(articulo)
        if not self.primero:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.ultimo
            self.ultimo = nuevo_nodo
        return True  # Artículo agregado exitosamente
        
    def existe_articulo(self, nombre):
        """
        Verifica si un artículo ya existe en el inventario.
        Retorna True si existe, False si no existe.
        """
        actual = self.primero
        while actual:
            if actual.dato.nombre.lower().strip() == nombre.lower().strip():
                return True
            actual = actual.siguiente
        return False

    #Clase basica para mostrar que es doble:
    def mostrar_articulos(self):
        actual = self.primero
        while actual:
            print(actual.dato)        
            print(actual.pila)        
            print(" -----------\n")
            actual = actual.siguiente

    #para que sirve este metodo?
    #debido a que se manejan pilas de articulos copia, este metodo permite obtener una lista de nodos
    #en otras palabras agarrar toda la pila
    @staticmethod
    def pasar_a_lista_nodos(lista_inventario):
        nodos = []
        actual = lista_inventario.primero
        while actual:
            nodos.append(actual)
            actual = actual.siguiente
        return nodos
    
    #metodos de ordenamiento selecction sort
    @staticmethod  #metodo para llamar sin instancia lo que seria un STATIC en c++
    def ordenarPorCantidad(lista_nodos):
        ordenada = []
        copia = lista_nodos[:] #copia la lista original
        while copia:
            menor = copia[0]
            for item in copia:
                if len(item.pila.items) < len(menor.pila.items): # Compara la can de articulos
                    menor = item
            ordenada.append(menor)
            copia.remove(menor)
        return ordenada

    @staticmethod
    def ordenarPorPrecios(lista_nodos):
        ordenada = []
        copia = lista_nodos[:]
        while copia:
            menor = copia[0]
            for item in copia:
                if item.dato.precio < menor.dato.precio:
                    menor = item
            ordenada.append(menor)
            copia.remove(menor)
        return ordenada

    @staticmethod
    def ordenarAlfabeticamente(lista_nodos):
        ordenada = []
        copia = lista_nodos[:]
        while copia:
            menor = copia[0]
            for item in copia:
                if item.dato.nombre.lower() < menor.dato.nombre.lower():
                    menor = item
            ordenada.append(menor)
            copia.remove(menor)
        return ordenada

    #metodo de busqueda
    def buscar_articulo_nombre(self, nombre):
        actual = self.primero
        while actual:
            if actual.dato.nombre.lower() == nombre.lower():
                return actual.pila
            actual = actual.siguiente
        return None
    
    def buscar_articulo_tipo(self, tipo):
        actual = self.primero
        while actual:
            if actual.dato.tipo.lower() == tipo.lower():
                return actual.dato
            actual = actual.siguiente
        return None
    
    #este metodo esta hecho para que solo elimine despues de completar con exito la compra
    def eliminar_articulo(self, nombre, cantidad=None):
       """Elimina un artículo del inventario.
          Si no se especifica cantidad, elimina el nodo completo.
          Si se especifica cantidad, elimina esa cantidad de la pila.
        Retorna True si se elimina exitosamente, False si no se encuentra."""
                                                                    
       actual = self.primero
       while actual:
           if actual.dato.nombre.lower().strip() == nombre.lower().strip():
               if cantidad is None:
                    if actual.anterior:
                        actual.anterior.siguiente = actual.siguiente
                    else:
                        self.primero = actual.siguiente
                
                    if actual.siguiente:
                        actual.siguiente.anterior = actual.anterior
                    else:
                        self.ultimo = actual.anterior
                
                    print(f"DEBUG - Nodo eliminado completamente: {nombre}")
                    return True
               else:
                # Eliminar cantidad específica
                    stock_inicial = len(actual.pila.items)
                    print(f"DEBUG - {nombre}: Stock inicial = {stock_inicial}")
                    print(f"DEBUG - Cantidad a eliminar solicitada = {cantidad}")
                
                # Validar que hay suficiente stock
                    if cantidad > stock_inicial:
                         print(f"DEBUG - ERROR: No hay suficiente stock. Stock: {stock_inicial}, Solicitado: {cantidad}")
                         return False
                
                # Eliminar la cantidad solicitada
                    cantidad_eliminada = 0
                    for _ in range(min(cantidad, len(actual.pila.items))):
                        if actual.pila.items:  # Verificar que aún hay items
                            actual.pila.desapilar()
                            cantidad_eliminada += 1
                
                    stock_final = len(actual.pila.items)
                    print(f"DEBUG - {nombre}: Cantidad eliminada = {cantidad_eliminada}")
                    print(f"DEBUG - {nombre}: Stock final = {stock_final}")
                
                # Si la pila quedó vacía, eliminar el nodo completo
                    if not actual.pila.items:
                         print(f"DEBUG - {nombre}: Pila vacía, eliminando nodo completo")
                         if actual.anterior:
                             actual.anterior.siguiente = actual.siguiente
                         else:
                             self.primero = actual.siguiente
                    
                         if actual.siguiente:
                             actual.siguiente.anterior = actual.anterior
                         else:
                             self.ultimo = actual.anterior
                
                    return True
        
           actual = actual.siguiente
    
       print(f"DEBUG - ERROR: Producto '{nombre}' no encontrado en inventario")
       return False
    
    def eliminar_uno(self, nombre):
        actual = self.primero
        if not self.verificar_cantidad_articulo(nombre, 1):
            print("No hay suficientes artículos en la pila.")
            return False
        else:
            while actual:
                if actual.dato.nombre.lower() == nombre.lower():
                    actual.pila.desapilar()
                    if not actual.pila.items:
                        if actual.anterior:
                            actual.anterior.siguiente = actual.siguiente
                        else:
                            self.primero = actual.siguiente
                        if actual.siguiente:
                            actual.siguiente.anterior = actual.anterior
                        else:
                            self.ultimo = actual.anterior
                    return True
                actual = actual.siguiente
        return False
    
    def contar_productos(self):
        #"""Contar productos recorriendo directamente los nodos"""
        contador = 0
        actual = self.primero
        
        while actual is not None:
            contador += 1
            actual = actual.siguiente
            
        return contador
    #Este metodo comprueba la cantidad de la pila para evitar que el usuario 
    #intente comprar mas de los que hay 
    def verificar_cantidad_articulo(self, nombre, cantidad):
        actual = self.primero
        while actual:
            if actual.dato.nombre.lower() == nombre.lower():
                return len(actual.pila.items) >= cantidad
            actual = actual.siguiente
        return False
        
    def verificar_cantidad_articulo(self, nombre, cantidad):
        actual = self.primero
        while actual:
            if actual.dato.nombre.lower() == nombre.lower():
                return len(actual.pila.items) >= cantidad
            actual = actual.siguiente
        return False
        
    #recursividad y asintotico
    def ordenar_recursivamente_por_tipo(self, tipo, nodo=None):
        if nodo is None:
            nodo = self.primero
        if nodo is None:
            return None
        if nodo.dato.tipo.lower() == tipo.lower():
            return nodo.pila
        return self.busqueda_recursiva(tipo, nodo.siguiente)
    
    def mostrar_articulos_recursivo(self, nodo=None):
        if nodo is None:
            nodo = self.primero
        if nodo is None:
            return
        print("Mostrando artículos recursivamente por tipo:")
        print(nodo.dato)        
        print(nodo.pila)        
        print(" -----------\n")
        self.mostrar_articulos_recursivo(nodo.siguiente)

    #tiempo constante
    def primer_articulo(self):
        if self.primero:
            return self.primero.dato
        return None
    
    #tiempo lineal
    def contar_articulos(self):
        contador = 0
        actual = self.primero
        while actual:
            contador += len(actual.pila.items)
            actual = actual.siguiente
        return contador
    
    def lista_a_arreglo(self):
        productos = []
        actual = self.primero
        while actual:
            productos.append(actual)
            actual = actual.siguiente
        return productos
    
    def mostar_articulos_arreglo(self, arreglo):
        for nodo in arreglo:
            print(nodo.dato)
            print(nodo.pila)
            print(" -----------\n")

#----------------------------------------------------
    #metodo de ordenamiento merge sort
    def ordenar_simple_merge_sort(self, lista_nodos=None):
        if lista_nodos is None:
            datos = []
            actual = self.primero
            while actual:
                datos.append(actual.dato)
                actual = actual.siguiente
        
            datos_ordenados = self.merge_sort_datos(datos)
            self.reconstruir_con_datos(datos_ordenados)
            return  
    
    # Si recibe lista_nodos (para interfaz gráfica)
        else:
            datos = [nodo.dato for nodo in lista_nodos]
            datos_ordenados = self.merge_sort_datos(datos)
        
        # Retornar nodos ordenados
            nodos_ordenados = []
            for dato_ordenado in datos_ordenados:
                for nodo in lista_nodos:
                    if nodo.dato is dato_ordenado:
                        nodos_ordenados.append(nodo)
                        break
            return nodos_ordenados

    def merge_sort_datos(self, datos):
        #implementacion recursiva
        #solo uno o ningun elemento
        if len(datos) <= 1:
           return datos

        mitad = len(datos) // 2
        izquierda = self.merge_sort_datos(datos[:mitad]) #recursividad
        derecha = self.merge_sort_datos(datos[mitad:])   #recursividad
        #tambien se hace log(n)

        return self.merge_datos(izquierda, derecha)

    def merge_datos(self, izquierda, derecha):
        #se hace una notacion n/2
        resultado = []
        i = j = 0
    
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i].precio <= derecha[j].precio:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
    
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado

    def reconstruir_con_datos(self, datos_ordenados):
        self.primero = None
        self.ultimo = None
        for dato in datos_ordenados:
            #se agrega cada articulo en orden
            self.agregar_articulo(dato)

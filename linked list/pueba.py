from MyLinkedList import MyLinkedList

lista = MyLinkedList()

lista.insertar_inicio(10)
lista.insertar_inicio(5)
lista.insertar_final(20)

print("Lista:", lista.mostrar())

lista.eliminar(10)
print("Después de eliminar 10:", lista.mostrar())

print("¿Existe 20?", lista.buscar(20))
print("Tamaño:", lista.tamaño())
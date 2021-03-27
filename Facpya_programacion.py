
import pandas as pd
from tabulate import tabulate

v_conjunto_tickets = []
v_num_ticket = 1

def nuevoItem():
    descripcion=input("Que desea comprar:")
    precio=int(input("Indique el precio del producto:"))
    cantidad=int(input("Cuantas piezas se estan comprando:"))
    total = precio * cantidad
    v_conjunto_tickets.append([v_num_ticket, descripcion, precio, cantidad, total])
    return [descripcion, precio, cantidad, total]
def registrarVenta():
    global v_num_ticket
    v_ticket = []
    v_lista = []
    v_lista.append(nuevoItem())
    while True:
        accion = input("¿Desea agregar algo más? S/N")
        if accion.upper() == "S":
            v_lista.append(nuevoItem())
        else:
            v_num_ticket = v_num_ticket + 1
            v_ticket = pd.DataFrame(v_lista, columns = ['Producto' , 'Precio', 'Cantidad','Total'])
            total_final = v_ticket['Total'].sum()
            print(tabulate(v_ticket, headers = ("Compra", "Producto", "Precio", "Cantidad", "Total")))
            print(f'Su total es:....................................{total_final}')
            break
def buscarTicket():
    ticket = int(input("Qué ticket desea ver? "))
    v_ticket_buscado = []
    for i in v_conjunto_tickets:
        if i[0] == ticket:
            v_ticket_buscado.append(i)
    v_df_buscado = pd.DataFrame(v_ticket_buscado, columns = ['Ticket', 'Producto' , 'Precio', 'Cantidad','Total'])
    total_buscado = v_df_buscado['Total'].sum()

    print(tabulate(v_df_buscado, headers = ("Elemento", "Ticket", "Producto", "Precio", "Cantidad", "Total")))
    print(f'Total del ticket:....................................{total_buscado}')
def Menu_Principal():
    while True:
        print("Opcion 1.- Registrar una venta")
        print("Opcion 2.- Consultar Venta")
        print("Opción 3.- Salir")
        respuesta = int(input("Elige una opción: "))
        if respuesta == 1:
            registrarVenta()
        elif respuesta == 2:
            buscarTicket()
        elif respuesta == 3:
            print("Saliendo...")
            break
        else:
            print("Opcion invalida\n")

Menu_Principal()

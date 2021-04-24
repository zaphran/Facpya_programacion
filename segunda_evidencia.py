import pandas as pd
import os
import datetime


def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

while True:
    borrarPantalla()
    print("1. Registrar una venta \n"
    "2. Consultar una venta \n"
    "3. Obtener reporte de ventas \n"
    "4. Salir")
    opcion = int(input("Elegir una opcion: "))
    if opcion == 1:
        borrarPantalla()
        archivo = "ventas.csv"
        carrito = {}
        descs = []
        cants = []
        precios = []
        total = 0
        fechaCapturada = input("Fecha de venta DD/MM/AAAA: ")
        fechaProcesada = datetime.datetime.strptime(fechaCapturada, "%d/%m/%Y").date()
        while True:
            desc = input("Descripcion del articulo: ")
            cant = int(input("Cantidad de piezas: "))
            precioU = int(input("Precio unitario: "))
            precio = cant * precioU
            total = total + precio

            cants.append(cant)
            descs.append(desc)
            precios.append(precio)

            while True:
                finalizar = input("¿Finalizar venta? [Y/N]: ")
                if finalizar.upper() == "Y" or finalizar.upper() == "N":
                    break
                else:
                    print("Opcion invalida")

            if finalizar.upper() == "Y":
                borrarPantalla()
                if os.path.isfile(archivo):
                    leerCSV = pd.read_csv('ventas.csv', header=0)
                    folio = leerCSV.iloc[-1]['Folio']
                    folio = folio + 1
                    carrito['Folio'] = folio

                else:
                    carrito['Folio'] = 1

                carrito['Cantidad'] = cants
                carrito['Descripcion'] = descs
                carrito['Precio'] = precios

                df = pd.DataFrame(carrito)
                df['Fecha'] = fechaProcesada
                print(df)
                print(f"TOTAL: {total} \n")

                if os.path.isfile(archivo):
                    df.to_csv('ventas.csv', index=False, header=False, mode='a+')
                else:
                    df.to_csv('ventas.csv', index=False, mode='w')
                    print("Se ha creado el archivo csv")
                print("Se ha guardado la venta en el archivo csv")
                input("--Presione ENTER para continuar--")
                break

    elif opcion == 2:
        borrarPantalla()
        if os.path.isfile('ventas.csv'):
            folioConsulta = int(input("Ingrese folio de venta: "))
            leerCSV = pd.read_csv('ventas.csv', header=0)
            coincidencia = leerCSV[leerCSV['Folio'] == folioConsulta]
            if coincidencia.empty:
                print("No existe una venta asociada al folio")
            else:
                print(coincidencia)
            input("--Presione ENTER para continuar--")
        else:
            print("No existen registros")
            input("--Presione ENTER para continuar--")

    elif opcion == 3:
        borrarPantalla()
        if os.path.isfile('ventas.csv'):
            fechaConsulta = input("Ingrese fecha a consultar AAAA-MM-DD: ")
            leerCSV = pd.read_csv('ventas.csv', header=0)
            reporte = leerCSV[leerCSV['Fecha'] == fechaConsulta]
            if reporte.empty:
                print("No se encontraron ventas asociadas a la fecha")
            else:
                print(reporte)
            input("--Presione ENTER para continuar--")
        else:
            print("No existen registros")
            input("--Presione ENTER para continuar--")

    elif opcion == 4:
        break

    else:
        print("Opcion invalida")
        input("--Presione ENTER para continuar--")

import datetime
import os
import pandas as pd
import re
import sqlite3
from sqlite3 import Error
import sys

p_espacios = r"^(\s*)$"
p_intPositivo = r"^\d+$"
p_floatPositivo = r"^\d*\.?\d+$"

def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

def enter():
    input("--Presione ENTER para continuar--")

try:
    with sqlite3.connect("TiendaCosmeticos.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS VENTA (Folio INTEGER PRIMARY KEY, VentaDetalle TEXT NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS VENTA_DETALLE (IdVenta INTEGER NOT NULL, Cantidad INTEGER NOT NULL, Descripcion TEXT NOT NULL, PrecioUnitario FLOAT NOT NULL, PrecioTotal FLOAT NOT NULL, Fecha TIMESTAMP NOT NULL);")
        print("Tablas creadas exitosamente")
except Error as e:
    print(e)
    enter()
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    enter()
finally:
    conn.close()

def folioGenerator():
    try:
        with sqlite3.connect("TiendaCosmeticos.db") as conn:
            cur_folio = conn.cursor()
            cur_folio.execute("SELECT count(Folio) FROM VENTA")
            registro = cur_folio.fetchall()
            row = registro[0][0]

            if row != 0:
                folio = row + 1
                return folio
            else:
                folio = 1
                return folio
    except Error as e:
        print(e)
        enter()
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        enter()
    finally:
        if (conn):
            conn.close()

while True:
    borrarPantalla()
    print("-- Menu Principal --\n"
    "1. Registrar una venta \n"
    "2. Consultar ventas de un dia especifico \n"
    "3. Salir")
    try:
        opcion = int(input("Elegir una opcion: "))
    except:
        print("Opcion invalida")
        enter()
    else:
        if opcion == 1:
            borrarPantalla()
            carrito = {}
            descs = []
            cants = []
            preciosU = []
            preciosT = []
            total = 0
            while True:
                while True:
                    borrarPantalla()
                    desc = input("Descripcion del articulo: ")
                    if re.match(p_espacios, desc):
                        print("Entrada invalida")
                        enter()
                    else:
                        break

                while True:
                    borrarPantalla()
                    _cant = input("Cantidad de piezas: ")
                    if re.match(p_intPositivo, _cant) and _cant != "0":
                        cant = int(_cant)
                        break
                    else:
                        print("Entrada invalida")
                        enter()

                while True:
                    borrarPantalla()
                    _precioU = input("Precio de venta: ")
                    if re.match(p_floatPositivo, _precioU) and _precioU != "0":
                        precioU = float(_precioU)
                        break
                    else:
                        print("Entrada invalida")
                        enter()

                precioT = cant * precioU
                total = total + precioT

                cants.append(cant)
                descs.append(desc)
                preciosU.append(precioU)
                preciosT.append(precioT)

                while True:
                    borrarPantalla()
                    finalizar = input("¿Finalizar venta? [Y/N]: ")
                    if finalizar.upper() == "Y" or finalizar.upper() == "N":
                        break
                    else:
                        print("Opcion invalida")
                        enter()

                if finalizar.upper() == "Y":
                    borrarPantalla()
                    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    folio = folioGenerator()
                    carrito['Folio'] = folio
                    carrito['Cantidad'] = cants
                    carrito['Descripcion'] = descs
                    carrito['Precio Unitario'] = preciosU
                    carrito['Precio Total'] = preciosT
                    df = pd.DataFrame(carrito)
                    df['Fecha'] = fecha_actual
                    print(df)
                    print("TOTAL: ${:.2f} \n".format(total))

                    i = 0
                    s_folio = str(folio)
                    s_fecha = datetime.datetime.now().strftime("%d%m%Y")
                    IdVenta = s_folio + '-' + s_fecha
                    try:
                        with sqlite3.connect("TiendaCosmeticos.db") as conn:
                            for articulo in descs:
                                cur_ventaDetalle = conn.cursor()
                                ventaDetalle_valores = {"IdVenta":IdVenta, "Cantidad":cants[i], "Descripcion": descs[i], "PrecioUnitario": preciosU[i], "PrecioTotal": preciosT[i],"Fecha": fecha_actual}
                                cur_ventaDetalle.execute("INSERT INTO VENTA_DETALLE VALUES(:IdVenta,:Cantidad,:Descripcion,:PrecioUnitario,:PrecioTotal,:Fecha)", ventaDetalle_valores)
                                i = i + 1

                            cur_venta = conn.cursor()
                            venta_valores = {"Folio":folio, "VentaDetalle":IdVenta}
                            cur_venta.execute("INSERT INTO VENTA VALUES(:Folio,:VentaDetalle)", venta_valores)
                    except Error as e:
                        print(e)
                        enter()
                    except:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                        enter()
                    finally:
                        if (conn):
                            conn.close()
                    print("Venta agregada exitosamente")
                    enter()
                    break

        elif opcion == 2:
            borrarPantalla()
            carrito = {}
            descs = []
            cants = []
            preciosU = []
            preciosT = []
            folios = []
            i = 0
            try:
                fecha_consultar = input("Ingrese fecha a consultar (dd/mm/aaaa): ")
                fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
                with sqlite3.connect("TiendaCosmeticos.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                    cur_fecha = conn.cursor()
                    values = {"Fecha":fecha_consultar}
                    cur_fecha.execute("SELECT b.Folio, a.Cantidad, a.Descripcion, a.PrecioUnitario, a.PrecioTotal FROM VENTA_DETALLE AS a INNER JOIN VENTA AS b ON a.IdVenta = b.VentaDetalle WHERE DATE(a.Fecha) = :Fecha;", values)
                    registros = cur_fecha.fetchall()

                    if registros:
                        for venta in registros:
                            folios.append(registros[i][0])
                            cants.append(registros[i][1])
                            descs.append(registros[i][2])
                            preciosU.append(registros[i][3])
                            preciosT.append(registros[i][4])
                            i = i + 1

                        carrito['Folio'] = folios
                        carrito['Cantidad'] = cants
                        carrito['Descripcion'] = descs
                        carrito['PrecioUnitario'] = preciosU
                        carrito['PrecioTotal'] = preciosT

                        df = pd.DataFrame(carrito)

                        cur_totalf = conn.cursor()
                        cur_totalf.execute("SELECT SUM(PrecioTotal) FROM VENTA_DETALLE WHERE DATE(Fecha) = :Fecha;", values)
                        total_fecha = cur_totalf.fetchall()

                        borrarPantalla()
                        print(f"Reporte de ventas para el dia: {fecha_consultar}")
                        print(df)
                        print("TOTAL VENDIDO: ${:.2f} \n".format(total_fecha[0][0]))
                    else:
                        print("No se encontraron ventas asociadas a la fecha")
                    enter()
            except Error as e:
                print(e)
                enter()
            except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                enter()

        elif opcion == 3:
            print("--Fin del programa--")
            break

        else:
            print("Opcion invalida")
            enter()

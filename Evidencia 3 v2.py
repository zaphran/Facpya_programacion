import pandas as pd
import os
import sys
import datetime
import sqlite3
from sqlite3 import Error

def borrarPantalla():
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")

try:
    with sqlite3.connect("Evidencia3.db") as conn:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS VENTA (Folio INTEGER PRIMARY KEY, VentaDetalle TEXT NOT NULL);")
        c.execute("CREATE TABLE IF NOT EXISTS VENTA_DETALLE (IdVenta INTEGER NOT NULL, Cantidad INTEGER NOT NULL, Descripcion TEXT NOT NULL, PrecioUnitario FLOAT NOT NULL, PrecioTotal FLOAT NOT NULL, Fecha TIMESTAMP NOT NULL);")
        print("Tabla creada exitosamente")
except Error as e:
    print (e)
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    conn.close()

def folioGenerator():
    try:
        with sqlite3.connect("Evidencia3.db") as conn:
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
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()

while True:
    borrarPantalla()
    print("1. Registrar una venta \n"
    "2. Consultar una venta \n"
    "3. Obtener reporte de ventas \n"
    "4. Salir")
    opcion = int(input("Elegir una opcion: "))
    if opcion == 1:
        borrarPantalla()
        carrito = {}
        descs = []
        cants = []
        preciosU = []
        preciosT = []
        total = 0
        fechaCapturada = input("Fecha de venta DD/MM/AAAA: ")
        fechaCapturada = datetime.datetime.strptime(fechaCapturada, "%d/%m/%Y").date()
        fecha_actual = datetime.datetime.combine(fechaCapturada, datetime.datetime.min.time())
        while True:
            desc = input("Descripcion del articulo: ")
            cant = int(input("Cantidad de piezas: "))
            precioU = float(input("Precio unitario: "))
            precioT = cant * precioU
            total = total + precioT

            cants.append(cant)
            descs.append(desc)
            preciosU.append(precioU)
            preciosT.append(precioT)

            while True:
                finalizar = input("¿Finalizar venta? [Y/N]: ")
                if finalizar.upper() == "Y" or finalizar.upper() == "N":
                    break
                else:
                    print("Opcion invalida")

            if finalizar.upper() == "Y":
                borrarPantalla()
                folio = folioGenerator()

                carrito['Folio'] = folio
                carrito['Cantidad'] = cants
                carrito['Descripcion'] = descs
                carrito['Precio Unitario'] = preciosU
                carrito['Precio Total'] = preciosT

                df = pd.DataFrame(carrito)
                df['Fecha'] = fecha_actual
                print(df)
                print(f"TOTAL: {total} \n")

                i = 0
                s_folio = str(folio)
                s_fecha = fecha_actual.strftime("%d%m%Y")
                IdVenta = s_folio + '-' + s_fecha
                try:
                    with sqlite3.connect("Evidencia3.db") as conn:
                        for articulo in descs:
                            cur_ventaDetalle = conn.cursor()
                            ventaDetalle_valores = {"IdVenta":IdVenta, "Cantidad":cants[i], "Descripcion": descs[i], "PrecioUnitario": preciosU[i], "PrecioTotal": preciosT[i],"Fecha": fecha_actual}
                            cur_ventaDetalle.execute("INSERT INTO VENTA_DETALLE VALUES(:IdVenta,:Cantidad,:Descripcion,:PrecioUnitario,:PrecioTotal,:Fecha)", ventaDetalle_valores)
                            i = i + 1

                        cur_venta = conn.cursor()
                        venta_valores = {"Folio":folio, "VentaDetalle":IdVenta}
                        cur_venta.execute("INSERT INTO VENTA VALUES(:Folio,:VentaDetalle)", venta_valores)
                except Error as e:
                    print (e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    if (conn):
                        conn.close()
                print("Venta agregada exitosamente")
                input("--Presione ENTER para continuar--")
                break

    elif opcion == 2:
        borrarPantalla()
        folioConsulta = int(input("Ingrese folio de venta: "))
        try:
            with sqlite3.connect("Evidencia3.db") as conn:
                query = '''SELECT a.Folio, b.Cantidad, b.Descripcion, b.PrecioUnitario, b.PrecioTotal, Date(b.Fecha) as Fecha
                FROM VENTA AS a
                INNER JOIN VENTA_DETALLE AS b ON a.VentaDetalle = b.IdVenta
                WHERE a.Folio = {}
                '''
                df = pd.read_sql_query(query.format(folioConsulta), conn)

                if df.empty:
                    print("No existe una venta asociada al folio")
                    input("--Presione ENTER para continuar--")
                else:
                    print(df)
                    input("--Presione ENTER para continuar--")
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

    elif opcion == 3:
        borrarPantalla()
        carrito = {}
        descs = []
        cants = []
        preciosU = []
        preciosT = []
        folios = []
        i = 0
        fecha_consultar = input("Ingrese fecha a consultar (dd/mm/aaaa): ")
        fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
        try:
            with sqlite3.connect("Evidencia3.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
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

                    borrarPantalla()
                    print(f"Reporte de ventas para el dia: {fecha_consultar}")
                    print(df)
                else:
                    print("No se encontraron ventas asociadas a la fecha")
                input("--Presione ENTER para continuar--")
        except Error as e:
            print (e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            input("--Presione ENTER para continuar--")

    elif opcion == 4:
        print("--Fin del programa--")
        break

    else:
        print("Opcion invalida")
        input("--Presione ENTER para continuar--")

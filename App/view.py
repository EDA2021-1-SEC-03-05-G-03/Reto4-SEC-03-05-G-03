"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import threading
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack
assert cf


connectionsFile = 'connections.csv'
countriesFile = 'countries.csv'
landingPointsFile = 'landing_points.csv'


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("\n*******************************************")
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- Cantidad de clústeres dentro de la red de cables submarinos y si dos landing points pertenecen o no al mismo clúster. - req1")
    print("2- Landing point(s) que sirven como punto de interconexión a más cables en la red.  - req2")
    print("3- Ruta mínima en distancia para enviar información entre dos países - req3")
    print("4- Infraestructura crítica para poder garantizar el mantenimiento preventivo del mismo - req4")
    print("5- Impacto que tendría el fallo de un determinado landing point que afecta todos los cables conectados al mismo - req5")
    print("6- Ancho de banda máximo que se puede garantizar para la transmisión (Bono)   - req6")
    print("7- Ruta mínima en número de saltos para enviar información entre dos direcciones IP dadas. (Bono)   - req7")
    print("8- Graficando los grafos (Bono)   - req8")
    print("*******************************************")

catalog = None

"""
Menu principal
"""

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 0:
            print("Cargando información de los archivos ....")
            cont = controller.init()

            print("Preparando Carga de Landing Points...")
            controller.loadLandingPoints(cont, landingPointsFile)
            print("Landing Points Cargados!")

            print("Preparando Carga de Connections...")
            controller.loadConnections(cont, connectionsFile)
            print("Connections Cargados!")

            print("Preparando Carga de Paises...")
            controller.loadCountries(cont, countriesFile)
            print("Paises Cargados!")

            numedges = controller.totalConnections(cont)
            numvertex = controller.totalLandingPoints(cont)
            numpaises = controller.totalCountries(cont)
            print('Numero de vertices (Landing Points): ' + str(numvertex))
            print('Numero de arcos (Connections): ' + str(numedges))
            print('Numero de Paises Cargados (Countries): ' + str(numpaises))

            print('Primer Landing Point Cargado: ' + str(controller.firstLandingPoint(cont)))
            print('Ultimo Country Cargado: ' + str(controller.lastLoadedCountry(cont)))

            print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))

        elif int(inputs[0]) == 1:
            pass

        elif int(inputs[0]) == 2:
            tuplaMostConnected = controller.mostConnectedLandingPoints(cont)
            arrayLandingPoints = tuplaMostConnected[0]
            maxDegree = tuplaMostConnected[1]

            for landing in arrayLandingPoints:
                print('• ' + str(landing['landing_point_id']) + ' - ' + str(landing['id']) + ' - ' + str(landing['name']))
            print('^ Cables conectados: ' + str(maxDegree))

        elif int(inputs[0]) == 3:
            inicio = str(input("Ingrese el pais de inicio: "))
            final = str(input("Ingrese el pais de llegada: "))
            resultado = controller.camino_mas_corto(cont, inicio, final)
            print(resultado)
            #print(resultado["VertexA"] + "-->" + resultado["VertexB"] + " costo: " + str(resultado["weight"]))
            

        elif int(inputs[0]) == 4:
            pass

        elif int(inputs[0]) == 5:
            pass

        elif int(inputs[0]) == 6:
            pass

        elif int(inputs[0]) == 7:
            pass

        elif int(inputs[0]) == 8:
            pass

        else:
            sys.exit(0)
    sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
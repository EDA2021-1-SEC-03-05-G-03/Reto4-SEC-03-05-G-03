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


servicefile = 'connections.csv'
servicefile2 = 'countries.csv'
servicefile3 = 'landing_points.csv'


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
    print("1- Identificar los clusteres de informacion     - req1")
    print("2- Identificar los puntos de conexion criticos  - req2")
    print("3- Identificar la ruta de menor distancia       - req3")
    print("4- Identificar la infraestructura critica       - req4")
    print("5- Analisis de fallas                           - req5")
    print("6- Los mejores canales para transmitir (Bono)   - req6")
    print("7- La mejor ruta para comunicarme      (Bono)   - req7")
    print("8- Graficando los grafos               (Bono)   - req8")
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
            controller.loadServices(cont, servicefile)
            controller.loadServices2(cont, servicefile2)
            controller.loadServices3(cont, servicefile3)
            numedges = controller.totalConnections(cont)
            numvertex = controller.totalStops(cont)
            print('Numero de vertices: ' + str(numvertex))
            print('Numero de arcos: ' + str(numedges))
            print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))

        elif int(inputs[0]) == 1:
            pass

        elif int(inputs[0]) == 2:
            pass

        elif int(inputs[0]) == 3:
            pass

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
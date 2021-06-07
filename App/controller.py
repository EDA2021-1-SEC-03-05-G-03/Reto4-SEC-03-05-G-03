"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import time
import tracemalloc
import config as cf
import model
import csv
from datetime import datetime

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Funciones para calcular el tiempo

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en kBytes (ej.: 2100.0 kB)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0
    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory


# Inicialización del Catálogo 

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

def cargar_conecciones(analyzer, connectionsFile):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    datos = loadConnections(analyzer, connectionsFile)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return datos, delta_time, delta_memory

def loadConnections(analyzer, connectionsFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    """
    file = cf.data_dir + connectionsFile
    input_file = csv.DictReader(open(file, encoding='utf-8-sig'),
                                delimiter=",")
    for connection in input_file:
        model.addLandingPointConnection(analyzer, connection)
    return analyzer

def loadCountries(analyzer, countriesFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    """
    file = cf.data_dir + countriesFile
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    lastCountry = None
    for country in input_file:
        if lastCountry is not None:
            sameCountry = lastCountry['CountryName'] == country['CountryName']
            #samedirection = lastservice['Direction'] == service['Direction']
            #samebusStop = lastservice['BusStopCode'] == service['BusStopCode']
            if sameCountry == False:
                model.addCountry(analyzer, country)
        else:
            model.addCountry(analyzer, country)
        lastCountry = country
    model.addCountry(analyzer, lastCountry)
    model.addLastCountry(analyzer, lastCountry)
    return analyzer

def loadLandingPoints(analyzer, landingPointsFile):
    """
    Carga los datos de los archivos CSV en el modelo.
    """
    file = cf.data_dir + landingPointsFile
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    lastLandingPoint = None
    for landingPoint in input_file:
        if lastLandingPoint is not None:
            sameLandingPoint = lastLandingPoint['landing_point_id'] == landingPoint['landing_point_id']
            if sameLandingPoint == False:
                model.addLandingPoint(analyzer, landingPoint)
                model.addLandingPointToMap(analyzer, landingPoint)
        else:
            model.addLandingPoint(analyzer, landingPoint)
            model.addLandingPointToMap(analyzer, landingPoint)
        lastLandingPoint = landingPoint
    model.addLandingPoint(analyzer, lastLandingPoint)
    model.addLandingPointToMap(analyzer, lastLandingPoint)
    return analyzer


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def totalLandingPoints(analyzer):
    """
    Total de Landing Points
    """
    return model.totalLandingPoints(analyzer)

def totalConnections(analyzer):
    """
    Total de Connections
    """
    return model.totalConnections(analyzer)

def totalCountries(analyzer):
    """
    Total de Countries
    """
    return model.totalCountries(analyzer)

def firstLandingPoint(analyzer):
    """
    Retorna el primer Landing_Point cargado
    """
    return model.firstLandingPoint(analyzer)

def lastLoadedCountry(analyzer):
    """
    Retorna el ultimo Country cargado
    """
    return model.lastLoadedCountry(analyzer)




# Req 1
def numeroTotalClusters(analyzer):
    return model.numeroTotalClusters(analyzer)

def estanEnMismoCluster(analyzer, nombreLandingA, nombreLandingB):
    return model.estanEnMismoCluster(analyzer, nombreLandingA, nombreLandingB)

# Req 2
def mostConnectedLandingPoints(analyzer):
    """
    Retorna una tupla con:
    Lista de landing points (nombre, país, identificador). [0]
    Total, de cables conectados a dichos landing points. [1]
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    datos = model.mostConnectedLandingPoints(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return datos, delta_time, delta_memory

# Req 3
def camino_mas_corto(analyzer, inicio, final):
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    datos = model.camino_mas_corto(analyzer, inicio, final)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)

    return datos, delta_time, delta_memory

# Req 4


# Req 5
def impacto_landingpoint(analyzer, nombre):
    return model.impacto_landingpoint(analyzer, nombre)
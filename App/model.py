﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from os import sep
from typing import List
import config as cf
from haversine import haversine
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

# Construccion de modelos

def newAnalyzer():
  
    try:
        analyzer = {
                    'connections': None,
                    'countries': None,
                    'landing_points': None,
                    'components': None,
                    'firstLandingPoint': None,
                    'lastLoadedCountry': None,
                    'paths': None
                    }

        analyzer['countries'] = mp.newMap(numelements=1279,
                                          maptype='PROBING',
                                          comparefunction=compareLandingIds)

        analyzer['landing_points'] = mp.newMap(numelements=1283,
                                               maptype='PROBING',
                                               comparefunction=compareLandingIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=3271,
                                              comparefunction=compareLandingIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


# Funciones para agregar informacion al catalogo

def addLandingPointConnection(analyzer, connection):
    """
    Adiciona las Landing Points al grafo como vertices y arcos entre las
    Landing Points adyacentes.
    """
    try:
        origin = int(connection['origin'])
        originLandingPoint = {'landing_point_id': int(origin)}
        destination = int(connection['destination'])
        destinationLandingPoint = {'landing_point_id': int(destination)}

        # Calcular Distancias
        latitudLandingOrigen = float(mp.get(analyzer['landing_points'], int(origin))['value']['first']['info']['latitude'])
        longitudLandingOrigen = float(mp.get(analyzer['landing_points'], int(origin))['value']['first']['info']['longitude'])
        latitudLandingDestino = float(mp.get(analyzer['landing_points'], int(destination))['value']['first']['info']['latitude'])
        longitudLandingDestino = float(mp.get(analyzer['landing_points'], int(destination))['value']['first']['info']['longitude'])

        latLongOrigen = (latitudLandingOrigen, longitudLandingOrigen)
        latLongDestino = (latitudLandingDestino, longitudLandingDestino)
        distance = distanciaEntreDosTuplasDeLatLong(latLongOrigen, latLongDestino)

        addLandingPoint(analyzer, originLandingPoint)
        addLandingPoint(analyzer, destinationLandingPoint)
        addConnection(analyzer, origin, destination, distance)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandingPointConnection')


def addLandingPoint(analyzer, landingPoint):
    """
    Adiciona una LandingPoint como un vertice del grafo
    """
    try:
        if analyzer['firstLandingPoint'] is None:
            analyzer['firstLandingPoint'] = str(landingPoint)
        if not gr.containsVertex(analyzer['connections'], int(landingPoint['landing_point_id'])):
            gr.insertVertex(analyzer['connections'], int(landingPoint['landing_point_id']))
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addLandingPoint')

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos landing points
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

def addCountry(analyzer, country):
    """
    Agrega a un Country
    """
    entry = mp.get(analyzer['countries'], country['CountryCode'])
    if entry is None:
        lst = lt.newList(cmpfunction=compare)
        lt.addLast(lst, country)
        mp.put(analyzer['countries'], country['CountryCode'], lst)
    else:
        lst = entry['value']
        info = country
        if not lt.isPresent(lst, info):
            lt.addLast(lst, info)
    return analyzer

def addLandingPointToMap(analyzer, landingPoint):
    """
    Agrega a un LandingPoint a un Map
    """
    entry = mp.get(analyzer['landing_points'], int(landingPoint['landing_point_id']))
    if entry is None:
        lst = lt.newList(cmpfunction=compare)
        lt.addLast(lst, landingPoint)
        mp.put(analyzer['landing_points'], int(landingPoint['landing_point_id']), lst)
    else:
        lst = entry['value']
        info = landingPoint
        if not lt.isPresent(lst, info):
            lt.addLast(lst, info)
    return analyzer

def addLastCountry(analyzer, country):
    analyzer['lastLoadedCountry'] = country
    return analyzer



# Funciones de consulta

def totalLandingPoints(analyzer):
    """
    Retorna el total de Landing Points (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])

def totalCountries(analyzer):
    """
    Retorna el total de Countries
    """
    return mp.size(analyzer['countries'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def firstLandingPoint(analyzer):
    """
    Retorna el primer Landing_Point cargado
    """
    return analyzer['firstLandingPoint']

def lastLoadedCountry(analyzer):
    """
    Retorna el ultimo Country cargado
    """
    return analyzer['lastLoadedCountry']

def mostConnectedLandingPoints(analyzer):
    maxDegreeLandingPoints = []
    vertices = []

    graphVertices = gr.vertices(analyzer['connections'])
    maxDegree = 0

    if graphVertices['first'] is not None:
        firstVertix = graphVertices['first']
        firstLandingId = int(firstVertix['info'])
        vertices.append(firstLandingId)
        next = firstVertix['next']
        while next is not None:
            currentVertixId = int(next['info'])
            vertices.append(currentVertixId)
            next = next['next']
    else:
        return ([], 0)

    for vertix in vertices:
        vertixDegree = gr.degree(analyzer['connections'], vertix)
        if vertixDegree == maxDegree:
            llaveValorMapaLanding = mp.get(analyzer['landing_points'], vertix)
            # Mapa retorna Llave/Valor. Sacamos Valor con Value,
            # Luego, el valor es un diccionario con la llave first
            # y dentro de esa llave encontramos el Landing con la llave info. 
            valorLanding = llaveValorMapaLanding['value']['first']['info']
            maxDegreeLandingPoints.append(valorLanding)
        elif vertixDegree > maxDegree:
            maxDegree = vertixDegree
            maxDegreeLandingPoints = []
            llaveValorMapaLanding = mp.get(analyzer['landing_points'], vertix)
            valorLanding = llaveValorMapaLanding['value']['first']['info']
            maxDegreeLandingPoints.append(valorLanding)
    return (maxDegreeLandingPoints, maxDegree)

# Se supone que el inicio o final son el nombre de un país.    
def camino_mas_corto(analyzer, inicio, final):
    landingInicio = None
    landingFinal = None

    listaLandingPoints = []
    landingValueSet = mp.valueSet(analyzer['landing_points']) 
    
    if landingValueSet['first'] is not None:
        firstItem = landingValueSet['first']
        firstLanding = firstItem['info']['first']['info']
        listaLandingPoints.append(firstLanding)
        next = firstItem['next']
        while next is not None:
            currentLanding = next['info']['first']['info']
            listaLandingPoints.append(currentLanding)
            next = next['next']
    else:
        return

    for landing in listaLandingPoints:
        landingCountryName = landingNameToCountryName(landing['name'])
        if inicio == landingCountryName:
            landingInicio = landing
        elif final == landingCountryName:
            landingFinal = landing
    
    if landingInicio == None or landingFinal == None:
        print("No se encontro el landing final o de inicio para esas entradas.")
        return analyzer
    

    #graphVertices = gr.vertices(analyzer["landing_points"])
    dijkstra = djk.Dijkstra(analyzer['connections'], int(landingInicio['landing_point_id']))
    path = djk.pathTo(dijkstra, int(landingFinal['landing_point_id']))

    respuesta = "• Path:"

    if path['first'] is not None:
        firstItem = path['first']
        firstIntermedio = firstItem['info']
        print(firstIntermedio)
        respuesta = respuesta + "\n    - From: " + str(firstIntermedio['vertexA']) + " to " + str(firstIntermedio['vertexB']) + ". Distance(km): " + str(firstIntermedio['weight'])
        next = firstItem['next']
        while next is not None:
            currentIntermedio = next['info']
            respuesta = respuesta + "\n    - From: " + str(currentIntermedio['vertexA']) + " to " + str(currentIntermedio['vertexB']) + ". Distance(km): " + str(currentIntermedio['weight'])
            next = next['next']
    else:
        return

    # Agregamos la distancia a la respuesta
    distancia = djk.distTo(dijkstra, int(landingFinal['landing_point_id']))
    respuesta = respuesta + "\n • Total Distance: " + str(distancia) + "km"

    return respuesta

# Usando libreria externa de Haversine: https://pypi.org/project/haversine/
def distanciaEntreDosTuplasDeLatLong(tupla1, tupla2):
    return haversine(tupla1, tupla2)

def landingNameToCountryName(name):
    splitName = str.split(name, ", ")
    splitSize = len(splitName)
    if splitSize == 1:
        return splitName
    else:
        return splitName[splitSize - 1]






# Funciones utilizadas para comparar elementos dentro de una lista

def compareLandingIds(landing, keyvaluelanding):
    """
    Compara dos landing point
    """
    landingcode = keyvaluelanding['key']
    if (landing == landingcode):
        return 0
    elif (landing > landingcode):
        return 1
    else:
        return -1

def compare(item1, item2):
    """
    Compara dos Countries
    """
    if (item1 == item2):
        return 0
    elif (item1 > item2):
        return 1
    else:
        return -1

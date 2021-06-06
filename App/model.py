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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
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
        #distance = float(landingPoint['Distance']) - float(lastservice['Distance'])
        #distance = abs(distance)
        distance = 0
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
    Adiciona un arco entre dos estaciones
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
        
def camino_mas_corto(analyzer, inicio, final):
    #graphVertices = gr.vertices(analyzer["landing_points"])
    search = djk.Dijkstra(analyzer['countries'], inicio)
    return search
    #assert djk.hasPathTo(search, final) is True
    #path = djk.pathTo(search, final)
    #print('')
    #while not stack.isEmpty(path):
    #    edge = stack.pop(path)
    #    print(edge)
    #    print(edge["VertexA"] + "-->" + edge["VertexB"] + " costo: " + str(edge["weight"]))
    









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

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

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo 

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos

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

def mostConnectedLandingPoints(analyzer):
    """
    Retorna una tupla con:
    Lista de landing points (nombre, país, identificador). [0]
    Total, de cables conectados a dichos landing points. [1]
    """
    return model.mostConnectedLandingPoints(analyzer)
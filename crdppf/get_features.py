# -*- coding: UTF-8 -*-
from pyramid.response import FileResponse
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPForbidden
from pyramid.view import view_config
from fpdf import FPDF
from datetime import datetime
import httplib
from owslib.wms import WebMapService
from simplejson import loads as sloads,dumps as sdumps   
import pkg_resources
from crdppf.models import *
import csv
from sqlalchemy import or_
from papyrus.geojsonencoder import dumps

@view_config(route_name='get_features',renderer='json')
def get_features(request):
    
    # for dev purposes: matching dictionnary model-table name
    table2model =   {'at39_itineraires_pedestres':PedestrianWays,
                    'at14_zones_communales': CommunalArea,
                    'at08_zones_cantonales': StateArea,
                    'clo_couloirs': Corridors,
                    'clo_cotes_altitude_surfaces': AltitudeRatings,
                    'en07_canepo_accidents': PollutedSitesAccidents,
                    'en07_canepo_decharges': PollutedSitesLandDumps,
                    'en07_canepo_decharges_points': PollutedSitesLandDumpsPts,
                    'en07_canepo_decharges_polygones': PollutedSitesLandDumpsPoly,
                    'en07_canepo_entreprises': PollutedSitesCompanies,
                    'en07_canepo_entreprises_points': PollutedSitesCompaniesPts,
                    'en07_canepo_entreprises_polygones': PollutedSitesCompaniesPoly}
    
    params = dict(request.params)
    parcelId = params['id']
    # get the parcel geometry
    queryParcel =DBSession.query(ImmeublesCanton).filter_by(idemai=parcelId).first()
    parcelGeom = queryParcel.geom
    # split the layer list string into proper python list
    csvReader = csv.reader([params['layerList']], skipinitialspace=True)

    # iterate over layer and make intersects queries
    itemList = []
    for item in csvReader:
        itemList.append(item)
    layerList = itemList[0]
    response = []
    test = 'empty'
    # retrieve models from table2model
    for layer in layerList:
        model = table2model[layer]
    
    # spatial analysis
    response = {}  
    featureList = []
    for layer in layerList:
        targetModel = table2model[layer]
        intersectResult = DBSession.query(targetModel).filter(or_(targetModel.geom.intersects(parcelGeom),targetModel.geom.within(parcelGeom))).all()
        if intersectResult:
            # create geojson output with custom attributes
            for feature in intersectResult:
                geometryType = DBSession.scalar(feature.geom.geometry_type())
                geomType = ''
                featureClass = ''
                featureMeasure = -9991
                if geometryType == 'ST_Polygon' or geometryType == 'ST_MultiPolygon':
                    intersectionArea = DBSession.scalar(feature.geom.intersection(parcelGeom).area())
                    featureMeasure = 100*intersectionArea/DBSession.scalar(parcelGeom.area())
                    geomType = 'Polygone'
                    if featureMeasure >= 99:
                        featureClass = 'within'
                    elif featureMeasure < 99 and featureMeasure > 1:
                        featureClass = 'intersects'
                    elif featureMeasure <= 1:
                        featureClass = 'adjacent'

                elif geometryType == 'ST_Line' or geometryType == 'ST_MultiLineString':
                    featureMeasure = -9999
                    geomType = 'Ligne'
                elif geometryType == 'ST_Point' or geometryType == 'ST_MultiPoint':
                    featureMeasure = -9999
                    geomType = 'Point'
                jsonFeature = sloads(dumps(feature))
                jsonFeature['properties']['layerName'] = layer
                jsonFeature['properties']['featureClass'] = featureClass
                featureList.append(jsonFeature)
                
                
                
     
    # append feature list to the response
    response.update({'type':'FeatureCollection', 'features': featureList})   
    return response
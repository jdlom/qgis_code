# coding: utf-8

import time
import platform

from qgis.utils import iface
from qgis.core import (QgsMapLayer, QgsVectorLayer,
                    QgsMapLayerRegistry)

from PyQt4.QtCore import QEventLoop

#decorator
def timeit(method):
    def timed(*args, **kwargs):
        try:
            ts = time.time()
            result = method(*args, **kwargs)
            te = time.time()
            print '%r %2.2f sec' % \
                  (method.__name__, te-ts)
            return result
        except Exception as e:
            msg = '{} failed'.format(method.__name__)
            raise TestException(msg, e.message)
    return timed

#Exception to manage error during tests
class TestException(Exception):
    def __init__(self, msg, details):
        Exception.__init__(self)
        self.msg = msg
        self.details = details
        self.inform_user(msg, details)
    def inform_user(self, msg, details):
        iface.messageBar().pushMessage(msg, details, level=QgsMessageBar.CRITICAL, duration=5)


@timeit
def loadLayer(layerUri, layer_name, provider):
    '''
    to get layerUri : open the layer
    get in properties and copy past the source:
    exemple :

    layerUri = ur"""dbname='D:/inondation.sqlite' table="commune" (geometry) sql="""
    layerUri = ur"""\\10.27.8.61\gb_cons\DONNEE_GENERIQUE\N_INTERCOMMUNALITE\L_EPCI_BDP_S_027.shp"""
    '''
    layer =  iface.addVectorLayer(layerUri, layer_name, provider)
    ev_loop = QEventLoop()
    canvas = iface.mapCanvas()
    canvas.renderComplete.connect(ev_loop.quit)
    ev_loop.exec_()
    return layer

@timeit
def openAttributeTable(layer):
    iface.showAttributeTable(layer)

@timeit
def saveLayer(layer, feature):
    pass

@timeit
def deleteFeatureAndSave(layer, fid):
    try:
        layer.startEditing()
        layer.deleteFeature(fid)
        layer.commitChanges()
    except:
        raise Error

def registerLayersSettings():
    ''' Return vector layer settings and remove all layers from the incoming project
    '''
    registry = QgsMapLayerRegistry.instance()
    layers_params = [
        (l.source(), l.name(), l.dataProvider().name())
        for l in registry.mapLayers().values()
        if l.type() == QgsMapLayer.VectorLayer]
    registry.removeAllMapLayers()
    return layers_params

def startTest():
    registry = QgsMapLayerRegistry.instance()
    layers_params = registerLayersSettings()
    for layer_params in layers_params:
        time.sleep(5)
        print(u'tests started - [{}]'.format(layer_params[1]))
        #run test
        layer = loadLayer(*layer_params)
        openAttributeTable(layer)
        #remove the layer
        registry.removeMapLayer(layer.id())

startTest()


#layerUri = ur"""/home/jd/TÃ©lÃ©chargements/GEOFLA_2-2_COMMUNE_SHP_LAMB93_FXX_2016-06-28/GEOFLA/1_DONNEES_LIVRAISON_2016-06-00236/GEOFLA_2-2_SHP_LAMB93_FR-ED161/COMMUNE/COMMUNE.shp"""
#layer = loadLayer(layerUri, "oscom", "ogr")
#openAttributeTable(layer)
##saveLayer(layer, 15)
#deleteFeatureAndSave(layer, 15)

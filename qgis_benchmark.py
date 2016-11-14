# coding: utf-8
import time
import platform
import os
import re
import random

from qgis.utils import iface
from qgis.core import (QgsMapLayer, QgsVectorLayer,
                       QgsMapLayerRegistry,
                       QgsVectorDataProvider)

from PyQt4.QtCore import QEventLoop
from functools import wraps

class Time:
    ''' Class to manage the format print of time
    '''
    def __init__(self, time, force_in_sec=False):
        self.time = time
        self.min, self.sec = divmod(time, 60)
        self.force_in_sec = force_in_sec
    def __repr__(self):
        if self.force_in_sec or not self.min:
            return u'{:.2f} sec(s)'.format(self.time)
        else:

            return u'{:.0f} min(s) {:.2f} sec(s)'.format(self.min, self.sec)


#decorator
def timeit(force_in_sec=False):
    def timeit_decorator(method):
        @wraps(method)
        def timed(*args, **kwargs):
            ts = time.time()
            result = method(*args, **kwargs)
            if result is not None:
                te = time.time()
                duration = Time(te-ts, force_in_sec)
                print('{} : {}'.format(method.__name__, duration))
            else:
                print('{} : failed'.format(method.__name__))
            return result
        return timed
    return timeit_decorator


#Exception to manage error during tests
# class TestException(Exception):
#     def __init__(self, msg, details):
#         Exception.__init__(self)
#         self.msg = msg
#         self.details = details
#         self.inform_user(msg, details)
#     def inform_user(self, msg, details):
#         iface.messageBar().pushMessage(msg, details, level=QgsMessageBar.CRITICAL, duration=5)

def qgisVersion():
    print('qgis version : {} '.format(unicode(QGis.QGIS_VERSION_INT)))

def machineInformation():
    #system, node, release, version, machine, processor = platform.uname()
    print 'os : {0} {2}\narchitecture : {4}\nprocessor : {5} '.format(*platform.uname())

def dateTimeTest():
    print ("Date tests : {}".format(time.strftime("%c")))



def layerSize(data_source, provider):
    '''
    Retrieve the layer size
    '''
    if provider == 'spatialite':
        m = re.search('\'(.*)\'', data_source)
        if m:
            filepath = m.group(1)
        else:
            return
    elif provider == 'ogr':
        filepath = data_source
    else:
        return

    _filepath, ext = os.path.splitext(filepath)
    if ext.lower() == '.shp':
        size = float(os.path.getsize(filepath))/(1024**2)
        print('layer size (shp): {:.2f}'.format(size))
        filepath = os.path.join(_filepath, '.dbf')
        if os.path.isfile(filepath):
            size = float(os.path.getsize(filepath))/(1024**2)
            print('layer size (dbf): {:.2f}'.format(size))
        else:
            return
    if ext.lower() == '.tab':
        size = float(os.path.getsize(filepath))/(1024**2)
        print('layer size (tab): {:.2f}'.format(size))
        filepath = os.path.join(_filepath, '.dbf')
        if os.path.isfile(filepath):
            size = float(os.path.getsize(filepath))/(1024**2)
            print('layer size (dbf): {:.2f}'.format(size))
        else:
            return    
    print('layer size : {:.2f}'.format(size))




@timeit(force_in_sec=True)
def loadLayer(data_source, layer_name, provider):
    '''
    To get data_source : open the layer,
    get in properties and copy past the source.
    Exemple :

    data_source = ur"""dbname='D:/inondation.sqlite' table="commune" (geometry) sql="""
    data_source = ur"""\\10.27.8.61\gb_cons\DONNEE_GENERIQUE\N_INTERCOMMUNALITE\L_EPCI_BDP_S_027.shp"""
    '''
    try:
        canvas = iface.mapCanvas()
        canvas.setRenderFlag(False)
        layer =  iface.addVectorLayer(data_source, layer_name, provider)
        ev_loop = QEventLoop()
        canvas.renderComplete.connect(ev_loop.quit)
        canvas.setRenderFlag(True)
        ev_loop.exec_()
        return layer
    except:
        return False

@timeit()
def openAttributeTable(layer):
    try:
        iface.showAttributeTable(layer)
        return True
    except:
        return False

@timeit()
def addFeatureAndSave(layer, features=None):
    try:
        if features is None:
            features = [layer.getFeatures().next()]
        layerProvider = layer.dataProvider()
        for feature in features:
            layer.startEditing()
            layerProvider.addFeatures([feature])
            layer.commitChanges()
        return True
    except:
        return False

@timeit()
def deleteFeatureAndSave(layer, feature_number=1):
    try:
        #features list to add with addFeatureLayerAndSave
        features = []
        layerCount = layer.featureCount()
        for i in range(feature_number):
            # layerCount = len([feat for feat in layer.getFeatures()])
            pos = int(random.random()*layerCount)
            for k, feat in enumerate(layer.getFeatures()):
                if k + 1 <= pos:
                    continue
            feature = QgsFeature(layer.getFeatures().next())
            fid = feature.id()
            for field in feature.fields():
                if field.name().lower() in ('id', 'pk', 'gid', 'pkuid', 'pk_uid', 'fid'):
                    try:
                        feature[field.name()] = None
                    except:
                        pass
            layer.startEditing()
            layer.deleteFeature(fid)
            layer.commitChanges()
            features.append(feature)
        return features
    except:
        return False

@timeit()
def updateGeomAndSave(layer, feature_number=1):
    try:
        return True
    except:
        return False

@timeit()
def updateAtributeAndSave(layer, feature_number=1):
    try:
        return True
    except:
        return False


def registerLayersSettings(printLayersParam=False):
    ''' Return vector layer settings and remove all layers from the incoming
        project
    '''
    registry = QgsMapLayerRegistry.instance()
    layers_params = [
        (l.source(), l.name(), l.dataProvider().name())
        for l in registry.mapLayers().values()
        if l.type() == QgsMapLayer.VectorLayer]
    registry.removeAllMapLayers()
    if printLayersParam:
        print layers_params
    return layers_params

def startTest(extraInformation=True):
    registry = QgsMapLayerRegistry.instance()
    layers_params = registerLayersSettings()
    #print layers_params
    print(u'Tests will start')
    if extraInformation:
        dateTimeTest()
        machineInformation()
        qgisVersion()
    for layer_params in layers_params:
        source, name, provider = layer_params
        print(u'\nTests starting - [{}]'.format(name))
        layerSize(source, provider)
        #time.sleep(2)
        #run test
        layer = loadLayer(*layer_params)
        openAttributeTable(layer)
        #tests with specific capabilites
        provider = layer.dataProvider()
        caps = provider.capabilities()
        if caps & QgsVectorDataProvider.DeleteFeatures:
            features = deleteFeatureAndSave(layer)
        if caps & QgsVectorDataProvider.AddFeatures:
            addFeatureAndSave(layer, features)

        #remove the layer
        registry.removeMapLayer(layer.id())

startTest()
# layer = loadLayer(u'\\\\10.27.8.61\\gb_cons\\FONCIER_SOL\\N_OCCUPATION_SOL\\OSCOM\\oscom2009_027_agr.shp', u'oscom2009_027_agr', u'ogr')
# openAttributeTable(layer)

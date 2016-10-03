# coding: utf-8
import time
import platform
import os
import re

from qgis.utils import iface
from qgis.core import (QgsMapLayer, QgsVectorLayer,
                    QgsMapLayerRegistry)

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
            te = time.time()
            duration = Time(te-ts, force_in_sec)
            print('{} : {}'.format(method.__name__, duration))
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
    info = platform.uname()
    os, version, arch, proc = info[0], info[2], info[4], info[5]
    print 'os : {} {}\narchitecture : {}\nprocessor : {} '.format(os, version, arch, proc)

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
    size = float(os.path.getsize(filepath))/(1024**2)
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
    canvas = iface.mapCanvas()
    canvas.setRenderFlag(False)
    layer =  iface.addVectorLayer(data_source, layer_name, provider)
    ev_loop = QEventLoop()
    canvas.renderComplete.connect(ev_loop.quit)
    canvas.setRenderFlag(True)
    ev_loop.exec_()
    return layer

@timeit()
def openAttributeTable(layer):
    iface.showAttributeTable(layer)

@timeit()
def saveLayer(layer, feature):
    pass

@timeit()
def deleteFeatureAndSave(layer, fid):
    # try:
    #     layer.startEditing()
    #     layer.deleteFeature(fid)
    #     layer.commitChanges()
    # except:
    #     pass
    pass

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
        #remove the layer
        registry.removeMapLayer(layer.id())

startTest()
# layer = loadLayer(u'\\\\10.27.8.61\\gb_cons\\FONCIER_SOL\\N_OCCUPATION_SOL\\OSCOM\\oscom2009_027_agr.shp', u'oscom2009_027_agr', u'ogr')
# openAttributeTable(layer)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qgis.core import (QgsDataSourceURI, 
    QgsVectorLayer, 
    QgsExpression, 
    QgsFeatureRequest,
    QgsMapLayerRegistry)

class VectorLayer(QgsVectorLayer):
    def __init__(self, *args, **kwargs):
        super(VectorLayer, self).__init__(*args, **kwargs)
        self._provider = self.dataProvider()
        self._name = None
        self._epsg = None
        self._filter = None
        self._encoding = None
        self._selection = None
        self._fieldList = None

    @classmethod
    def fromLayer(cls, layer, name=None, add_to_legend=False):
        ''' Transform classical layer into VectorLayer
        Usage :
        layer = VectorLayer.fromLayer(layer)
        layer = VectorLayer.fromLayer(layer, "my layer")
        layer = VectorLayer.fromLayer(layer, "my layer", True)
        layer = VectorLayer.fromLayer(layer, add_to_legend=True)
        layer = VectorLayer.fromLayer(layer,name,add_to_legend)
        '''
        if layer.__class__ is QgsVectorLayer:
            if not name:
                name = layer.name()
            new_layer = VectorLayer(layer.source(), name, 
                layer.dataProvider().name())
            new_layer.add(add_to_legend)
            return new_layer
        else:
            return None

    @classmethod
    def activeLayer(cls, name=None, add_to_legend=False):
        ''' Transform activeLayer into VectorLayer
        Usage :
        layer = VectorLayer.activeLayer()
        layer = VectorLayer.activeLayer("my layer")
        layer = VectorLayer.activeLayer(add_to_legend=True)

        '''
        layer = iface.activeLayer()
        return cls.fromLayer(layer, name, add_to_legend)

    ### name property ###
    @property
    def name(self):
        return super(VectorLayer, self).name()
    
    @name.setter
    def name(self, name):
        try:
            self.setName(name)
        except AttributeError:
            self.setLayerName(name)
    
    ### epsg property ###
    @property
    def epsg(self):
        try:
            return int(self._provider.crs().authid().split(":")[1])
        except IndexError:
            return None

    ### filter propery ###
    @property
    def filter(self):
        return self._provider.subsetString()

    @filter.setter
    def filter(self, sql):
        self._provider.setSubsetString(sql)
        self.reload()

    ### encoding property ###    
    @property
    def encoding(self):
        return self._provider.encoding()
    
    @encoding.setter
    def encoding(self, encoding):
        self._provider.setEncoding(encoding)

    ### provider property ###
    @property
    def provider(self):
        return self._provider.name()
    
    ### selection property ###
    @property
    def selection(self):
        return self.selectedFeatures()
    
    @selection.setter
    def selection(self, expr):
        result_it = self.where(expr)
        ids = [f.id() for f in result_it]
        self.setSelectedFeatures(ids)

    def where(self, exp):
        '''Request feature by QgsExpression
        Usage :
        for feat in layer.where("myfield" = 2):
            ...
        '''
        exp = QgsExpression(exp)
        if exp.hasParserError():
            raise Exception(exp.parserErrorString())
        if exp.hasEvalError():
            raise ValueError(exp.evalErrorString())
        return self.getFeatures(QgsFeatureRequest(exp))
    
    def add(self, add_to_legend=True):
        '''Add the instance to the legend'''
        QgsMapLayerRegistry.instance().addMapLayer(self, addToLegend=add_to_legend)
    
    def reload(self):
        '''Reload to force mapcanvas refresh'''
        self._provider.forceReload()
        self.triggerRepaint()
    

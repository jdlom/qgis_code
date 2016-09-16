#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qgis.core import (QgsDataSourceURI, 
    QgsVectorLayer, 
    QgsExpression, 
    QgsFeatureRequest,
    QgsMapLayerRegistry)

def add_layer(layer, load_in_legend=True):
    """
    Add a open layer to the QGIS session and layer registry.
    :param layer: The layer object to add the QGIS layer registry and session.
    :param load_in_legend: True if this layer should be added to the legend.
    :return: The added layer
    """
    if not hasattr(layer, "__iter__"):
        layer = [layer]
    QgsMapLayerRegistry.instance().addMapLayers(layer, load_in_legend)

class VectorLayer(QgsVectorLayer):
    def __init__(self, *args, **kwargs):
        super(VectorLayer, self).__init__(*args, **kwargs)
        self._provider = self.dataProvider()
        self._name = None
        self._epsg = None
        self._filter = None
        self._encoding = None
        self._selection = None

    @classmethod
    def fromLayer(cls, layer, name=None, add_to_legend=False):
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
        layer = iface.activeLayer()
        return cls.fromLayer(layer, name, add_to_legend)

    
    @property
    def name(self):
        return super(VectorLayer, self).name()
    
    @name.setter
    def name(self, name):
        try:
            self.setName(name)
        except AttributeError:
            self.setLayerName(name)
    
    @property
    def epsg(self):
        try:
            return int(self._provider.crs().authid().split(":")[1])
        except IndexError:
            return None

    @property
    def filter(self):
        return self._provider.subsetString()

    @filter.setter
    def filter(self, sql):
        self._provider.setSubsetString(sql)
        self.reload()

    @property
    def encoding(self):
        return self._provider.encoding()
    
    @encoding.setter
    def encoding(self, encoding):
        self._provider.setEncoding(encoding)

    @property
    def provider(self):
        return self._provider.name()
        
    def where(self, exp):
        exp = QgsExpression(exp)
        if exp.hasParserError():
            raise Exception(exp.parserErrorString())
        if exp.hasEvalError():
            raise ValueError(exp.evalErrorString())
        return self.getFeatures(QgsFeatureRequest(exp))

    @property
    def selection(self):
        return self.selectedFeatures()
    
    @selection.setter
    def selection(self, expr):
        result_it = self.where(expr)
        ids = [f.id() for f in result_it]
        self.setSelectedFeatures(ids)
    
    def add(self, add_to_legend=True):
        QgsMapLayerRegistry.instance().addMapLayer(self, addToLegend=add_to_legend)
    
    def reload(self):
        self._provider.forceReload()
        self.triggerRepaint()
    

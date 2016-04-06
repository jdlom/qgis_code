#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qgis.core import (QgsDataSourceURI, QgsVectorLayer)

class VectorLayer(QgsVectorLayer):
    def __init__(self, *args, **kwargs):
        super(QgsVectorLayer, self).__init__(*args, **kwargs)
        self._provider = self.dataProvider()
        
        self._epsg = None
        self._sql = None
        self._uri = QgsDataSourceURI()

    @property
    def epsg(self):
        return int(self._provider.crs().authid().split(":")[1])

    @property
    def sql(self):
        return self._provider.subsetString()

    @sql.setter
    def sql(self, sql):
        self._provider.setSubsetString(sql)

    @property
    def uri(self):





#qgis_code
conveniance class to get pyqgis more pythonic

##VectorLayer
A class to manipulate vector layer easier

###Why to use
With the VectorLayer class it's easier to :

	* access name
	* filter a layer
	* select entities


###How to use
```python
from VectorLayer import VectorLayer

#To transform an instance of QgsVectorLayer into VectorLayer
normal_layer = iface.activeLayer()
layer = VectorLayer.fromLayer(normal_layer, name="new name", add_to_legend=True)

#Print the name of the layer
print(layer.name)

#Chage the name of the layer
layer.name = "an other new name"

#Print the crs
print(layer.crs)

#Filter the layer
layer.filter="id<10"

#Select feature where "id>=5"
layer.selection="id>=5"

#Iterate over feature where "id<5"
for feature in layer.where("id<5"):
	print feat['id']
```



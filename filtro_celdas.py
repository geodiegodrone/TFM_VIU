import processing
from qgis.core import QgsRasterLayer, QgsProject

# Ruta al archivo raster del inventario
raster_path = "C:/Users/HOME/radar_antioquia_sentinel/raster/inventario.tif"

# Cargar el raster del inventario
raster_layer = QgsRasterLayer(raster_path, "Inventario")

# Verificar si el raster se cargó correctamente
if not raster_layer.isValid():
    print("Error: No se pudo cargar el raster de inventario.")
else:
    print("Raster cargado correctamente.")

# Crear una capa temporal con las celdas de movimientos en masa (valor 1)
processing.run("gdal:polygonize", {
    'INPUT': raster_layer,
    'BAND': 1,
    'FIELD': 'value',
    'EIGHT_CONNECTEDNESS': False,
    'EXTRA': '',
    'OUTPUT': 'memory:'
})

# Buffer de 10 celdas alrededor de las celdas con movimientos en masa
buffer_output = processing.run("native:buffer", {
    'INPUT': raster_layer,
    'DISTANCE': 10 * raster_layer.rasterUnitsPerPixelX(),  # Multiplicar por el tamaño de la celda
    'SEGMENTS': 5,
    'END_CAP_STYLE': 0,
    'JOIN_STYLE': 0,
    'MITER_LIMIT': 2,
    'DISSOLVE': False,
    'OUTPUT': 'memory:'
})

# Rasterizar el buffer creado anteriormente para que coincida con la capa de inventario original
rasterized_buffer = processing.run("gdal:rasterize", {
    'INPUT': buffer_output['OUTPUT'],
    'FIELD': 'value',
    'BURN': 0,
    'USE_Z': False,
    'UNITS': 1,
    'WIDTH': raster_layer.rasterUnitsPerPixelX(),
    'HEIGHT': raster_layer.rasterUnitsPerPixelY(),
    'EXTENT': raster_layer.extent(),
    'NODATA': -9999,
    'OPTIONS': '',
    'DATA_TYPE': 5,  # Float32
    'INIT': None,
    'INVERT': False,
    'EXTRA': '',
    'OUTPUT': "C:/Users/HOME/radar_antioquia_sentinel/raster/inventario_expandido.tif"
})

# Cargar el nuevo raster en QGIS
new_raster_layer = QgsRasterLayer(rasterized_buffer['OUTPUT'], "Inventario Expandido")
QgsProject.instance().addMapLayer(new_raster_layer)

print("Nuevo raster creado con celdas expandidas.")

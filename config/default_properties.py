import os
import sys

MAIN_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
CURRENT_WORKING_FILE_DIRECTORY = os.path.abspath(os.path.join(__file__))
CURRENT_WORKING_DIRECTORY = os.path.abspath(os.path.join(__file__, ".."))

if MAIN_PATH not in sys.path:
    sys.path.append(MAIN_PATH)

dir_path = os.path.dirname(os.path.realpath(__file__))
for root, dirs, files in os.walk(dir_path):
    sys.path.append(root)


def defualt_properties_info():
    """
    Default Properties are added here
    """
    pass


DEFAULT_EGO_PROPERTIES = {"model": "simonedriver",
                          "category": "Ego",
                          "name": "SimOne Driver",
                          "obuId": "0",
                          "obu_enabled": "false",
                          "color": "#63BA3C"}

DEFAULT_OBJ_PROPERTIES = {
            'car': {"asset_id": "1000064",
                     "builtIn": "true",
                     "resource_type": "builtIn",
                     "semantic_type": "vehicle",
                     "model": "ENCAP_GVT01",
                     "category": "vehicle",
                     "subCategory": "car",
                     "name": "ENCAP_GVT01",
                     "obuId": "1",
                     "obu_enabled": "true",
                     "scaleX": "1",
                     "scaleY": "1",
                     "scaleZ": "1",
                     "color": "#FF0000"},
            'twowheeler': {"asset_id": "1200003",
                     "builtIn": "true",
                     "resource_type": "builtIn",
                     "semantic_type": "none",
                     "model": "Bike03",
                     "category": "bicycle",
                     "subCategory": "bicycle",
                     "name": "Bike03",
                     "obuId": "1",
                     "obu_enabled": "false",
                     "scaleX": "1",
                     "scaleY": "1",
                     "scaleZ": "1"},
            'bicycle' : {"asset_id": "1200001",
                                 "builtIn": "true",
                                 "resource_type": "builtIn",
                                 "semantic_type": "none",
                                 "model": "Bike01",
                                 "category": "bicycle",
                                 "subCategory": "bicycle",
                                 "name": "Bike01",
                                 "obuId": "1",
                                 "obu_enabled": "false",
                                 "scaleX": "1",
                                 "scaleY": "1",
                                 "scaleZ": "1"},
            'human' : {"asset_id": "1100000",
                                 "builtIn": "true",
                                 "resource_type": "builtIn",
                                 "semantic_type": "none",
                                 "model": "Ped00",
                                 "category": "pedestrian",
                                 "subCategory": "pedestrian",
                                 "name": "Ped00",
                                 "obuId": "1",
                                 "obu_enabled": "false",
                                 "scaleX": "1",
                                 "scaleY": "1",
                                 "scaleZ": "1"}

            }


DEFAULT_SIZE_PROPERTIES = {
        'car': {'width': 1.73, 'length': 4.03, 'height': 1.43},
        'van': {'width': 2.0, 'length': 5.0, 'height': 2.0},
        'truck': {'width': 2.5, 'length': 7.0, 'height': 3.0},
        'trailer': {'width': 2.5, 'length': 12.0, 'height': 4.0},
        'semitrailer': {'width': 2.5, 'length': 14.0, 'height': 4.0},
        'bus': {'width': 2.5, 'length': 12.0, 'height': 3.5},
        'twowheeler': {'width': 0.82, 'length': 1.99, 'height': 1.77},
        'bicycle': {'width': 0.72, 'length': 1.87, 'height': 1.97},
        'train': {'width': 3.0, 'length': 20.0, 'height': 4.0},
        'tram': {'width': 2.5, 'length': 20.0, 'height': 3.5},
        'human': {'width': 0.18, 'length': 0.59, 'height': 1.82},
        'wheelchair': {'width': 0.7, 'length': 1.2, 'height': 1.5},
        'animal': {'width': 0.5, 'length': 1.5, 'height': 1.5}
    }
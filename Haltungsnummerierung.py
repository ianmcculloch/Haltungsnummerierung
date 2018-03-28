import processing
from PyQt4.QtGui import QColor
from operator import itemgetter
from operator import attrgetter
import time
import sys
import pdb
import logging
import qgis.gui 

VonSchacht = 0
BisSchacht = 0
bis_schacht = 1
sTime = time.time()
haltungen = []
selected_FeatureCount = 0
VonBisSchacht = []
logging.basicConfig(level=logging.DEBUG)

layer_haltungen = QgsMapLayerRegistry.instance().mapLayersByName("Haltungen 20180308")[0]
layer_haltungen.isValid()
layer_schacht = QgsMapLayerRegistry.instance().mapLayersByName("Normschacht 20180308")[0]
# layer_selectedHaltungen = QgsMapLayerRegistry.instance().mapLayersByName("Haltungen 20180308 copy")[0]
features_selectedHaltungen = processing.features(layer_haltungen)
# print("Haltungen-For:")
for feature in features_selectedHaltungen:
    try:
        # print("Start des Haltungs-For-Loop")
        layer_haltungen.setSelectedFeatures([])
        iface.mapCanvas().setSelectionColor( QColor("yellow"))
        fid = int(feature.id())
        layer_haltungen.setSelectedFeatures([fid])

        # print "Feature ID %d: " % feature.id()
        processing.runalg("preconfigured:normschacht")
        features_schacht = processing.features(layer_schacht)
        # for f in features_schacht:
        #     if f['Funktion'] == 6:
        #         logging.DEBUG("Break")
        #         break
        ordered_nodes = sorted(features_schacht, key=itemgetter('Num_Holi'))
        # for f in ordered_nodes:
        #     print("Schacht: " + str(f['Num_Holi']))
        ordered_nodes.reverse()
        # print("Sorted: ")
        # for f in ordered_nodes:
        #     print("Schacht: " + str(f['Num_Holi']))
        layer_haltungen.startEditing()
        # print("Type: " + str(type(ordered_nodes[1])))
        # print(type(ordered_nodes[1]))

        # with edit(layer_haltungen):
        #     for ord in ordered_nodes:
        #         print ord['Num_Holi']
        #         # VonBisSchacht[ord.id()] = ord['Num_Holi']
        #         # print type(ord)
        # print ("Attribut: " +str(feature.attribute('VonSchacht')))
        # layer_haltungen.updateFeature(fet)
        # feature['VonSchacht'] = 
        if (ordered_nodes[0].attribute('Num_Holi') == None):
            pass
            # print("Check(VonSchacht) is Null")
        elif (ordered_nodes[1].attribute('Num_Holi') == None):
            pass
            # print("Check(BisSchacht) is Null")
        elif (ordered_nodes[0].attribute('Kilo_Holi') == None):
            pass
            # print("Check(Kilo) is Null")
        else:
            VonSchacht = ordered_nodes[0].attribute('Num_Holi')
            BisSchacht = ordered_nodes[1].attribute('Num_Holi')
            Kilo = ordered_nodes[0].attribute('Kilo_Holi')
            # print("VonSchacht: " + str(VonSchacht))
            # print("BisSchacht: " + str(BisSchacht))
            # print("Kilo: " + str(Kilo))
            vonSchacht_fieldIndex = feature.fields().indexFromName('VonSchacht')
            bisSchacht_fieldIndex = feature.fields().indexFromName('BisSchacht')
            bezeich_fieldIndex = feature.fields().indexFromName('Bezeichn_1')
            kilo_fieldIndex = feature.fields().indexFromName('Kilo')
            # print(type(vonSchacht_fieldIndex))
            # print(bisSchacht_fieldIndex)
            vonSchacht_attr = {vonSchacht_fieldIndex: VonSchacht}
            bisSchacht_attr = {bisSchacht_fieldIndex: BisSchacht}
            Schacht_attrs = {vonSchacht_fieldIndex: VonSchacht, bisSchacht_fieldIndex: BisSchacht}
            # print(vonSchacht_attr)
            # print(bisSchacht_attr)
            # print(fid)
            abschnitt = "N01_0"
            # if Kilo = None or VonSchacht = None or BisSchacht = None: print()
            bezeichnung = abschnitt + str(Kilo) + "_H" + str(VonSchacht) + "-" + str(BisSchacht)
            layer_haltungen.changeAttributeValue(fid, vonSchacht_fieldIndex, VonSchacht)
            layer_haltungen.changeAttributeValue(fid, bisSchacht_fieldIndex, BisSchacht)
            layer_haltungen.changeAttributeValue(fid, bezeich_fieldIndex, bezeichnung)
            layer_haltungen.changeAttributeValue(fid, kilo_fieldIndex, Kilo)
        layer_haltungen.changeAttributeValue(fid, feature.fields().indexFromName('Counter'), 1)
        layer_haltungen.commitChanges()
        layer_schacht.setSelectedFeatures([])
    except IndexError, e:
        layer_haltungen.startEditing()
        layer_haltungen.changeAttributeValue(fid, feature.fields().indexFromName('Counter'), 1)
        layer_haltungen.commitChanges()
        logging.warning("IndexError")
    else:
        pass
    finally:
        pass
# print("Ende des Haltungs-For-Loop")

layer_haltungen.setSelectedFeatures([])
print("Skript beendet")
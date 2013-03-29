#!/usr/bin/python
# David Newell
# kml_styles.py
# Generate KML styles for SUPERSLR features in Google Earth

BASE_PATH = "/home/jack_sparrow/sebastian.sp/sebastian/"

# Import Useful Modules
import sys
sys.path.append(BASE_PATH)
import GeoUtils
BASE_URL = GeoUtils.constants.BASE_URL

# Format KML styles
def KMLstyles():
    # Start KML output
    kml_output = '<name>SUPERSLR KML Styles</name>\n'
    kml_output += '<open>1</open>\n\n'

    # Don't show child elements in feature listing
    kml_output += '<Style id="check-hide-children">\n<ListStyle>\n'
    kml_output += '<listItemType>checkHideChildren</listItemType>\n'
    kml_output += '</ListStyle>\n</Style>\n\n'

    # Elevation point style
    kml_output += '<Style id="depthPoint">\n<IconStyle>\n'
    kml_output += '<scale>0.25</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/shapes/donut.png</href></Icon>\n'
    kml_output += '</IconStyle></Style>\n\n'

    # Zoom in point style
    kml_output += '<Style id="zoom_placemark">\n<IconStyle>\n'
    kml_output += '<scale>1.2</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/shapes/arrow.png</href></Icon>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'

    # Error placemark
    kml_output += '<Style id="error_placemark">\n<IconStyle>\n'
    kml_output += '<scale>1</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/shapes/forbidden.png</href></Icon>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'

    # 4D timeline port not designed (white placemark)
    kml_output += '<Style id="portNotDesigned">\n<IconStyle>\n'
    kml_output += '<scale>2</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/paddle/wht-blank.png</href></Icon>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'

    # 4D timeline port in design (pink placemark)
    kml_output += '<Style id="portDesign">\n<IconStyle>\n'
    kml_output += '<scale>2</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/paddle/pink-diamond.png</href></Icon>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'

    # 4D timeline port in construction (yellow placemark)
    kml_output += '<Style id="portConstruction">\n<IconStyle>\n'
    kml_output += '<scale>2</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png</href></Icon>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'

    # 4D timeline port complete/protected (green placemark)
    kml_output += '<Style id="portComplete">\n<IconStyle>\n'
    kml_output += '<scale>2</scale>\n'
    kml_output += '<Icon><href>http://maps.google.com/mapfiles/kml/paddle/grn-blank.png</href></Icon>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'

    # Port Characteristics placemarks (complete - green sailboat icon)
    kml_output += '<StyleMap id="portCharacteristicsComplete">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#portCharCompleteN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#portCharCompleteH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="portCharCompleteN">\n<IconStyle>\n'
    kml_output += '<scale>1.2</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/sailboat-tourism.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="portCharCompleteH">\n<IconStyle>\n'
    kml_output += '<scale>1.4</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/sailboat-tourism.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>fff3e9d7</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Port Characteristics placemarks (partially complete - red sailboat icon)
    kml_output += '<StyleMap id="portCharacteristicsPartComplete">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#portCharPartCompleteN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#portCharPartCompleteH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="portCharPartCompleteN">\n<IconStyle>\n'
    kml_output += '<scale>1.2</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/sailboat-sport.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="portCharPartCompleteH">\n<IconStyle>\n'
    kml_output += '<scale>1.4</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/sailboat-sport.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>fff3e9d7</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Port Characteristics placemarks (incomplete - black sailboat icon)
    kml_output += '<StyleMap id="portCharacteristicsIncomplete">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#portCharIncompleteN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#portCharIncompleteH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="portCharIncompleteN">\n<IconStyle>\n'
    kml_output += '<scale>1.2</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/sailboat.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="portCharIncompleteH">\n<IconStyle>\n'
    kml_output += '<scale>1.4</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/sailboat.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>fff3e9d7</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Region Characteristics placemarks (info icon)
    kml_output += '<StyleMap id="RegionPlacemark">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#RegionPlacemarkN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#RegionPlacemarkH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="RegionPlacemarkN">\n<IconStyle>\n'
    kml_output += '<scale>2.0</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/info.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="RegionPlacemarkH">\n<IconStyle>\n'
    kml_output += '<scale>2.2</scale>\n'
    kml_output += '<Icon><href>http://gis.davidnewell.info/ico/icons/info.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction" />\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>fff3e9d7</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Port Infrastructure polygons (transparent red)
    kml_output += '<StyleMap id="portInfrastructure">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#portInfrastructureN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#portInfrastructureH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="portInfrastructureN">\n<PolyStyle>\n'
    kml_output += '<color>bf0000ff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="portInfrastructureH">\n<BalloonStyle>\n'
    kml_output += '<bgColor>ff7575ff</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bf0000ff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Basin polygons (transparent light blue)
    kml_output += '<StyleMap id="basinPolygon">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#basinPolygonN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#basinPolygonH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="basinPolygonN">\n<PolyStyle>\n'
    kml_output += '<color>bfff5555</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="basinPolygonH">\n<BalloonStyle>\n'
    kml_output += '<bgColor>fffea2a2</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bfff5555</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Model Avoid polygons (transparent orange)
    kml_output += '<StyleMap id="avoidPolygon">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#avoidPolygonN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#avoidPolygonH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="avoidPolygonN">\n<PolyStyle>\n'
    kml_output += '<color>bf0b78ff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="avoidPolygonH">\n<BalloonStyle>\n'
    kml_output += '<bgColor>ff73b2ff</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bf0b78ff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Berm Avoid polygons (transparent orange)
    kml_output += '<StyleMap id="bermAvoidPolygon">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#bermAvoidPolygonN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#bermAvoidPolygonH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="bermAvoidPolygonN">\n<PolyStyle>\n'
    kml_output += '<color>bfff5555</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="bermAvoidPolygonH">\n<BalloonStyle>\n'
    kml_output += '<bgColor>fffea2a2</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bfff5555</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Model StartEnd polygons (transparent lime green)
    kml_output += '<StyleMap id="startEndPolygon">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#startEndPolygonN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#startEndPolygonH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="startEndPolygonN">\n<PolyStyle>\n'
    kml_output += '<color>bf25f87e</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="startEndPolygonH">\n<BalloonStyle>\n'
    kml_output += '<bgColor>ff6af6a5</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bf25f87e</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Connected User View polygons (transparent pink)
    kml_output += '<StyleMap id="connUserViewPolygon">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#connUserViewPolygonN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#connUserViewPolygonH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="connUserViewPolygonN">\n<PolyStyle>\n'
    kml_output += '<color>55c1bdff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="connUserViewPolygonH">\n<BalloonStyle>\n'
    kml_output += '<bgColor>bfa48cfe</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bfc1bdff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Model Path linestrings (yellow lines with transparent light yellow fill)
    kml_output += '<StyleMap id="modelPath">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#modelPathN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#modelPathH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="modelPathN">\n<IconStyle>\n'
    kml_output += '<scale>1.1</scale>\n'
    kml_output += '</IconStyle>\n<LineStyle>\n'
    kml_output += '<color>bf00ffff</color>\n'
    kml_output += '</LineStyle>\n<PolyStyle>\n'
    kml_output += '<color>bf7fffff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="modelPathH">\n<IconStyle>\n'
    kml_output += '<scale>1.3</scale>\n'
    kml_output += '</IconStyle>\n<LineStyle>\n'
    kml_output += '<color>bf00ffff</color>\n'
    kml_output += '</LineStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ffaaffff</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>bf7fffff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Berm Path linestrings (yellow lines with transparent light yellow fill)
    kml_output += '<StyleMap id="bermPath">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#bermPathN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#bermPathH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="bermPathN">\n<IconStyle>\n'
    kml_output += '<scale>1.1</scale>\n'
    kml_output += '</IconStyle>\n<LineStyle>\n'
    kml_output += '<color>ff73b2ff</color>\n'
    kml_output += '</LineStyle>\n<PolyStyle>\n'
    kml_output += '<color>ff73b2ff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'
    kml_output += '<Style id="bermPathH">\n<IconStyle>\n'
    kml_output += '<scale>1.3</scale>\n'
    kml_output += '</IconStyle>\n<LineStyle>\n'
    kml_output += '<color>ff73b2ff</color>\n'
    kml_output += '</LineStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ff73b2ff</bgColor>\n'
    kml_output += '<textColor>ff73b2ff</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n<PolyStyle>\n'
    kml_output += '<color>ff73b2ff</color>\n'
    kml_output += '</PolyStyle>\n</Style>\n\n'

    # Information placemarks (no icon)
    kml_output += '<StyleMap id="infoNoIcon">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#infoNoIconN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#infoNoIconH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="infoNoIconN">\n<IconStyle>\n'
    kml_output += '<scale>0</scale>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="infoNoIconH">\n<IconStyle>\n'
    kml_output += '<scale>0</scale>\n'
    kml_output += '<hotSpot x="0.5" y="0.5" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ffa0cadc</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Note Caution (caution icon)
    kml_output += '<StyleMap id="noteCaution">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#noteCautionN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#noteCautionH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="noteCautionN">\n<IconStyle>\n'
    kml_output += '<Icon><href>http://sebastian.underwatershipping.com/uniform/img/Alert.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '<scale>0.4</scale>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="noteCautionH">\n<IconStyle>\n'
    kml_output += '<Icon><href>http://sebastian.underwatershipping.com/uniform/img/Alert.png</href></Icon>\n'
    kml_output += '<scale>0.5</scale>\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ff7ec9fe</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Note Sticky (note icon)
    kml_output += '<StyleMap id="noteSticky">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#noteStickyN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#noteStickyH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="noteStickyN">\n<IconStyle>\n'
    kml_output += '<Icon><href>http://sebastian.underwatershipping.com/uniform/img/Notepad.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '<scale>0.4</scale>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="noteStickyH">\n<IconStyle>\n'
    kml_output += '<Icon><href>http://sebastian.underwatershipping.com/uniform/img/Notepad.png</href></Icon>\n'
    kml_output += '<scale>0.5</scale>\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ff87ecf0</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Note Info (info icon)
    kml_output += '<StyleMap id="noteInfo">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#noteInfoN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#noteInfoH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="noteInfoN">\n<IconStyle>\n'
    kml_output += '<Icon><href>http://sebastian.underwatershipping.com/uniform/img/Info.png</href></Icon>\n'
    kml_output += '<hotSpot x="0.5" y="0" xunits="fraction" yunits="fraction"/>\n'
    kml_output += '<scale>0.4</scale>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="noteInfoH">\n<IconStyle>\n'
    kml_output += '<Icon><href>http://sebastian.underwatershipping.com/uniform/img/Info.png</href></Icon>\n'
    kml_output += '<scale>0.5</scale>\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ffe4c49e</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Note Hidden (hidden icon)
    kml_output += '<StyleMap id="noteHidden">\n'
    kml_output += '<Pair>\n<key>normal</key>\n<styleUrl>#noteHiddenN</styleUrl>\n</Pair>\n'
    kml_output += '<Pair>\n<key>highlight</key>\n<styleUrl>#noteHiddenH</styleUrl>\n</Pair>\n'
    kml_output += '</StyleMap>\n\n'
    kml_output += '<Style id="noteHiddenN">\n<IconStyle>\n'
    kml_output += '<scale>0</scale>\n'
    kml_output += '</IconStyle>\n</Style>\n\n'
    kml_output += '<Style id="noteHiddenH">\n<IconStyle>\n'
    kml_output += '<scale>0</scale>\n'
    kml_output += '</IconStyle>\n<BalloonStyle>\n'
    kml_output += '<bgColor>ffd2ebec</bgColor>\n'
    kml_output += '<textColor>ff300502</textColor>\n'
    kml_output += '<displayMode>default</displayMode>\n'
    kml_output += '</BalloonStyle>\n</Style>\n\n'

    # Return formatted KML styles
    return kml_output



# If file called directly, output KML
if __name__ == "__main__":
    # Print content-type header
    print GeoUtils.Interface.ContentType("kml")

    # Alternate MIME-type for debugging
    #print "Content-type: text/html"

    # Print blank line
    print

    # KML Header
    kml_header = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_header += '<kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom">\n'
    kml_header += '<Document id="superslr_styles">\n'

    # KML Footer
    kml_footer = '</Document>\n'
    kml_footer += '</kml>\n'

    print kml_header
    print KMLstyles()
    print kml_footer

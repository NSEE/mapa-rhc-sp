from lxml import etree
import os

def create_multi_placemark(drs_name, geometries):
    placemark = etree.Element("Placemark")
    name = etree.SubElement(placemark, "name")
    name.text = drs_name
    multi_geometry = etree.SubElement(placemark, "MultiGeometry")
    for geometry in geometries:
        multi_geometry.append(geometry)
    return placemark

def group_county_by_drs(county_with_name_file: str, drs_list: dict):
    print("GROUP COUNTY BY DRS: Grouping counties by DRS")
    
    if drs_list is None:
        print("GROUP COUNTY BY DRS: DRS list is empty")
        exit()
    
    file_dir = './tmp/' + county_with_name_file
    try:
        tree = etree.parse(file_dir)
    except Exception as e:
        print("GROUP COUNTY BY DRS [ERROR]: ", e)
        exit()
    
    root = tree.getroot()
    namespace = {"kml": "http://www.opengis.net/kml/2.2"}
    
    new_kml = etree.Element("kml", nsmap=namespace)
    new_document = etree.SubElement(new_kml, "Document")
    
    
    for drs_name, cities in drs_list.items():
        geometries = []
        for placemark in root.xpath(".//kml:Placemark", namespaces=namespace):
            city_name = placemark.find("kml:name", namespaces=namespace).text.upper()
            if city_name in cities:
                geometry = placemark.find("kml:Polygon", namespaces=namespace)
                if geometry is not None:
                    geometries.append(geometry)
        if geometries:
            multi_placemark = create_multi_placemark(drs_name, geometries)
            new_document.append(multi_placemark)
    
    new_tree = etree.ElementTree(new_kml)
    
    if not os.path.exists("./tmp"):
        print("GROUP COUNTY BY DRS: Creating tmp directory")
        os.makedirs("./tmp")
    
    output_file_name = "municipios_sp_grouped_by_drs.kml"
    
    print("GROUP COUNTY BY DRS: Writing to file")
    new_tree.write(
        "./tmp/" + output_file_name,
        encoding="UTF-8",
        xml_declaration=True,
        pretty_print=True
        )
    
    return output_file_name

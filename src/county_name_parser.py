import os
from lxml import etree

async def parse_county_name(county_file_name: str):
    print('COUNTY NAME PARSER: Parsing county names')
    
    file_dir = './content/' + county_file_name
    
    try:
        tree = etree.parse(file_dir)
    except Exception as e:
        print('COUNTY NAME PARSER [ERROR]:', e)
        exit()
    
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

    for placemark in root.findall('.//kml:Placemark', namespaces=namespace):
        nm_mun = placemark.find('.//kml:SimpleData[@name="NM_MUN"]', namespaces=namespace)

        if nm_mun is not None:
            name_tag = etree.Element('name')
            nm_mun.text = str(nm_mun.text).upper()
            name_tag.text = nm_mun.text
            placemark.insert(0, name_tag)

    if not os.path.exists('./tmp'):
        print('COUNTY NAME PARSER: Creating tmp directory')
        os.makedirs('./tmp')

    output_file_name = 'municipios_sp_with_name.kml'
    
    print('COUNTY NAME PARSER: Writing to file')
    
    tree.write(
        './tmp/' + output_file_name, 
        encoding="UTF-8", 
        xml_declaration=True, 
        pretty_print=True
        )
    
    return output_file_name


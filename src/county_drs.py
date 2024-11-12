from lxml import etree
import os

def parse_county_drs(county_with_name_file: str, drs_list: dict):
    print('COUNTY DRS PARSER: Parsing county DRS codes')
     
    if drs_list is None:
        print('COUNTY DRS PARSER: DRS list is empty')
        exit()
    
    file_dir = './tmp/' + county_with_name_file
    
    try:
        tree = etree.parse(file_dir)
    except Exception as e:
        print('COUNTY DRS PARSER [ERROR]: ', e)
        exit()
    
    root = tree.getroot()
    namespace = {'kml': 'http://www.opengis.net/kml/2.2'}
    
    for drs_name, cities in drs_list.items():
        for city in cities:
            city = str(city).upper()
            
            placemark = root.find(
                f'.//kml:Placemark[kml:name="{city}"]',
                namespaces=namespace
                )
            
            if placemark is not None:
                drs_tag = etree.Element('drs')
                drs_tag.text = drs_name
                placemark.insert(1, drs_tag)
                
    if not os.path.exists('./tmp'):
        print('COUNTY DRS PARSER: Creating tmp directory')
        os.makedirs('./tmp')
        
    output_file_name = 'municipios_sp_with_name_and_drs.kml'
    
    print('COUNTY DRS PARSER: Writing to file')
    tree.write(
        './tmp/' + output_file_name,
        encoding='UTF-8',
        xml_declaration=True,
        pretty_print=True
        )
        
    return output_file_name
import src.county_name_parser as county_name_parser
import src.county_drs as county_drs 
import src.group_county_by_drs as group_county_by_drs
import src.data as data
import asyncio

original_file = 'municipios_sp_ibge.kml'
drs_list = data.get_drs_list()

county_with_name_file = asyncio.run(county_name_parser.parse_county_name(original_file))

county_drs.parse_county_drs(county_with_name_file, drs_list)
group_county_by_drs.group_county_by_drs(county_with_name_file, drs_list)

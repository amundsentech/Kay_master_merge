
from ipaddress import collapse_addresses


sample_id_formats= ["(\d{2}\-\d{3})","(\d{2}\-\d{3}[a-zA-Z]{1})"]
hole_id_formats=['([a-zA-Z]{2}\-{1}\d{2}\-{1}\d{2})','([a-zA-Z]{2}\-{1}\d{2}\-{1}\d{2}[a-zA-Z]{1})']
collars='/_Drilling/collar master.csv'
holes='/_Lab/XRF/_XRF Hole Masters/'
raw='/_Lab/XRF/_Daily Master/_XLSX/'

depth_mapping={
    'DepthFrom':'start_depth',
    'START':'start_depth',
    'END':'end_depth',
    'DepthTo':'end_depth'
    }

file_mapping={
    'FileName':'file',
    'filename':'file',
    'foldername':'folder',
    'ProjectPath':'folder'
}
geo_mapping={
    'User':'geo',
    'Sample ID':'sample_id_xrf',
    'Depth':'depth_ft'
}

mappings=[file_mapping,geo_mapping]
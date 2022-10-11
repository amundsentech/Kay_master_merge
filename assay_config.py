
sample_id_formats= "([a-zA-Z]{1}\d{6})","([a-zA-Z]{2}\d{10})"
hole_id_formats=['([a-zA-Z]{2}\-{1}\d{2}\-{1}\d{2})','([a-zA-Z]{2}\-{1}\d{2}\-{1}\d{2}[a-zA-Z]{1})']

soil_ids="([a-zA-Z]{2}\d{10})"
drill_ids="([a-zA-Z]{2}\d{10})"

samples='/_Master Databases/drill assay samples master.csv'

soils='/_Lab/Terraspec/Terraspec Master.xlsx'

vnir_mapping={
    'Chlorite_vnir':'Chl_vnir',
    'Amphibole_vnir':'Amph_vnir',
    'Tourmaline_vnir':'Tourm_vnir',
}

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
mappings=[depth_mapping,file_mapping]
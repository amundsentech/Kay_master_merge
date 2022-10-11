
sample_id_formats= "([a-zA-Z]{1}\d{6})","([a-zA-Z]{2}\d{10})"

hand_samples='/_Lab/Terraspec/Terraspec Master.xlsx'
hand_export='/_Master Databases/spectral master onsite.csv'
sample_path='/_Drilling/_Logs'

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
mappings=[depth_mapping,file_mapping,vnir_mapping]
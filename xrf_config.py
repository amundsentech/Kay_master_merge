
sample_id_formats= ["(\d{2}\-\d{3})","(\d{2}\-\d{3}[a-zA-Z]{1})","(\d{2}\-\d{2})"]

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
mappings=[file_mapping]
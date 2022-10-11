
sample_id_formats= ["([a-zA-Z]{1}\d{6})","([a-zA-Z]{2}\d{10})"]
hole_id_formats= '([a-zA-Z]{2}\-{1}\d{2}\-{1}\d{2})','([a-zA-Z]{2}\-{1}\d{2}\-{1}\d{2}[a-zA-Z]{1})'


vnir_mapping={
    'Chlorite_vnir':'Chl_vnir',
    'Amphibole_vnir':'Amph_vnir',
    'Tourmaline_vnir':'Tourm_vnir',
}

depth_mapping={
    'DepthFrom':'start_depth',
    'START':'start_depth',
    'END':'end_depth',
    'DepthTo':'end_depth',
    'To_Ft':'To_ft'
    }

file_mapping={
    'FileName':'file',
    'filename':'file',
    'foldername':'folder',
    'ProjectPath':'folder'
}

hole_mapping={
    'Work_Order':'hole_id',
    'Hole_ID':'hole_id',
}



mappings=[depth_mapping,file_mapping]
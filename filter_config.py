

output_path='Google Drive/Shared drives/AMC Projects/_AZ_Kay/_Master Databases/ML_data/'
assay_file='Google Drive/Shared drives/AMC Projects/_AZ_Kay/_Master Databases/drill assays master.csv'
spec_file='Google Drive/Shared drives/AMC Projects/_AZ_Kay/_Master Databases/spectral master.csv'


assay_fname=f'drill assays_curate.csv'
spec_fname=f'spectral_curate.csv'


final_fname=f'spectral_drill assays_curate_merge.csv'



sample_id_formats= "([a-zA-Z]{1}\d{6})","([a-zA-Z]{2}\d{10})"

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


output_path='/home/scott/amcdrive/_AZ_Kay/_Master Databases/'
assay_file='https://drive.google.com/file/d/1YSK2cDKDI5hNZVqBCCHfxbMzll6k49uf/view?usp=sharing'
spec_file='https://drive.google.com/file/d/1fhu8rJSIa8mkWzznzRN3rCfxUaQu-o5e/view?usp=sharing'


assay_fname=f'drill assays master.csv'
spec_fname=f'spectral master.csv'


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
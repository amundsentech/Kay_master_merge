

output_path='~/amcdrive/_AZ_Kay/_Master Databases/'
assay_file='~/amcdrive/_AZ_Kay/_Master Databases/drill assays master'
spec_file='~/amcdrive/_AZ_Kay/_Master Databases/spectral master.csv'
alter_file='~/amcdrive/_AZ_Kay/_Master Databases/alteration master.csv'
mineral_file='~/amcdrive/_AZ_Kay/_Master Databases/mineralization master.csv'
sample_file='~/amcdrive/_AZ_Kay/_Master Databases/samples master.csv'
structure_file='~/amcdrive/_AZ_Kay/_Master Databases/stricture master.csv'
lith_file='~/amcdrive/_AZ_Kay/_Master Databases/lithology master.csv'

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
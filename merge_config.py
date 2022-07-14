'''
Do not include sample_id in main_columns! that is the starting point for the merge
'''
import file_config as fconfig
merge_samples=[
    fconfig.assay_file,
    fconfig.spec_file,
    fconfig.hyp_file,
    fconfig.sample_file,
]
merge_holes=[
    fconfig.structure_file,
    fconfig.mineral_file,
    fconfig.lith_file,
    fconfig.alter_file,
]
main_columns=['geo','hole_id','from_ft','to_ft']
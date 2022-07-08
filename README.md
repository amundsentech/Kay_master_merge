# Kay_curation_scripts
 The scripst and tools to clean and merge Kay sample data
 All data must be in csvs at the moment.
 Current tools:
- pull_sample_ids()
     - Searchs for columns named something similiar to sample
     - Takes the values in those columns and matches them to a regex pattern(located in the filter_config) 
     - merges the data based on the sample_id
     - drops columns with no data
- column_cleanup()
     - Uses mappings located in the filter config to merge columns with the same name but different column headers
- carrot_cleanup() 
     - sets values with '<' to - (logic here is that a less than value means the value is negligable so ' - ')\
     - sets values with > to the proper value or the converted percentage from the converted 'XX_2' column
## assay_curate.py is the main file to clean the assay data. Currently accepts two arguements.
 - assay_curate.py -r
    1. The path to the master assay_data -i
    2. the output path -o
    3. will use the default Google-drive location in the config if input not specified
    4. if output not specified will edit inplace
    
 ## spectral_curate.py is the main file to clean the assay data. Currently accepts two arguements.
 - spectral_curate.py
    1. The path to the master spectral_data -i
    2. the output path -o
    3. will use the default Google-drive location in the config if input not specified
    4. if output not specified will edit inplace
### curate_merge.py outputs 3 csvs. takes 2 args. the path to the spectral data and the path to the assay data.\
     ## this script can be ignored
    1. cleaned file for the spectral master 
    2. cleaned file for the assay master
    3. merged file on the sample_ids with assay data.

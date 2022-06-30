# Kay_master_merge
 The script and tools to clean and merge Kay sample data
 Current tools:
- pull_sample_ids()
     - Searchs for columns named something similiar to sample
     - Takes the values in those columns and matches them to a regex pattern(located in the filter_config) 
     - merges the data based on the sample_id
     - drops columns with no data
- column_cleanup()
     - Uses mappings located in the filter config to merge columns with the same name but different column headers
- carrot_cleanup() 
     - sets values with '<' to - (logic here is that a less than value means the value is negligable so ' 0 ')\
     - sets values with > to the proper value or the converted percentage from the converted 'XX_2' column
## Clean.py is the main file to clean and merge the data. Currently accepts two arguements.
    1. The path to the master spectral_data -s
    2. the path to the master assay data -a
    3. will use the default drive location if not specified
### clean.py outputs 3 csvs.
    1. cleaned file for the spectral master 
    2. cleaned file for the assay master
    3. merged file on the sample_ids with assay data.

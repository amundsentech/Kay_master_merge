# Kay_curation_scripts
 The scripst and tools to clean and merge Kay sample data
 All data must be in csvs at the moment.
 Current tools:
- pull_sample_ids()
     - Searchs for columns named something similiar to sample
     - Takes the values in those columns and matches them to a regex pattern(located in the file_config) 
     - merges the data based on the sample_id
     - drops columns with no data
- column_cleanup()
     - Uses mappings located in the filter config to merge columns with the same name but different column headers
- carrot_cleanup() 
     - sets values with '<' to - (logic here is that a less than value means the value is negligable so ' - ')\
     - sets values with > to the proper value or the converted percentage from the converted 'XX_2' column
- Depth_ cleanup()
     - if there is no hole_id but the rest of the data looks correct, it will replace it with the foldername the data came from
     - drop no data columns
     - drop na samples
## XX_curate.py is the main curation file for a given data. Currently accepts one arguement.
ex= python3 structure_curate.py -i '/home/seabass/amcdrive/_AZ_Kay/_Master Databases/structure master.csv'
 - Use the 'file_config.py' to point at the locations of the file you want cleaned
 - run using XX_curate.py -r
    1. Each XX_curate.py has an associated config file. Update the configs with column mappings if necessary.
    
    2. the output path -o
    4. if output not specified will edit inplace(suggested usage)
    
### merge_curations2master.py outputs 1 master_MASTER.xlsx to the location It reads from
ex= python3 merge_curations2master.py -p '/home/seabass/amcdrive/_AZ_Kay/_Master Databases/
 - run using XX_curate.py -p
     -p is the path to all the curated .csvs

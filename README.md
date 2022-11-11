# Kay_curation_scripts
 The script and tools to clean and merge Kay samples data


## curate.py is the main curation file for a given diractory. specify file directory with -i arguement.
the script will then loop through all the files in the dir and standardize and clean them.
ex= python3 structure_curate.py -i '/home/seabass/amcdrive/_AZ_Kay/_Master Databases/'
 - Use the 'file_config.py' to point at the locations of the file you want cleaned
 - run using curate.py -r
    1. Each curate.py has an associated config file. Update the configs with column orders and sorting preferences if necessary.
    2. the output path -o
    3. -v is verbose will out put all steps during curation
    4. if output not specified will edit inplace(suggested usage)
    

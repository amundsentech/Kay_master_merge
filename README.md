# Kay_curation_scripts
 The script and tools to clean and merge Kay samples data


## curate.py is the main curation file for a given diractory. specify file directory with -i arguement.
the script will then loop through all the files in the dir and standardize and clean them.
python3 kay_curate/curate.py -i "${mount}/_AZ_Kay/_Master Databases/" 
python3 kay_curate/curation_merge.py -i "${mount}/_AZ_Kay/_Master Databases/"
    

import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd
import assay_sample_config as config
import file_config as fconfig
import datetime

def main(argv):
    assay_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('assay_samples_curate.py -i <input_file> -a <output_file>')
                print('using defaults in config if no file specified')
                
            elif opt in ("-i", "--input_file"):
                assay_file = arg
                print ('Input file is "', assay_file)
                assays=pd.read_csv(assay_file)
                output_file=assay_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(assay_file)==0:        
        assay_file=fconfig.assay_samples_file
        data=pd.read_csv(assay_file,low_memory=False)
        output_file=assay_file

    print ('Input file is ', assay_file)
    print ('Output file is ', output_file)
    print('------------------------------------------------------------------------------')
    print('################ ASSAY SAMPLES #############')
    msg = "Begin Cleaning"
    print(msg)
    #depth cleaner
    

    for map in config.mappings:
        data=ct.column_cleanup(data,mapping=map)

    #assays=ct.pull_hole_ids(assays,id_formats=config.hole_id_formats)
    data=ct.drop_no_data(data)
    data=ct.clean_column_names(data)
    data=ct.depth_cleanup(data)
    assay_fname= fconfig.assay_samples_fname
    
    print(f'output {assay_fname}')
    assays.to_csv(output_file,index=False)
    print('------------------------------------------------------------------------------')
    return assays

if __name__ == "__main__":
    main(sys.argv[1:])
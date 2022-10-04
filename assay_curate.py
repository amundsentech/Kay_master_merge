import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd
import assay_config as config
import file_config as fconfig
import datetime

def main(argv):
    assay_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('assay_curate.py -i <input_file> -a <output_file>')
                print('using defaults in config, no file specified')
                
            elif opt in ("-i", "--input_file"):
                assay_file = arg
                print (f'Input file is ', assay_file)
                assays=pd.read_csv(assay_file)
                output_file=assay_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(assay_file)==0:
        assay_file=fconfig.assay_file
        assays=pd.read_csv(assay_file,low_memory=False)
        output_file=assay_file
        

    print ('Input file is ', assay_file)
    print ('Output file is ', output_file)
    print('################ ASSAYS #############')
    msg = "Begin Cleaning"
    print(msg)
    #pull sample ids
    assays=ct.pull_sample_ids(assays,config.sample_id_formats)
    #### clean and fill spec data
    assays=ct.carrot_cleanup(assays)
    for map in config.mappings:
        assays=ct.column_cleanup(assays,mapping=map)
    

    assay_fname= fconfig.assay_fname

    
    print(f'output {assay_fname}')
    assays.to_csv(output_file)
    return assays

if __name__ == "__main__":
    main(sys.argv[1:])
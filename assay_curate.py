import getopt,sys


import pandas as pd
import cleaningtools as ct
import filter_config as config
import datetime

def main(argv):
    assay_file=config.assay_file

    try:
        opts, args = getopt.getopt(argv,"ci:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-c':
                print ('test.py -i <input_file> -a <output_file>')
                sys.exit()
            elif opt in ("-i", "--input_file"):
                assay_file = arg
            elif opt in ("-o", "--output_file"):
                assay_file = arg
        print ('Input file is "', config.spec_file)
        print ('Output file is "', config.path, config.output)
    except getopt.GetoptError:
        print ('test.py -i <input_file> -a <output_file>')
        print('using default paths')
    
    
    assays=pd.read_csv(assay_file,low_memory=False)
    msg = "Begin Cleaning"
    print(msg)
    #pull sample ids
    assays=ct.pull_sample_ids(assays)
    #### clean and fill spec data
    assays=ct.carrot_cleanup(assays)
    assays=ct.column_cleanup(assays,mapping=config.depth_mapping)
    assays=ct.column_cleanup(assays,mapping=config.file_mapping)

    assay_fname= config.assay_fname
        ## out put final csvs
    path=config.output_path

    
    print(f'output {assay_fname}')
    assays.to_csv(path+assay_fname)
    return assays

if __name__ == "__main__":
    main(sys.argv[1:])
import getopt,sys
import subprocess
try:
    print('check for pandas')
    import pandas as pd
    
except:
    print('install pandas')
    subprocess.check_call([sys.executable,'-m','pip','install','pandas'])

import cleaningtools as ct
import filter_config as config
import datetime

def main(argv):
    assay_file=config.assay_file
    assay_file='https://drive.google.com/uc?id=' + assay_file.split('/')[-2]
    output_file=config.output_path+config.assay_fname
    assays=pd.read_csv(assay_file,low_memory=False)
    try:
        opts, args = getopt.getopt(argv,"ci:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-c':
                print ('spectral_curate.py -i <input_file> -a <output_file>')
                sys.exit()
            elif opt in ("-i", "--input_file"):
                assay_file = arg
                print ('Input file is "', assay_file)
                assay=pd.read_csv(assay_file)
                output_file=config.output_path+assay_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError:
        print ('file error read from google drive')
        

    print ('Input file is ', assay_file)
    print ('Output file is ', output_file)
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
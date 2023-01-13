import getopt,sys
import subprocess
import os
import cleaningtools as ct 
import pandas as pd
import curate_config as config
from tqdm.auto import tqdm
import numpy as np
import datetime
import glob

def main(argv):
    dir=[]
    verbose=config.verbose
    try:
        opts, args = getopt.getopt(argv,"ri:o:v:",["input_file=","output_file=",'verbose='])
        for opt, arg in opts:
            if opt == '-r':
                print ('curate.py -i <input_dir> -o <output_dir>')
                print('using default location in yaml if no file specified')
                
            elif opt in ("-i", "--input_dir"):
                dir = arg
                print (f'Input file location is {arg} ',)
                output_dir=dir
            elif opt in ("-o", "--output_file"):
                output_dir= arg
                print ('Output directory is ', output_dir)

            elif opt in ("-v", "--verbose"):
                verbose=arg
                print ('Verbose= ', verbose)

    except getopt.GetoptError as e:
        print (e)
        print ('FILE Location ERROR: read from CONFIG')
    
    if len(dir)==0:
        dir=config.dir
        output_dir=config.dir

    print ('Input file directory is ', dir)
    print ('Output file directory is ', output_dir)

    print('------------------------------------------------------------------------------')
    print('################ CURATE DATA #############')

    verbose=config.verbose
    pbar=tqdm(sorted(os.listdir(dir)))
    master_dic={}
    for file in pbar:
        new=False
        if file.endswith('.csv'):
            filename=file.split('.')[0]
            if file not in master_dic:
                new=True
                master_dic[filename]=pd.DataFrame()
            pbar.set_postfix_str(f'{file}')
            # print('-----------------------------------')
            # print('Cleaning',file)
            try:
                if verbose:
                    print(file)
                data=pd.read_csv(dir+file,low_memory=False)
                data=ct.drop_bad_columns(data,verbose=verbose)
                data=ct.clean_column_names(data)
                data=ct.merge_duplicate_columns(data)
                data=ct.drop_work_order(data,verbose=verbose)
                data=ct.round_depths(data,verbose=verbose)
                data=ct.reorder_columns(data,col_order=config.col_order,verbose=verbose) 
                
                ## this is a legacy line needed before the upgrade the new merge script performs this
                #data=ct.drop_bad_rows(data,na_threshold=config.na_threshold,targets=config.targets,verbose=verbose)
                data=ct.sort_data(data)
                output=output_dir+filename+'.csv'
                print('output location:')

                print(output)
                data.to_csv(output,index=False)


            except Exception as e:
                print('________')
                print('did not write file')

                print(file)
                print(e)
                continue
    print('------------------------------------------------------------------------------')
    print('FINISHED CURATION')

if __name__ == "__main__":
    main(sys.argv[1:])
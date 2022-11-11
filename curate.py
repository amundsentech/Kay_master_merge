import getopt,sys
import subprocess
import os
import cleaningtools as ct 
import pandas as pd
import curate_config as config
from tqdm.auto import tqdm
import numpy as np
import datetime

def main(argv):
    dir=[]
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
                data=pd.read_csv(dir+file,low_memory=False)
                data=ct.drop_bad_columns(data,verbose=verbose)
                data=ct.clean_column_names(data)
                data=ct.reorder_columns(data,col_order=config.col_order,verbose=verbose)
                data=ct.drop_bad_rows(data,na_threshold=config.na_threshold,targets=config.targets,verbose=verbose)
                data=ct.sort_data(data)
                data.to_csv(output_dir+filename+'.csv',index=False)


            except Exception as e:
                print(file)
                print(e)
                continue


    print('------------------------------------------------------------------------------')
    print('################ MERGE SAMPLES AND DATA #############')
    ## merge the cleaned up data

    sample_files=[]
    data_files=[]
    for file in os.listdir(dir):
        if 'sample' in file:
            print(file)
            sample_files.append(file)

    for d_file in os.listdir(dir):
        if d_file not in sample_files:
            d_name=d_file.split(' ')
            for s_file in sample_files:
                s_name=s_file.split(' ')
                if s_name[:2]==d_name[:2]:
                    if'merge'not in(d_name):
                        data_files.append(d_name)
                        basename=" ".join(s_name[:2])
                        try:
                            d_data=pd.read_csv(dir+d_file,low_memory=False)
                            s_data=pd.read_csv(dir+s_file,low_memory=False)
                        except Exception as e:
                            print(e)
                            continue

                        d_col=d_data.filter(like='sample').columns[0]
                        s_col=s_data.filter(like='sample').columns[0]
                        try:
                            data=pd.merge(s_data,d_data,left_on=s_col,right_on=d_col,how='outer',suffixes=['_'+s_name[2],'_'+d_name[2]] )
                            data=ct.sort_data(data,verbose=True)
                        except Exception as e:
                            print(e)
                        if verbose:
                            print(f'Merging {" ".join(s_name)} samples with {" ".join(d_name)} data')
                            print(f'Using column: {s_col} in the sample sheet')
                            print(f'Using column: {d_col} in the data sheet')
                        data.to_csv(f'{output_dir}{basename} master.csv',index=False)
    print('FINISHED CURATION')

if __name__ == "__main__":
    main(sys.argv[1:])
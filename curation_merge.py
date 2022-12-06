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
    verbose=config.verbose
    try:
        opts, args = getopt.getopt(argv,"ri:o:v:",["input_file=","output_file=",'verbose='])
        for opt, arg in opts:
            if opt == '-r':
                print ('curation merge.py -i <input_dir> -o <output_dir>')
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
        output_dir=config.output_dir

    print ('Input file directory is ', dir)
    print ('Output file directory is ', output_dir)

    verbose=config.verbose
    print('------------------------------------------------------------------------------')
    print('################ MERGE SAMPLES AND DATA #############')
    ## merge the cleaned up data

    sample_files=[]
    data_files=[]
    for file in os.listdir(dir):
        if 'sample' in file:
            print(file)
            sample_files.append(file)
    files=[f for f in os.listdir(dir) if f.endswith('.csv')]
    files=[f for f in files if 'merged' not in f]
    for d_file in files:
        if d_file not in sample_files:
            d_name=d_file.split(' ')
            for s_file in sample_files:
                merge=False
                s_name=s_file.split(' ')
                if (s_name[:2]==d_name[:2]):
                    merge=True
                elif (s_name[:2]==['drill','samples']) and (d_name[:2]==['drill','geochemical']):
                    merge=True
                if merge==True:
                    data_files.append(d_name)
                    basename=" ".join(d_name[:2])
                    try:
                        d_data=pd.read_csv(dir+d_file,low_memory=False)
                        s_data=pd.read_csv(dir+s_file,low_memory=False)
                    except Exception as e:
                        print(e)
                        continue
                    
                    d_col=d_data.filter(like='sample').columns[0]
                    s_col=s_data.filter(like='sample').columns[0]

                    if 'terraspec' in s_name:
                        s_col=s_data.filter(like='file').columns[0]

                    try:
                        #data=pd.concat([s_data.set_index(s_col),d_data.set_index(d_col)], axis=1, join='inner')
                        data=pd.merge(  
                                        s_data.drop_duplicates(subset=[s_col],keep='first'),
                                        d_data.drop_duplicates(subset=[d_col],keep='first'),
                        left_on=s_col,
                        right_on=d_col,
                        how='left',
                        suffixes=['_'+s_name[2],'_'+d_name[2]],
                        )
                        data=ct.sort_data(data,verbose=True)
                    except Exception as e:
                        print('___________')
                        print('MERGE FAIL')
                        print(e)
                    if verbose:
                        print(f'Merging {" ".join(s_name)} samples with {" ".join(d_name)} data')
                        print(f'Using column: {s_col} in the sample sheet')
                        print(f'Using column: {d_col} in the data sheet')
                    output=f'{output_dir}{basename}_merged.csv'
                    print('output location:')
                    print(output)
                    try:
                        data.to_csv(output,index=False)
                    except Exception as e:
                        print(e)
    print('------------------------------------------------------------------------------')
    print('FINISHED MERGE')

if __name__ == "__main__":
    main(sys.argv[1:])
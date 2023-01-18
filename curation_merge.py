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
    files= os.listdir(dir)
    files=[f for f in files if 'drill' in f]
    files=[f for f in files if f.endswith('.csv')]
    files=[f for f in files if 'merged' not in f]
    files=[f for f in files if 'shift' not in f]

    samples=[f for f in files if 'samples' in f]

    keys=sorted([k.split(' ')[1] for k in samples]+['geochemical'])
    all_samples=[k for k in samples if k.split(' ')[1] =='samples']
    d_list=[]
    keys.remove('samples')
    print(keys,all_samples)

    for k in keys:
        try:
            merge_files=[f for f in files if k in f ]
            globed=''.join(merge_files)
            if 'geochemical' in globed or 'hyp-pkg' in globed:
                merge_files+=all_samples
            print('---------------------------------------------------')
            merg_files=sorted(merge_files)
            print(merge_files)
            base=merg_files[0].split(' ')
            basename=' '.join(base[:2])
            print(basename)


            if len(merge_files)<=2:
                s_file=merge_files[-1]
                s_name=merge_files[-1].split('.')[0]
                s_data=pd.read_csv(dir+s_file,low_memory=False)
                s_col=s_data.filter(like='sample').columns[0]


                d_file=merge_files[0]
                d_name=merge_files[0].split('.')[0]
                d_data=pd.read_csv(dir+d_file,low_memory=False)
                d_col=d_data.filter(like='sample').columns[0]
                d_sub=d_name.split(' ')[2]
                
                if 'terraspec' in d_file:
                    s_col=s_data.filter(like='file_name').columns[0]

                if 'geochemical' in d_file:
                    s_sub=s_name.split(' ')[1]
                else:
                    s_sub=s_name.split(' ')[2]


                
                print(f'Merging {s_name}  with {d_name} data')
                print('using columns')
                print(s_col,';',d_col)
                #data=pd.concat([s_data.set_index(s_col),d_data.set_index(d_col)], axis=1, join='inner')
                data=pd.merge(  
                        s_data.drop_duplicates(subset=[s_col],keep='first'),
                        d_data.drop_duplicates(subset=[d_col],keep='first'),
                left_on=s_col,
                right_on=d_col,
                how='inner',
                suffixes=['_'+s_sub,'_'+d_sub],
                )
            
            
            if len(merge_files)>2:

                s_file=merge_files[-1]
                s_name=merge_files[-1].split('.')[0]
                s_data=pd.read_csv(dir+s_file,low_memory=False)
                s_col=s_data.filter(like='sample').columns[0]

                d_file=merge_files[0]
                d_name=merge_files[0].split('.')[0]
                d_data=pd.read_csv(dir+d_file,low_memory=False)
                d_col=d_data.filter(like='sample').columns[0]

                d_file2=merge_files[1]
                d_name2=merge_files[1].split('.')[0]
                d_data2=pd.read_csv(dir+d_file2,low_memory=False)
                d_col2=d_data2.filter(like='sample').columns[0]

                s_sub=s_name.split(' ')[1]
                d_sub=d_name.split(' ')[2]
                d_sub2=d_name2.split(' ')[2]


                print(f'Merging {s_name} samples with {d_name} samples')
                print('using columns')
                print(s_col,':',d_col)
                #data=pd.concat([s_data.set_index(s_col),d_data.set_index(d_col)], axis=1, join='inner')
                data=pd.merge(  
                        s_data.drop_duplicates(subset=[s_col],keep='first'),
                        d_data.drop_duplicates(subset=[d_col],keep='first'),
                left_on=s_col,
                right_on=d_col,
                how='outer',
                suffixes=['_'+s_sub,'_'+d_sub],
                )
                print(f'Merging {s_name} + {d_name} with {d_name} data')

                data=pd.merge(  
                                data.drop_duplicates(subset=[s_col],keep='first'),
                                d_data2.drop_duplicates(subset=[d_col2],keep='first'),
                                left_on=s_col,
                                right_on=d_col,
                                how='inner',
                                suffixes=['_'+s_name,'_'+d_name2[2]],
                                )
            data=ct.merge_duplicate_columns(data)
            data=ct.sort_data(data)
            data=ct.reorder_columns(data,verbose=True)
            data=ct.fix_depths(data)
            data=ct.round_depths(data)


            d_list.append(data)
            print('----------------------------')
            output=f'{dir}{basename}_merged.csv'
            print('output location:')
            print(output)                    
        except Exception as e:
            print('___________')
            print('MERGE FAIL')
            print(e)
        try:
            data.to_csv(output,index=False)
        except Exception as e:
            print(e)

    print('------------------------------------------------------------------------------')
    print('FINISHED MERGE')

if __name__ == "__main__":
    main(sys.argv[1:])
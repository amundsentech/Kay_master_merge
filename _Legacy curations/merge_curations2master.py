import getopt,sys
import subprocess

import pandas as pd
import cleaningtools as ct 
import file_config as fconfig
import merge_config as config

import numpy as np
import math
from tqdm import tqdm as tqdm
tqdm.pandas()
import os
import file_config as fconfig
import pandas as pd

def clean_for_merge(data):
    for col in data.columns:
        if 'depth_ft'in col.lower():
            data['from_ft']=data[col]
            data['to_ft']=data['from_ft'].shift(-1)-1
            #convert ft to meters
            data['from_m']=data['from_ft']* .3281
            data['to_m']=data['to_ft'] * .3281
            data=data.drop(data.filter(like='Depth').columns,axis=1)
        if ('hole' in col.lower())& ('id' in col.lower()):
            data[col]=data[col].astype(object)
            data.rename(columns={f'{col}':f'hole_id'},inplace=True)
        try: 
            data[col]=data[col].str.strip()
        except Exception as e:
            pass
            #print(f'{col}: {e}')
        data.rename(columns={f'{col}':f'{col.strip().lower()}'},inplace=True)
        data=data.drop(data.filter(like='unnamed'),axis=1)
        if 'from_ft'in col.lower():
            try:
                drop_index=data[data['from_ft'].isna()].index
                data=data.drop(drop_index,axis=0)
            except Exception as e:
                pass
                #print(f'{e}')
    if 'hole_id' not in data.columns:
        data['hole_id']=np.nan
    if 'recvd wt.'  in data.columns:
        try:
            data['recvd wt.']=pd.to_numeric(data['recvd wt.'],errors='coerce')
            data['from_ft']=pd.to_numeric(data['from_ft'],errors='coerce')
        except Exception as e:
            print(e)
            pass
    names=data.loc[:,data.columns.duplicated()].columns
    if len(names)>0:
        print(f'duplcated column: {names} drop or else the nasty merge bug')
        data=data.loc[:,~data.columns.duplicated()].copy()

    return data

def fill_merge_groups(data):
    data=data.fillna(method='ffill')
    data=data.fillna(method='bfill')
    data=data.drop_duplicates(keep='first')
    return data
def explode_depths(data):
    data[['from_ft','to_ft']]=data[['from_ft','to_ft']].fillna(0)
    if 'sample_id' in data.columns:
        zipped=zip(data['sample_id'],data['hole_id'], data['from_ft'], data['to_ft'])
        depths=pd.DataFrame([(s_id,h_id, y) for s_id,h_id, start, end in zipped for y in np.arange(start, end,.5)],
                    columns=['sample_id','hole_id','true_depth'])
        d_frame=depths.merge(data,on=['sample_id','hole_id'])
        d_frame=depths.merge(data,on=['sample_id','hole_id'])
    else:
        data['START']=data['from_ft']
        zipped=zip(data['START'],data['hole_id'], data['from_ft'], data['to_ft'])
        depths=pd.DataFrame([(s,h_id, y) for s,h_id, start, end in zipped for y in np.arange(start, end,.5)],
                        columns=['START','hole_id','true_depth'])
        d_frame=depths.merge(data,on=['START','hole_id'])
        d_frame=d_frame.drop('START',axis=1)
    d_frame=d_frame.drop(d_frame.filter(like='from').columns,axis=1)
    d_frame=d_frame.drop(d_frame.filter(like='to').columns,axis=1)
    return d_frame

def pull_start_end(data):
    depths=data['true_depth']
    start=depths.values[0]
    end=depths.values[-1]
    data['from_ft']=start
    data['to_ft']=end
    data=data.drop_duplicates(subset=['from_ft','to_ft'],keep='first')
    return data

def merge_dflist(data_list,data_names):
    big_df=pd.DataFrame()
    non_id_cols=['true_depth', 'hole_id']
    for i,data in enumerate(data_list):
        ## merge all the data with sample_ids
        name=data_names[i]
        suf=name.split(' ')[0]
        print(f"####### merge frame {i}: {name} suffix= {suf} #######")
        data=data.astype(object)
        big_df=big_df.astype(object)
        big_cols=list(big_df.columns)
        small_cols=list(data.columns)
        
        dups=sorted([col for col in big_cols if col in small_cols])
        cols=config.main_columns
        try:
            [dups.remove(x) for x in ['file','folder','start_depth','end_depth']if x in data.columns]
        except:
            pass
        if 'sample_id' not in data.columns:
            cols=non_id_cols
            try:
                big_index=list(big_df.hole_id.unique())
                small_index=list(data.hole_id.unique())
                same_ids= [id for id in big_index if id in small_index]
            except Exception as e:
                print(e)
                same_ids=[]
            dups=non_id_cols
        else:
            big_index=list(big_df.index)
            small_index=list(data.index)
            same_ids= [id for id in big_index if id in small_index]
        print(f'common columns {dups}')
        n_ids=len(same_ids)
        if n_ids==0:
            print(f'{n_ids} common ids concat')
            big_df=pd.concat([big_df,data],axis=0,join='outer')
        else:
            print(f'{n_ids} common ids merge')
            big_df=big_df.merge(data,on=dups,suffixes=[None,'_'+suf],how='outer')

        print(f'data shape {big_df.shape}')
    
    not_dups=[i for i in big_df.columns if i not in cols]
    big_final=pd.concat([big_df[cols],big_df[not_dups]],axis=1)

    big_final.drop(big_final.filter(like='file').columns,axis=1,inplace=True)
    big_final.drop(big_final.filter(like='folder').columns,axis=1,inplace=True)
    big_final.sort_index(inplace=True)
    return big_final

def main(argv):
    path=[]
    hole_list=[]
    sample_list=[]
    sample_data_names=[]
    hole_data_names=[]
    try:
        opts, args = getopt.getopt(argv,"rp:",["input_path="])
        for opt, arg in opts:
            if opt == '-r':
                print ('merge_curations2master.py -p <input_path> ')
                print('using defaults if no file specified')
                
            elif opt in ("-p", "--input_path"):
                path = arg
                print (f'Input path is {arg} ',)

    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR: read from CONFIG')
    print('------------------------------------------------------------------------------')
    if len(path)==0:
        path=fconfig.output_path
    files=[file for file in os.listdir(path) if file.endswith('.csv')]
    for file in files:
        name=file.split('.')[0]
        if len(name)==0:
            continue
        print(f'read {name}')
        try:
            data=pd.read_csv(path+file,low_memory=False,on_bad_lines='skip')

        except Exception as e:
            print(e)
            print('likely not a csv')
            continue
        print(f'clean {name}')
        data=clean_for_merge(data)

        if 'sample_id' in data.columns:
            print(f'{name} has sample ids')
            sample_list.append(data)
            sample_data_names.append(name)
        else:
            print(f'{name} does not have sample ids')
            print(f'explode {name}')
            try:
                data=explode_depths(data)
                hole_list.append(data)
                hole_data_names.append(name)
            except Exception as e:
                print(e)
                print('must have (depths and hole ids) or (sample_ids) to merge into master')

    big_samples=merge_dflist(sample_list,sample_data_names)
    print('FINISHED MERGING SAMPLES')
    big_holes=merge_dflist(hole_list,hole_data_names)

    print('#####clean the sample_ids#########')
    big_samples=big_samples.groupby(['sample_id']).progress_apply(fill_merge_groups).droplevel(level=0)
    print('#####explode sample_ids#########')
    samp_ex=explode_depths(big_samples)
    print('#########merge holes and samples##########')
    merged=samp_ex.merge(big_holes,on=['hole_id','true_depth'],how='outer')
    print('clean the final_data')

    dups=merged[merged.drop('true_depth',axis=1).duplicated(keep=False)]
    print('#########Clean Merged data##########')
    merged=merged.groupby(['hole_id','true_depth']).progress_apply(fill_merge_groups).reset_index(drop=True)
    print('#########Clean Merged data##########')
    merged['u_id']=merged.fillna(np.inf).groupby(merged.drop('true_depth',axis=1).columns.to_list()).ngroup()
    merged['from_ft']=np.inf
    merged['to_ft']=np.inf

    merged_test=merged.groupby(merged['u_id']).progress_apply(pull_start_end).reset_index(drop=True)

    merged_test.drop('true_depth',axis=1, inplace=True)

    final_cols=['sample_id','hole_id','from_ft','to_ft']
    des_cols = merged_test.filter(like='description').columns
    other_cols= [col for col in merged_test.columns if col not in final_cols]
    merged_test=pd.concat([merged_test[final_cols],merged_test[des_cols],merged_test[other_cols]],axis=1)
    merged_test=merged_test.T.drop_duplicates(keep='first').T

    for col in merged_test.columns:
        if merged_test[col].isna().sum()==len(merged_test):
            print(f'drop {col}: no data')
            merged_test=merged_test.drop(col,axis=1)
    merged_test=merged_test.sort_values(by=['sample_id'],ascending=False)
    merged_test=merged_test.sort_values(by=['hole_id','from_ft'],ascending=True)
    #ct.generate_from_to(data,sort_by=['sample_id','hole_id','depth_ft'])
    #merged_test=ct.remove_depth_errors(merged_test)
    merged_test=merged_test.set_index('sample_id')
    print(f'export {path} master_MASTER.xlsx')

    merged_test.to_excel(path+'master_MASTER.xlsx')
    print('------------------------------------------------------------------------------')

if __name__ == "__main__":
    main(sys.argv[1:])
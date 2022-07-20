from logging import exception
import sys
import subprocess
import math
import importlib



pkgs = {'pandas': 'pd', 'tqdm': 'tqdm','numpy':'np'}
def check_packages():
    for p in pkgs:
        s = pkgs[p]
        try:
            print(f'check for {p}')
            s = importlib.import_module(p)
            
        except ImportError:
            print(f'{p} is not installed and has to be installed')
            subprocess.call([sys.executable, '-m', 'pip', 'install', p])
        finally:
            s = importlib.import_module(p)
            print(f'{p} is properly installed')
    return
try:
    check_packages()
except:
    print('upgrade pip then try again')
    subprocess.check_call([sys.executable,'-m','pip','install','--upgrade','pip'])
    check_packages()

import pandas as pd
import numpy as np
from tqdm import tqdm
import assay_config as config

def pull_sample_ids(data,id_formats):
    print('Sample_ids')
    
    data=data.replace(' ','')
    ## fix index
    data.index=data.index.astype(int)
    ##search for columns with samp in thier names 
    sample_ids=[samp for samp in list(data.columns) if ('samp' in samp.lower())]
    print(f'get sample ids from {sample_ids},with forms {id_formats}')
    data['sample_id']=''
    sample_cols=[]
    ##search for Id formats in the previously found coulmns and merge 
    for i in range(len(id_formats)):
        i_format=id_formats[i]
        for col in sample_ids:
            print(f'search {col} for format {i_format}')
            
            data[col]=data[col].astype(str)
            data[col]=data[col].fillna('')
            if data[col].str.contains(i_format).any():
                sample_cols.append(col)
                print(f'{col} has format{i_format}')
                extract=data[col].str.extract(i_format).fillna('')[0]
                data['sample_id']=data['sample_id']+extract
            else: 
                print(f'{col} is not an id column')
    print(sample_cols)
    data=data.sort_values('sample_id')
    data=data.set_index('sample_id')
    # try:
    #     sample_cols.remove('sample_id')
    # except Exception as e:
    #     print(e)
    data=data.drop(sample_cols,axis=1)
    #drop data with no values
    for col in data.columns:
        if data[col].isna().sum()==len(data):
            print(f'Drop {col}: no data')
            data=data.drop(col,axis=1) 
    return data

def pull_hole_ids(data,id_formats):
    print('pulling Hole_ids')
    data=data.replace(' ','')
    ## fix index
    data.index=data.index.astype(int)
    hole_cols=[]
    if 'hole_id' not in data.columns:
        data['hole_id']=''

    ##search for Id formats in the coulmns and merge 
    for i in range(len(id_formats)):
        i_format=id_formats[i]
        for col in data.columns:
            print(f'search {col} for format {i_format}')
            
            data[col]=data[col].astype(str)
            data[col]=data[col].fillna('')
            if data[col].str.contains(i_format,).any():
                hole_cols.append(col)
                print(f'{col} has format{i_format}')
                extract=data[col].str.extract(i_format, expand=False).fillna('')[0]
                data['hole_id']=data['hole_id']+extract
            else: 
                print(f'{col} is not an id column')
    #drop data with no values
    for col in data.columns:
        if data[col].isna().sum()==len(data):
            print(f'Drop {col}: no data')
            data=data.drop(col,axis=1) 

    return data

'''
column clean up just loops through the mappings
'''
def column_cleanup(data,mapping=config.depth_mapping):
    print('Column cleanup')
    data=data.astype(str)
    for value in mapping.values():
        if value in data.columns:
            data[value].fillna('',inplace=True)
        else: 
            data[value]=''
    for key,value in mapping.items():
        print (f'add {key} to {value} and drop {key}')
        try:
            data[value]=data[value].values.copy()+data[key].values.copy()
            data[value].fillna('',inplace=True)
            # data[value].replace({'':'nan'},inplace=True)
            
            data.drop(key,axis=1,inplace=True)
            # data=pd.concat([data,data[value].copy()],axis=1)
        except Exception as e:
            print(e)
    for col in data.columns:
        try:
            data[col]=data[col].str.strip('nan')
            
        except Exception as e:
            print(e)
    data=data.drop(data.filter(like='\r').columns,axis=1)
    return data
'''
carrot clean up just loops through the mappings
'''
def carrot_cleanup(data):
    carrots=['>','<']
    for col in data.columns:
        print(col)
        data[col]=data[col].astype(str).str.strip()
        more_index=data[col][data[col].str.startswith(carrots[0])].index
        less_index=data[col][data[col].str.startswith(carrots[-1])].index
        data[col]=data[col].astype(str).replace({'<':"-"},regex=True)
        data[col]=data[col].astype(str).replace({'>':""},regex=True)
        col2=f'{col}_2'
    return data

def depth_cleanup(data,hole_id_formats=[]):
    print('clean up depths and hole_ids')
    for col in data.columns:
        if 'hole' in col.lower() and 'id' in col.lower():
            print(f'use {col} as the hole id columns')
            hole=col
            if data[hole].str.contains('XX',na=False).any():
                drop_index=data[data[hole].str.contains('XX',na=False)].index
                data.drop(drop_index,axis=0,inplace=True)
        if hole_id_formats:
            for i_format in hole_id_formats: 
                print (f'{col} searching for {i_format}')
                try:
                    if data[col].str.contains(i_format).any():
                        extract=data.loc[data[data[hole].isna()==True].index,col].str.extract(i_format, expand=False)
                        extract=extract.squeeze()
                        holes=extract.unique()
                        fill_index=data[data[hole].isna()==True].index
                        print(f'fill {hole}, {fill_index} with {holes} from {col}')
                        data.loc[data[data[hole].isna()==True].index,hole]=extract
                except Exception as e:
                    print (e)
                    print ('no hole ids')
        if 'geo' == col.lower():        
            geo=col
            print(f'use {col} as the Geo column')
        if 'sample' in col.lower() and 'id' in col.lower():        
            sample=col
            print(f'use {col} as the sample_id column/ drop na samples')
            drop_index=data[data[sample].isna()].index
            data.drop(drop_index,axis=0,inplace=True)
        if data[col].isna().sum()==len(data):
            print(f'dropping {col}')
            data.drop(col,axis=1,inplace=True)
    try:
        print ('drop na hole ids')
        data.drop(data[(data[hole].isna()==True)& (data[geo].isna()==True)].index,axis=0,inplace=True)
    except Exception as e:
        print (e)
        print ('no hole ids')

    na_num=math.floor(data.shape[1]/2)
    data=data.drop(data[data.isna().sum(axis=1)>=(na_num)].index,axis=0)
    print ('drop na rows')
    return data


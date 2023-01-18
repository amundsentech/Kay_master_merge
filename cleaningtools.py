from logging import exception
import sys
import subprocess
import math
import importlib


pkgs = {'pandas': 'pd', 'tqdm': 'tqdm','numpy':'np','openpyxl':'openpyxl','xlwings':'xlwings'}
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
import curate_config as config




def clean_column_names(data):
    try:
        columns=[str(c) for c in data.columns]
        data.columns=[c.replace(' ','_').lower() for c in columns]
        data.columns=[c.replace('__','_') for c in data.columns]
        data.columns=[c.replace('sampleid','sample_id').lower() for c in data.columns]
        data.columns=[c.replace('holeid','hole_id').lower() for c in data.columns]

        data.rename(columns={'depth':'depth_ft'},inplace=True)

        data=data.groupby(level=0,axis=1).sum(numeric_only=False)



    except:
        print('error in cleaning the column names')
    return data

def merge_duplicate_columns(df, method="unique", sep=""):
    duplicated =  df.columns[df.columns.duplicated()].unique()
    print('######duplicated_columns#####')
    print(duplicated)
    try:
        if method == "join":
            for d in duplicated:
                df[d] = df.pop(d).fillna("").astype(str).apply(sep.join, axis=1)
                
        elif method == "unique":
            for d in duplicated:
                df[d] = df.pop(d).fillna("").astype(str).apply(lambda x: sep.join(x.unique()),axis=1) 
                        
        elif method == "sum":
            for d in duplicated:
                df[d] = df.pop(d).sum(axis=1)
    
    except Exception as e:
        print('error merging duplicate columns')
        print(e)

    return df

def reorder_columns(data,verbose=False,col_order=['work_order','sample_id','hole_id','from_ft','to_ft','from_m','to_m','depth_ft','depth_m','depth','depthfrom','depthto']):
    new_order=col_order.copy()
    for c in col_order:
        i=new_order.index(c)
        if '_'in c:
            new=c.replace('_','')
            new_order.insert(i+1,new)
    #look in the data for the columns we want
    #look in the data for the columns we want

    u_cols=set([c for c in new_order if c in data.filter(like=c).columns])
    # set alphabetizies them so we need to reorder basded
    first_cols=[c for c in new_order if c in u_cols]
    last_cols= [c for c in data.columns if c not in first_cols]
    col_order=first_cols+last_cols
    col_order=[c for c in col_order if c in data.columns]
    if verbose:
        print('first columns before sort')
        print([c for c in data.columns][:15])
        print('first columns after sort')
        print(col_order[:15])
    try:
        data=data[col_order]
    except Exception as e:
        print('Error re ordering columns')
        print(e)
    return data
        
def drop_bad_rows(data,na_threshold=2,targets=['ft','hole'],verbose=False):
    target_rows=[]
    for f in targets:
        try:
            trow=data.filter(like=f).columns[0]
            target_rows.append(trow)
        except:
            pass
    for col in target_rows:
        pass
    try:
        drop_index=data[(data.notna().sum(axis=1)<=na_threshold)].index
        
        if verbose:
            print(f'drop {len(drop_index)} na rows in locations: {drop_index}')
        data=data.drop(drop_index,axis=0)
        if len(drop_index)==len(data):
            if verbose:
                print('dropped all of the data only contained empty cells')
            
    except Exception as e:
        print('Error dropping bad rows')
        print(e)
    return data

def drop_work_order(data,verbose=False):
    if verbose:
        print('## Drop work_order column ##')
    work=data.filter(like='work_order').columns
    if len(work)>0:
        data = data.drop(work,axis=1)
    return data

def drop_bad_columns(data,verbose=False):
    if verbose:
        print('## Drop no data columns ##')
    dropped_cols=[]
    for col in data.columns:
        try:
            data[col]=data[col].replace({'':np.nan})
        except Exception as e:
            print(e)
        try:
            if data[col].isna().sum()==len(data):
                dropped_cols.append(col)
                data.drop(col,axis=1,inplace=True)
        except Exception as e:
            print('Error dropping bad columns')
            print(e)
    if verbose:
        print(f'Dropped {dropped_cols}: no data')
    return data

def sort_data(data,sorters=['hole','ft','sample'],verbose=False):
    sort_by=[]
    for c in sorters:
        try:
            all_columns=data.filter(like=c,axis=1).columns
            sort_by.append(all_columns[0])
        except Exception as e:
            print('Error in sorting')
            print(c,'not in the columns')
            print(e)
    if verbose:
        print(f'using {sort_by} for sorting the data')
    try:
        data=data.sort_values(sort_by,axis=0,ascending=True).reset_index(drop=True)
    except Exception as e:
        print('Error in sorting')
        print(e)
    return data
       
def get_base_path(path,start_point='_AZ_Kay'):

    path_list=path.split('/')
    b=path_list.index(start_point)
    base_path='/'.join(path_list[:b+1])
    return base_path

def round_depths(data,targets=['_m','_ft','recovery','depth'],verbose=False):
    if verbose:
        print('###rounding depths#####')
    for t in targets:
        cols=list(data.filter(like= t).columns)
        if len(cols)>0:
            print("rounding:",cols)
            for col in cols:
                try:
                    ser=pd.to_numeric(data[col],errors='coerce',)
                    ser=ser.astype(float)

                    ser=ser.round(1)
                    ser=ser.map('{:.1f}'.format)
                    data.loc[ser[ser.notna()==True].index,col]=ser[ser.notna()==True]
                except:
                    pass

    return data

def drop_hash(data, verbose=True):
    print('####DROP HASH #########')
    try:
        print('Dtype',data['depth_m'].dtype)   
        data['depth_m']=pd.to_numeric(data['depth_m'],errors='coerce')
        data['depth_m']=data['depth_m'].replace(0.0,np.nan)
        drop=(data[data['depth_m'].isna()==True]).index
        print('Dropping ',drop)   
        data=data.drop(drop,axis=0)
        data['depth_m']=data['depth_m'].replace(0.0,np.nan)
        data=data.drop(drop,axis=0)
        print('Dropping ',drop)        
        drop=(data[data['depth_m']==0]).index
        data=data.drop(drop,axis=0)
    except Exception as e :
        if verbose:
            print (e)
        pass

    try:
        drop=(data[(data['recovery_%']=='#DIV/0!')]).index
        data['recovery_%']=pd.to_numeric(data['recovery_%'],errors='coerce')
        data['recovery_%']=data['recovery_%'].replace(0.0,np.nan)
        drop=(data[data['recovery_%'].isna()==True]).index
        print('Dropping ',drop) 

        data=data.drop(drop,axis=0)

    except Exception as e :
        if verbose:
            print (e)
        pass

    return data

def fix_depths(data,like=['_m','_ft'],verbose=True):
    depths=[d for d in data.columns if d.lower().startswith('depth')]
    print(depths)
    depth_map={d:'_'.join(d.split('_')[:-1]) for d in depths if len(d.split('_'))>2 }
    print (depth_map)
    
    data=data.rename(columns=depth_map)

    for l in like:
        depths=data.filter(like=l,)
        cols=[c for c in depths.columns if c.endswith(l)]
        cols=list(set(cols))

        if verbose:
            print('Filling', cols)
        data[cols]=data[cols].replace(0,np.nan)
        depths=data[cols].copy()

        depths=depths.apply(lambda x: x.fillna(x.mean(skipna=True)),axis=1)
        data[cols]=depths
        # data.drop(data.columns.isduplicated(),axis=1)
    return data
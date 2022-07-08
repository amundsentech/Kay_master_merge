import sys
import subprocess
try:
    print('check for pandas')
    import pandas as pd
    
except:
    try:
        print('install pandas')
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
    except:
        print('upgrade pip then try again')
        subprocess.check_call([sys.executable,'-m','pip','install','--upgrade','pip'])
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
        import pandas as pd
import filter_config as config

def pull_sample_ids(data,id_formats=config.sample_id_formats):
    print('Sample_ids')
    
    data=data.replace(' ','')
    ## fix index
    data.index=data.index.astype(int)
    ##search for columns with samp in thier names 
    sample_ids=[samp for samp in list(data.columns) if ('samp' in samp.lower())]
    print(f'get sample ids from {sample_ids},with forms{id_formats}')
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
    data=data.drop(sample_cols,axis=1)
    #drop data with no values
    for col in data.columns:
        if data[col].isna().sum()==len(data):
            print(f'Drop {col}: no data')
            data=data.drop(col,axis=1) 
    data=data.sort_values('sample_id')
    data=data.set_index('sample_id')
    return data
'''
column clean up just loops through the mappings
'''
def column_cleanup(data,mapping=config.depth_mapping):
    print('Carrot_ cleanup')
    data=data.astype(str)
    for value in mapping.values():
        if value in data.columns:
            data[value].fillna('',inplace=True)
        else: 
            data[value]=''
    for key,value in mapping.items():
        print (f'add {key} to {value} and drop {key}')
        try:
            data[value]=data[value]+data[key]
            data[value]=data[value].fillna('')
            data[value]=data[value].replace({'nan':''})
            data=data.drop(key,axis=1)
        except Exception as e:
            print(e)

    data=data.replace({'nan':''})
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

            


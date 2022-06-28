import pandas as pd

def pull_sample_ids(data,id_formats=['[a-zA-Z]{1}[0-9]{1}','[a-zA-Z]{2}[0-9]{1}','[a-zA-Z]{3}[0-9]{1}']):
    sample_ids=[samp for samp in list(data.columns) if ('samp' in samp.lower())]
    data_clean=pd.DataFrame()
    data_clean['sample_id']=0
    for col in sample_ids:
        for i in range(len(id_formats)):
                data[col]=data[col].astype(str)
                data['is_id']=data[col].str.contains(id_formats[i])
                data_clean['sample_id']=pd.concat([data_clean['sample_id'],data[col][data['is_id']==True]].copy(),ignore_index=True)

    return data_clean.sort_values()
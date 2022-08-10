import getopt,sys
import subprocess
import os
import cleaningtools as ct 
import pandas as pd
import file_config as fconfig
import xrf_config as config
import numpy as np
import datetime

def main(argv):
    xrf_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('xrf_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                xrf_file = arg
                print (f'Input file is {arg} ',)
                xrf=pd.read_csv(xrf_file)
                output_file=xrf_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)

    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR: read from CONFIG')
    if len(xrf_file)==0:
        xrf_file=fconfig.xrf_file
        xrf=pd.read_csv(xrf_file,low_memory=False)
        output_file=xrf_file
        print ('no_input use ', output_file)
    print ('Input file is ', xrf_file)
    print ('Output file is ', output_file)

    #### clean and fill xrf data
    path=xrf_file
    base_path=ct.get_base_path(path,start_point='_AZ_Kay')
    hole_path=base_path+config.holes
    raw_path=base_path+config.raw
    collar_path=base_path+config.collars
    collars=pd.read_csv(collar_path)    
    data_list=[]
    for file in os.listdir(raw_path):
        print(file)
        try:
            data=pd.read_excel(raw_path+file)
            data['FileName']=file
            data_list.append(data)
        except Exception as e:
            print(e)
    
    xrf=pd.concat(data_list)
    xrf=xrf.reset_index(drop=True)

    xrf[xrf=='<LOD']=np.nan
    xrf[xrf=='na']=np.nan
    for map in config.mappings:
        xrf=ct.column_cleanup(xrf,mapping=map)
    xrf=ct.drop_no_data(xrf)

    ##create hole_id column
    for format in config.hole_id_formats:
        xrf[format]=xrf.file.str.extract(format,expand=False)
    xrf.loc[xrf[config.hole_id_formats[1]].isna(),'hole_id']=xrf.loc[xrf[config.hole_id_formats[1]].isna(),config.hole_id_formats[0]]
    xrf.loc[xrf.hole_id.isna(),'hole_id']=xrf.loc[xrf.hole_id.isna(),config.hole_id_formats[1]]

    for format in config.hole_id_formats:
        xrf=xrf.drop(format,axis=1)
    drop_index=(xrf[xrf['sample_id_xrf'].str.contains('penman')==True]).index
    xrf=xrf.drop(drop_index,axis=0)
    drop_index=xrf[xrf.hole_id.isna()].index
    xrf=xrf.drop(drop_index,axis=0)
    ## fix hole_ids
    fix_hole=xrf['sample_id_xrf'].fillna('').str.split('-').str[0].str.isdigit()
    xrf.loc[fix_hole,'hole_id']=(xrf[fix_hole].hole_id.str.split('-').str[:-1].str.join('-')+'-'+xrf[fix_hole].sample_id_xrf.str.split('-').str[0]).values
    ends=xrf.sample_id_xrf.str.split('-').str[0].unique()
    for end in ends:
        
        hole=collars[collars.Hole.str.split('-').str[-1]==end].Hole.values
        if len(hole)>0:
            print(hole)
            xrf.loc[xrf.sample_id_xrf.str.split('-').str[0]==end,'hole_id']=hole[0]
    columns= list(xrf.filter (like='Real').columns)
    for i in range(len(columns[:-1])):
        
        drop_index=xrf[xrf[columns[i]]!=xrf[columns[i+1]]].index
        print (f'drop rows {drop_index}')
        xrf=xrf.drop(drop_index,axis=0)

    xrf=ct.generate_from_to(xrf,sort_by=['sample_id_xrf','depth_ft','hole_id'])
    
    drop=xrf.loc[xrf.from_ft+10< xrf.to_ft].index
    xrf=xrf.drop(drop,axis=0)
    print('drop',drop)
    xrf=ct.remove_depth_errors(xrf)

    starting_cols=['sample_id_xrf','from_ft','to_ft','from_m','to_m','hole_id','geo']
    ending_cols=[col for col in xrf.columns if col not in starting_cols]
    xrf=pd.concat([xrf[starting_cols],xrf[ending_cols]],axis=1)
    print(f'output to {output_file}')
    xrf.to_csv(output_file,index=False)
    holes=xrf.hole_id.unique()
    for hole in holes:

        print(f'create {hole} .xlsx file')
        
        data=xrf[xrf.hole_id==hole]
        
        data.to_excel(hole_path+hole+'.xlsx')

    return xrf

if __name__ == "__main__":
    main(sys.argv[1:])
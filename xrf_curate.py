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
        opts, args = getopt.getopt(argv,"ri:o:v:",["input_file=","output_file="])
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
            elif opt in ("-v", "--output_file"):
                verbose=arg
                print ('Verbose= ', verbose)

    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR: read from CONFIG')
    if len(xrf_file)==0:
        xrf_file=fconfig.xrf_file
        try:
            xrf=pd.read_csv(xrf_file,low_memory=False)
        except:
            xrf=pd.DataFrame()

        output_file=xrf_file
        verbose=config.verbose
        print ('no_input use ', output_file)
    print ('Input file is ', xrf_file)
    print ('Output file is ', output_file)
    
    print('------------------------------------------------------------------------------')
    print('################ XRF #############')
    #### clean and fill xrf data
    path=xrf_file
    base_path=ct.get_base_path(path,start_point='_AZ_Kay')
    raw_path=base_path+config.raw  
    data_list=[]
    for file in os.listdir(raw_path):
        print(file)
        try:
            data=pd.read_excel(raw_path+file)
            data['FileName']=file
            data=ct.drop_bad_columns(data,verbose=verbose)
            data=ct.clean_column_names(data)
            data=ct.reorder_columns(data,verbose=verbose)
            data=ct.drop_bad_rows(data,verbose=verbose)
            data_list.append(data)
        except Exception as e:
            print(e)
    
    xrf=pd.concat(data_list)
    xrf=xrf.reset_index(drop=True)
    print(f'output{output_file}')
    xrf.to_csv(output_file,index=False)




if __name__ == "__main__":
    main(sys.argv[1:])
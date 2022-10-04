import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd
import file_config as fconfig
import alteration_config as config
import datetime

def main(argv):
    data_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('alteration_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                data_file = arg
                print (f'Input file is {arg} ',)
                data=pd.read_csv(data_file)
                output_file=data_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(data_file)==0:
        data_file=fconfig.alter_file
        data=pd.read_csv(data_file,low_memory=False)
        output_file=data_file
    print ('Input file is ', data_file)
    print ('Output file is ', output_file)
    #### clean and fill alter data
    print('################ ALTERATION #############')
    data=ct.depth_cleanup(data)
    for map in config.mappings:
        data=ct.column_cleanup(data,mapping=map)
    data=ct.remove_depth_errors(data,sort_by=['hole_id','from_ft'])
    print(f'output {output_file}')
    data.to_csv(output_file,index=False)
    return data

if __name__ == "__main__":
    main(sys.argv[1:])
import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd
import file_config as fconfig
import mineralization_config as config
import datetime

def main(argv):
    mineral_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('mineralogy_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                mineral_file = arg
                print (f'Input file is {arg} ',)
                mineral=pd.read_csv(mineral_file)
                output_file=mineral_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(mineral_file)==0:
        mineral_file=fconfig.mineral_file
        data=pd.read_csv(mineral_file,low_memory=False)
        output_file=mineral_file
    print ('Input file is ', mineral_file)
    print ('Output file is ', output_file)
    #### clean and fill mineral data
    print('------------------------------------------------------------------------------')
    print('################ MINERALIZATION #############')
    for map in config.mappings:
        data=ct.column_cleanup(data,mapping=map)

    data=ct.clean_column_names(data,spaces=True)
    data=ct.drop_no_data(data)
    data=ct.depth_cleanup(data)
    data=ct.remove_depth_errors(data)
    
    print(f'output {output_file}')
    mineral.to_csv(output_file,index=False)
    print('------------------------------------------------------------------------------')
    return mineral

if __name__ == "__main__":
    main(sys.argv[1:])
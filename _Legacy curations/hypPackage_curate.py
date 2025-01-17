import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd
import file_config as fconfig
import hypPackage_config as config
import datetime

def main(argv):
    hyp_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('hypPackage_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                hyp_file = arg
                print (f'Input file is {arg} ',)
                hyp=pd.read_csv(hyp_file)
                output_file=hyp_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(hyp_file)==0:
        hyp_file=fconfig.hyp_file
        data=pd.read_csv(hyp_file,low_memory=False)
        output_file=hyp_file
    print ('Input file is ', hyp_file)
    print ('Output file is ', output_file)
    print('------------------------------------------------------------------------------')
    print('################ HYPER SPECTRAL #############')
    #### clean and fill hyp data
    
    for map in config.mappings:
        data=ct.column_cleanup(hyp,mapping=map)

    data=ct.drop_no_data(data)
    data=ct.clean_column_names(data)
    data=ct.depth_cleanup(data)
    print(f'output {output_file}')
    data.to_csv(output_file,index=False)
    print('------------------------------------------------------------------------------')
    return data

if __name__ == "__main__":
    main(sys.argv[1:])
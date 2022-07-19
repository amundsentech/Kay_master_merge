import getopt,sys
import subprocess
import cleaningtools as ct 
import pandas as pd 
import file_config as fconfig
import lithology_config as config
import datetime

def main(argv):
    lith_file=[]
    try:
        opts, args = getopt.getopt(argv,"ri:o:",["input_file=","output_file="])
        for opt, arg in opts:
            if opt == '-r':
                print ('lithology_curate.py -i <input_file> -a <output_file>')
                print('using defaults if no file specified')
                
            elif opt in ("-i", "--input_file"):
                lith_file = arg
                print (f'Input file is {arg} ',)
                lith=pd.read_csv(lith_file)
                output_file=lith_file
            elif opt in ("-o", "--output_file"):
                output_file = arg
                print ('Output file is ', output_file)
    except getopt.GetoptError as e:
        print (e)
        print ('FILE READ ERROR read from CONFIG')
    if len(lith_file)==0:
        lith_file=fconfig.lith_file
        lith=pd.read_csv(lith_file,low_memory=False)
        output_file=lith_file
    print ('Input file is ', lith_file)
    print ('Output file is ', output_file)
    #### clean and fill lith data
    lith=ct.depth_cleanup(lith)

    for map in config.mappings:
        lith=ct.column_cleanup(lith,mapping=map)
    print(f'output {output_file}')
    lith.to_csv(output_file,index=False)
    return lith

if __name__ == "__main__":
    main(sys.argv[1:])
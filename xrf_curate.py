import getopt,sys
import subprocess
try:
    print('check for pandas')
    import pandas as pd
    import numpy as np
    
except:
    try:
        print('install pandas')
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
    except:
        print('upgrade pip then try again')
        subprocess.check_call([sys.executable,'-m','pip','install','--upgrade','pip'])
        subprocess.check_call([sys.executable,'-m','pip','install','pandas'])
        import pandas as pd

import cleaningtools as ct 
import file_config as fconfig
import xrf_config as config
import datetime

def main(argv):
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
        print ('FILE READ ERROR read from CONFIG')
        xrf_file=fconfig.xrf_file
        xrf=pd.read_csv(xrf_file,low_memory=False)
        output_file=xrf_file
    print ('Input file is ', xrf_file)
    print ('Output file is ', output_file)
    #### clean and fill xrf data
    xrf[xrf=='<LOD']=np.nan
    xrf[xrf=='na']=np.nan
    xrf=ct.depth_cleanup(xrf)
    for map in config.mappings:
        xrf=ct.column_cleanup(xrf,mapping=map)
    
    print(f'output to {output_file}')
    xrf.to_csv(output_file,index=False)
    return xrf

if __name__ == "__main__":
    main(sys.argv[1:])